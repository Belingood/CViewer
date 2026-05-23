import os
import re
import uuid

import cv2
import numpy as np
import pytesseract
from cv2 import data
from PIL import Image

from src.schemas.cv import ExtractedCVData


class OCRService:
    """
    Serwis odpowiedzialny za przetwarzanie obrazów, ekstrakcję tekstu (OCR)
    oraz wyciąganie ustrukturyzowanych informacji (NLP/Regex).
    """

    def __init__(self) -> None:
        # Inicjalizacja katalogu na zdjęcia wycięte z CV
        self.faces_dir = os.path.join("uploads", "faces")
        os.makedirs(self.faces_dir, exist_ok=True)

        # Wczytanie pretrenowanego modelu kaskad Haara (klasyczne widzenie komputerowe)
        # Model ten jest zoptymalizowany pod kątem wykrywania twarzy zwróconych przodem
        cascade_path = data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

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

    def _extract_face(self, open_cv_image: np.ndarray) -> str | None:
        """
        Wykrywa twarz na zdjęciu za pomocą algorytmu Viola-Jones (Kaskady Haara).
        Jeśli twarz zostanie znaleziona, wycina ją i zapisuje na dysku.
        Zwraca względną ścieżkę do pliku.
        """
        # Konwersja do skali szarości (wymagane przez kaskady Haara)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Detekcja twarzy
        # scaleFactor=1.1 - kompensacja rozmiaru (skalowanie obrazu w poszukiwaniu twarzy)
        # minNeighbors=5 - określa jakość detekcji (wyższa wartość = mniej fałszywych trafień)
        # minSize=(50, 50) - ignorowanie bardzo małych obiektów (np. ikonek na CV)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50)
        )

        # Jeśli nie wykryto twarzy, zwracamy None
        if len(faces) == 0:
            return None

        # Zakładamy, że na CV jest tylko jedna twarz kandydata (bierzemy pierwszą znalezioną)
        x, y, w, h = faces[0]

        # Dodanie marginesu wokół twarzy (aby nie ucinać czoła czy brody)
        margin = int(w * 0.2)
        y1 = max(0, y - margin)
        y2 = min(open_cv_image.shape[0], y + h + margin)
        x1 = max(0, x - margin)
        x2 = min(open_cv_image.shape[1], x + w + margin)

        # Wycięcie twarzy z oryginalnego, kolorowego zdjęcia
        cropped_face = open_cv_image[y1:y2, x1:x2]

        # Wygenerowanie unikalnej nazwy pliku i zapis na dysku
        filename = f"face_{uuid.uuid4().hex[:8]}.jpg"
        filepath = os.path.join(self.faces_dir, filename)

        cv2.imwrite(filepath, cropped_face)

        # Zwracamy ścieżkę w formacie przyjaznym dla URL (np. "uploads/faces/face_123.jpg")
        return filepath.replace("\\", "/")

    def process_image(self, image: Image.Image) -> ExtractedCVData:
        """Główna metoda koordynująca ekstrakcję z pojedynczego obrazu."""

        # --- Zmiana: zachowujemy oryginalny obraz do wycięcia twarzy ---
        image_rgb = image.convert("RGB")
        original_cv_image = np.array(image_rgb)[:, :, ::-1].copy()

        # 1. Przetwarzanie wstępne dla OCR (Computer Vision)
        processed_cv2_image = self._preprocess_image(image)

        # 2. Detekcja i ekstrakcja twarzy kandydata
        photo_path = self._extract_face(original_cv_image)

        # 3. Ekstrakcja tekstu (OCR)
        custom_config = r"--oem 3 --psm 6"
        raw_text = pytesseract.image_to_string(
            processed_cv2_image, lang="pol+eng", config=custom_config
        )

        # 4. Analiza NLP
        email = self._extract_email(raw_text)
        phone = self._extract_phone(raw_text)

        return ExtractedCVData(
            email=email,
            phone=phone,
            photo_path=photo_path,  # <--- Dodanie ścieżki do wyniku
            raw_text=raw_text.strip(),
        )
