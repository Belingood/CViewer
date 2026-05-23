# CViewer - CV Information Extraction & Face Detection System

**CViewer** is an automated, lightweight, and local system designed to extract structured information (email, phone number) and profile photos from unstructured CV documents (JPEG, PNG, WEBP). 

This repository represents the backend implementation, developed as a semester project for the course **Metody rozpoznawania i przetwarzania obrazów** (Image Recognition and Processing Methods) at a Polish technical university.

---

## 🚀 Key Features

*   **Advanced Image Preprocessing:** Utilizes `OpenCV` to perform image upscaling, Gaussian blurring (background noise reduction), and adaptive binarization (Otsu's thresholding) to maximize OCR readability.
*   **Classical Face Detection:** Implements the **Viola-Jones algorithm via Haar Cascades** (`CascadeClassifier`) to detect, crop, and save candidate profile photos without the need for heavy deep learning neural networks.
*   **Fuzzy NLP Extraction:** Uses regular expressions equipped with "fuzzy" matching to dynamically identify contact details and auto-correct typical OCR artifacts (e.g., mistaking `@` for `Q` or `©`, or inserting blank spaces).
*   **Strict Architecture:** Built using the **Explicit Composition Root** pattern to ensure decoupling, clean dependency injection, and high testability.
*   **Industrial Tooling:** Full static type checking (`Mypy`), rigorous code formatting and linting (`Ruff`), unit and integration tests (`Pytest` with `Mocking`), and automatic gatekeeping (`pre-commit` hooks).

---

## 📚 Language and Academic Localization Note

In compliance with the pedagogical guidelines of the **Metody rozpoznawania i przetwarzania obrazów** course and academic transparency standards, **all internal code documentation, docstrings, and inline comments are strictly written in Polish**. 

This is a deliberate architectural decision. It ensures that the academic terminology of the curriculum (e.g., *progowanie adaptacyjne*, *kaskady Haara*, *rozmycie Gaussa*, *binaryzacja*) is mapped directly and unambiguously to the software implementation for grading and review purposes, while the global README and API contract remain in English for universal compatibility.

---

## 🛠️ Technology Stack

*   **Language:** Python 3.14 (fully typed)
*   **Web Framework:** FastAPI (asynchronous, modern REST API)
*   **Image Processing & CV:** OpenCV, Pillow, PyTesseract, PDF2Image
*   **Database:** PostgreSQL 16 + SQLAlchemy 2.0 (using `asyncpg` async driver)
*   **DevOps & QA:** Docker, docker-compose, pytest, ruff, mypy, taskipy, pre-commit

---

## ⚙️ Getting Started

### Prerequisites
*   Docker & Docker Desktop installed on your machine (supports Windows 11 with WSL2).

### 1. Launch the Stack
Initialize and run the multi-container environment (API and Database):
```bash
docker-compose up --build
```
The system implements a `healthcheck` on the database layer. The FastAPI container will wait and only initialize the application once PostgreSQL is fully ready to accept connections.

### 2. Interactive API Documentation
Once the stack is running, access the interactive Swagger UI to test the endpoints:
*   **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)

You can upload a CV image using the `POST /api/v1/cv/upload/` endpoint. If a face is successfully detected, the extracted profile image will be saved and served statically at `http://localhost:8000/uploads/faces/...`.

---

## 🧪 Development & Quality Assurance

To maintain a clean codebase, a localized task runner is configured. You can execute the entire verification pipeline (formatting, linting, type-checking, and tests) locally with a single command:

```bash
task check
```

This runs:
1.  `ruff format .` (Formatting)
2.  `ruff check --fix .` (Linting)
3.  `mypy src/` (Type Checking)
4.  `pytest` (Unit and Mock Testing)

*Note: These checks are also run automatically before every git commit via the installed `pre-commit` hooks.*
