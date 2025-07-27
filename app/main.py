from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import tempfile

from app.database import engine, Base, SessionLocal
from app.models import Document
from app.ocr.ocr import extract_text
from app.ml.classifier import load_model_and_vectorizer, predict_category

# Initialize FastAPI app
app = FastAPI()

# Mount static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the index.html at root
@app.get("/", response_class=FileResponse)
def read_index():
    return FileResponse("frontend/index.html")

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and vectorizer at startup
model, vectorizer = load_model_and_vectorizer()

# Create DB tables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Base.metadata.create_all(bind=engine)

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp.flush()
        tmp_path = tmp.name

    try:
        text = extract_text(tmp_path)
    finally:
        os.remove(tmp_path)

    category, confidence = predict_category(model, vectorizer, text)

    new_doc = Document(category=category, confidence=confidence)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    return {
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
            "id": doc.id,
            "category": doc.category,
            "confidence": doc.confidence,
            "created_at": doc.created_at.isoformat()
        }
        for doc in docs
    ]
