import os
import requests

API_URL = "http://127.0.0.1:8000/upload/"
FOLDER_PATH = "test_pdfs"

# Loop through all PDF files in the folder
for filename in os.listdir(FOLDER_PATH):
    if filename.endswith(".pdf"):
        file_path = os.path.join(FOLDER_PATH, filename)
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, "application/pdf")}
            response = requests.post(API_URL, files=files)
            print(f"{filename} → {response.status_code}: {response.text}")
