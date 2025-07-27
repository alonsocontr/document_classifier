# Document Classifier

A document classification system that uses OCR and a trained machine learning model to categorize uploaded files into one of three types: receipt, invoice, or contract. The system is built using FastAPI for the backend, PostgreSQL for the data handling, and a simple frontend interface for file upload and public database display.

---

## Features

- Supports PDF, PNG, JPG, and JPEG formats
- Extracts text using OCR (Tesseract and pdf2image)
- Classifies documents using a scikit-learn model
- Stores only classification results (not file content) in PostgreSQL
- Includes public results feed sorted by most recent
- Offers a clean and minimal single-page frontend interface
- Includes a full test suite using Pytest and in-memory SQLite

---

## Technologies Used

- **FastAPI** (backend framework)
- **PostgreSQL** (database)
- **SQLAlchemy** (ORM)
- **Tesseract OCR + pdf2image** (text extraction)
- **scikit-learn** (classification)
- **HTML, CSS, JavaScript** (frontend)
- **Pytest** (testing)

