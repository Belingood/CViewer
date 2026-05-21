import re
import cv2
import numpy as np
import pytesseract
from PIL import Image
from typing import Optional
from src.schemas.cv import ExtractedCVData


class OCRService:
    """
    Serwis odpowiedzialny za przetwarzanie obrazów, ekstrakcję tekstu (OCR)
    oraz wyciąganie ustrukturyzowanych informacji (NLP/Regex).
    """

    def _preprocess_image(self, image: Image.Image) -> np.ndarray:  # type: ignore
        """
        Przetwarzanie wstępne obrazu w celu poprawy jakości dla silnika Tesseract.
        Konwersja do skali szarości i binaryzacja.
        """
        # Wymuszenie formatu RGB (zabezpieczenie przed obrazami w skali szarości - 1 kanał, lub z kanałem alfa - RGBA)
        image = image.convert('RGB')

        # Konwersja obrazu PIL na tablicę NumPy (format OpenCV)
        open_cv_image = np.array(image)

        # Konwersja z RGB (format PIL) na BGR (natywny format OpenCV)
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        # Konwersja do skali szarości
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Zastosowanie progowania adaptacyjnego (binaryzacja)
        # Poprawia kontrast między tekstem a tłem (czarny tekst, białe tło)
        processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        return processed_img  # type: ignore

    def _extract_email(self, text: str) -> Optional[str]:
        """Ekstrakcja adresu e-mail z tekstu za pomocą wyrażenia regularnego."""
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """
        Ekstrakcja numeru telefonu (polski format, z kierunkowym lub bez).
        """
        phone_pattern = r'(?:\+?48)?[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}'
        match = re.search(phone_pattern, text)
        # Oczyszczenie znalezionego numeru z białych znaków
        return match.group(0).strip() if match else None

    def process_image(self, image: Image.Image) -> ExtractedCVData:
        """
        Główna metoda koordynująca proces ekstrakcji dla pojedynczego obrazu.
        """
        # 1. Przetwarzanie wstępne (Computer Vision)
        processed_cv2_image = self._preprocess_image(image)

        # 2. Ekstrakcja tekstu (OCR) - język polski i angielski
        # Wymaga zainstalowanych paczek językowych w systemie (tesseract-ocr-pol tesseract-ocr-eng)
        raw_text = pytesseract.image_to_string(processed_cv2_image, lang='pol+eng')

        # 3. Analiza i ekstrakcja danych ustrukturyzowanych
        email = self._extract_email(raw_text)
        phone = self._extract_phone(raw_text)

        return ExtractedCVData(
            email=email,
            phone=phone,
            raw_text=raw_text.strip()
        )
