from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base
import os
import tempfile
from app.ocr.ocr import extract_text
from app.ml.classifier import load_model_and_vectorizer, predict_category
from app.database import SessionLocal
from app.models import Document
from fastapi.middleware.cors import CORSMiddleware

# Load model and vectorizer at startup
model, vectorizer = load_model_and_vectorizer()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["http://localhost:8000"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DB session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    valid_extensions = (".pdf", ".png", ".jpg", ".jpeg")
    if not file.filename.lower().endswith(valid_extensions):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF or image.")

    suffix = os.path.splitext(file.filename)[1]


    # Creates temp file for classification (OCR processing)
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        tmp_path = tmp.name

    try:
        text = extract_text(tmp_path)  # Calls extract_text method
    finally:
        os.remove(tmp_path)  # Deletes temp file from memory

    category, confidence = predict_category(model, vectorizer, text)

    new_doc = Document(
        category=category,
        confidence=confidence
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
        # Local FastAPI view (dev view)
        "id": new_doc.id,
        "category": category,
        "confidence": confidence,
        "preview": "[hidden in demo]"
    }


@app.get("/documents/")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.created_at.desc()).all()
    return [
        {
            # User view
            "id": doc.id,
            "category": doc.category,
            "confidence": doc.confidence,
            "created_at": doc.created_at.isoformat()
        }
        for doc in docs
    ]
