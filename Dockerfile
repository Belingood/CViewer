# Używamy oficjalnego, odchudzonego obrazu Pythona 3.14 (wersja slim dla mniejszego rozmiaru)
FROM python:3.14-slim

# Ustawienie zmiennych środowiskowych zapobiegających tworzeniu plików .pyc
# oraz wymuszających natychmiastowe wypisywanie logów
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ustawienie katalogu roboczego wewnątrz kontenera
WORKDIR /app

# Kopiowanie pliku z zależnościami
COPY requirements.txt .

# Instalacja zależności systemowych (przydatne później dla OpenCV i Tesseract)
# oraz zależności z pliku requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-pol \
    libtesseract-dev \
    poppler-utils \
    libgl1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego projektu
COPY src/ /app/src/

# Uruchomienie serwera aplikacji z wykorzystaniem uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
