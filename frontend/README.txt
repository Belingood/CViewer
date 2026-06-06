# CViewer Frontend

Frontend aplikacji webowej do projektu: **System ekstrakcji informacji z dokumentów CV na podstawie analizy obrazu dokumentu i OCR**.

Projekt wykonany w React + Vite na podstawie kontraktu API CViewer.

## Funkcje

- Dashboard z listą przesłanych CV.
- Upload CV w formatach JPG, JPEG, PNG i WEBP.
- Widok szczegółów dokumentu CV.
- Wyświetlanie surowego tekstu OCR.
- Wyświetlanie danych kandydata.
- Korekta danych kandydata po OCR.
- Usuwanie dokumentu CV.
- Obsługa błędów API i statusów ładowania.
- Konfiguracja adresu backendu przez plik `.env`.

## Wymagania

- Node.js 18 lub nowszy.
- Działający backend pod adresem `http://localhost:8000`.

## Uruchomienie

1. Wejdź do folderu projektu:

```bash
cd cviewer-frontend
```

2. Zainstaluj zależności:

```bash
npm install
```

3. Utwórz plik `.env` na podstawie `.env.example`:

```bash
copy .env.example .env
```

Na Linux/macOS:

```bash
cp .env.example .env
```

4. Uruchom frontend:

```bash
npm run dev
```

5. Otwórz adres pokazany w terminalu, zwykle:

```txt
http://localhost:5173
```

## Ważna uwaga

Aktualny kontrakt API przyjmuje tylko obrazy: `.jpg`, `.jpeg`, `.png`, `.webp`. Pliki PDF są zablokowane w interfejsie, ponieważ backend według kontraktu jeszcze ich nie obsługuje.