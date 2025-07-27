import os

from fastapi.testclient import TestClient
import pytest
import app.ocr.ocr as ocr_module

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Document registered on Base
import app.models
from app.database import Base
from app.main import app, get_db
from app.ml.classifier import load_model_and_vectorizer

# Sqlite for testing
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Bind a session factory to it
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

# Override get_db so that every request uses the same session factory
@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def mock_extract_text(monkeypatch):
    monkeypatch.setattr(ocr_module, "extract_text", lambda path: "dummy extracted text")


# Load model/vectorizer for testing
model, vectorizer = load_model_and_vectorizer()

def test_model_prediction():
    sample_text = "This is an invoice for services rendered"
    X = vectorizer.transform([sample_text])
    pred = model.predict(X)[0]
    assert pred in ["invoice", "receipt", "contract"]

def test_docs_endpoint(client):
    r = client.get("/docs")
    assert r.status_code == 200

def test_root_endpoint(client):
    r = client.get("/")
    assert r.status_code in (200, 404)

def test_model_loading():
    m, v = load_model_and_vectorizer()
    assert m is not None and v is not None


def test_pdf_classification(client):
    # Checks file path for test.pdf
    test_path = os.path.join(os.path.dirname(__file__), "test.pdf")
    assert os.path.exists(test_path), f"Missing test.pdf at {test_path}"

    with open(test_path, "rb") as f:
        r = client.post(
            "/upload/",
            files={"file": ("test.pdf", f, "application/pdf")},
        )

    # Checks response codes

    print("Status Code:", r.status_code)
    print("Response:", r.text)

    assert r.status_code == 200
    data = r.json()
    assert "category" in data
    assert "confidence" in data
    assert isinstance(data["confidence"], float)
    assert 0.0 <= data["confidence"] <= 1.0

