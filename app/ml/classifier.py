from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Trains a logistic regression model
def train_model(docs, labels):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)
    model = LogisticRegression()
    model.fit(X, labels)
    return model, vectorizer

# Loads trained model and vectorizer
def load_model_and_vectorizer():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "model.pkl")
    vectorizer_path = os.path.join(base_dir, "vectorizer.pkl")

    print(f"Trying to load model from: {model_path}")
    print(f"Trying to load vectorizer from: {vectorizer_path}")

    # Checks if model and vectorizer exist
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"model.pkl not found at: {model_path}")
    if not os.path.exists(vectorizer_path):
        raise FileNotFoundError(f"vectorizer.pkl not found at: {vectorizer_path}")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Model and vectorizer loaded successfully.")
    return model, vectorizer

# Predicts document type and confidence from the extracted text
def predict_category(model, vectorizer, text: str):
    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X).max()
    return prediction, float(confidence)
