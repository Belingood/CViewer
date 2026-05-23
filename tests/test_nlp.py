from src.services.ocr_service import OCRService


def test_extract_email_standard() -> None:
    """Test poprawnej ekstrakcji standardowego adresu e-mail."""
    service = OCRService()
    text = "Kontakt do mnie: jan.kowalski@example.com. Zapraszam!"
    assert service._extract_email(text) == "jan.kowalski@example.com"


def test_extract_email_ocr_errors() -> None:
    """Test naprawy typowych błędów silnika OCR w adresach e-mail."""
    service = OCRService()
    # Tesseract wstawia spacje i literę 'Q' zamiast '@'
    text_with_error = "Email: anna.nowakQ gmail.com "
    assert service._extract_email(text_with_error) == "anna.nowak@gmail.com"

    # Tesseract wstawia '©'
    text_with_copyright = "test.user ©edu.pl"
    assert service._extract_email(text_with_copyright) == "test.user@edu.pl"


def test_extract_phone_polish() -> None:
    """Test ekstrakcji standardowych, polskich numerów (9 cyfr)."""
    service = OCRService()
    assert service._extract_phone("Tel: 123 456 789") == "123 456 789"
    assert service._extract_phone("123-456-789") == "123-456-789"


def test_extract_phone_international() -> None:
    """Test ekstrakcji numerów z kodem kraju i formatów zagranicznych."""
    service = OCRService()
    assert service._extract_phone("Phone: +48 508-762-847") == "+48 508-762-847"
    assert service._extract_phone("(508) 762 8478") == "(508) 762 8478"  # Format US


def test_extract_phone_ignore_dates() -> None:
    """Test weryfikujący, czy system ignoruje daty wyglądające jak numery."""
    service = OCRService()
    # To jest data w CV, nie powinna zostać uznana za telefon
    text_with_date = "Praca w firmie XYZ: 2015-08 - 2018-05"
    assert service._extract_phone(text_with_date) is None
