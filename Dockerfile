WORKDIR /app
COPY requirements.txt .

# OCR dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

