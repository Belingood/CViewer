import re

import cv2
import numpy as np
import pytesseract
from PIL import Image

from src.schemas.cv import ExtractedCVData


class OCRService:
    """
    Serwis odpowiedzialny za przetwarzanie obrazów, ekstrakcję tekstu (OCR)
    oraz wyciąganie ustrukturyzowanych informacji (NLP/Regex).
    """

    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Zaawansowane przetwarzanie wstępne obrazu.
        Zawiera skalowanie, konwersję do skali szarości, usuwanie szumu i binaryzację.
        """
        # Wymuszenie formatu RGB
        image = image.convert("RGB")

        # Konwersja obrazu PIL na tablicę NumPy (format OpenCV BGR)
        open_cv_image = np.array(image)[:, :, ::-1].copy()

        # 1. Skalowanie obrazu (Powiększenie 2x)
        # Znacząco poprawia skuteczność silnika Tesseract dla małych czcionek
        scaled_img = cv2.resize(open_cv_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # 2. Konwersja do skali szarości
        gray = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2GRAY)

        # 3. Rozmycie Gaussa (Gaussian Blur)
        # Pomaga zredukować szum tła (np. znaki wodne, kolorowe wzory w CV)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # 4. Binaryzacja adaptacyjna (OTSU)
        processed_img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return processed_img

    def _extract_email(self, text: str) -> str | None:
        """
        Ekstrakcja adresu e-mail z uwzględnieniem spacji wstawianych przez OCR
        oraz typowych błędów (Q, © zamiast @).
        """
        # Dodajemy ' ?' (opcjonalna spacja) wokół symbolu małpy,
        # ponieważ Tesseract czasem rozdziela e-mail np.: "jan.kowalskiQ gmail.com"
        email_pattern = r"[a-zA-Z0-9_.+-]+ ?(?:@|Q|©) ?[a-zA-Z0-9-]+\.(?:com|pl|net|org|edu|eu|io)"

        match = re.search(email_pattern, text)
        if match:
            email = match.group(0)

            # 1. Usuwamy sztuczne spacje ze znalezionego adresu
            email = email.replace(" ", "")

            # 2. Automatyczna naprawa odczytanego znaku na poprawne '@'
            if "@" not in email:
                email = re.sub(r"(?:Q|©)", "@", email, count=1)

            return email
        return None

    def _extract_phone(self, text: str) -> str | None:
        """
        Ekstrakcja numeru telefonu z uwzględnieniem kodów krajów (np. +48, +44),
        numerów kierunkowych w nawiasach (np. (0)) oraz różnych separatorów.
        """
        # Wyjaśnienie wzorca:
        # (?:\+\d{1,3}[\s-]?)?       -> Opcjonalny kod kraju, np. "+48 ", "+44 "
        # (?:\(\d{1,3}\)[\s-]?)?     -> Opcjonalny kierunkowy w nawiasie, np. "(0) "
        # (?:\d{2,4}[\s-]?){2,4}\d{2,4} -> Bloki cyfr (od 2 do 4 w bloku),
        # oddzielone spacją lub myślnikiem
        phone_pattern = r"(?:\+\d{1,3}[\s-]?)?(?:\(\d{1,3}\)[\s-]?)?(?:\d{2,4}[\s-]?){2,4}\d{2,4}"

        # Używamy finditer, aby przeanalizować wszystkie potencjalne dopasowania
        matches = re.finditer(phone_pattern, text)

        for match in matches:
            phone_candidate = match.group(0).strip()

            # Zliczamy same cyfry w dopasowanym ciągu, ignorując znaki specjalne
            digits_only = re.sub(r"\D", "", phone_candidate)

            # Prawdziwy numer telefonu musi mieć od 9 do 15 cyfr
            if 9 <= len(digits_only) <= 15:
                # Zabezpieczenie (Negative filter): odrzucamy ciągi, które wyglądają jak daty
                # (np. "2015-08 - 2018-05"), które OCR może uznać za długi ciąg cyfr
                if re.search(r"20[0-2]\d[\s-]*[0-1]?\d", phone_candidate):
                    continue

                return phone_candidate

        return None

    def process_image(self, image: Image.Image) -> ExtractedCVData:
        """Główna metoda koordynująca ekstrakcję z pojedynczego obrazu."""
        processed_cv2_image = self._preprocess_image(image)

        # Dodanie psm 6 (Page Segmentation Mode: Assume a single uniform block of text)
        # Pomaga to Tesseractowi lepiej zachować układ i spacje
        custom_config = r"--oem 3 --psm 6"
        raw_text = pytesseract.image_to_string(
            processed_cv2_image, lang="pol+eng", config=custom_config
        )

        email = self._extract_email(raw_text)
        phone = self._extract_phone(raw_text)

        return ExtractedCVData(email=email, phone=phone, raw_text=raw_text.strip())
