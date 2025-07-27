from PIL import Image
import os
import pytesseract
import platform
from pdf2image import convert_from_path

def extract_text(image_path: str) -> str:
    poppler_path = None
    if platform.system() == "Windows":
        possible_path = r"C:\poppler\Library\bin"
        if os.path.exists(possible_path):
            poppler_path = possible_path

    if image_path.endswith(".pdf"):
        images = convert_from_path(image_path, poppler_path=poppler_path)
        return "".join(pytesseract.image_to_string(img) for img in images)
    else:
        return pytesseract.image_to_string(Image.open(image_path))
