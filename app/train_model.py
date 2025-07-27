import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

def train_model(vectorizer_type="tfidf", model_type="logistic"):
    # Set base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..")

    # Paths to CSV files
    csv1_path = os.path.join(data_dir, "training_data_doubled.csv")
    csv2_path = os.path.join(data_dir, "Expanded_Training_Data_With_Tips.csv")

    # Load and merge CSVs
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)
    df = pd.concat([df1, df2], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)

    # Choose vectorizer
    if vectorizer_type == "count":
        vectorizer = CountVectorizer()
    else:
        vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(df["text"])

    # Choose model
    if model_type == "naive_bayes":
        model = MultinomialNB()
    else:
        model = LogisticRegression(max_iter=1000)

    # Train and save
    model.fit(X, df["label"])
    joblib.dump(model, os.path.join(data_dir, "model.pkl"))
    joblib.dump(vectorizer, os.path.join(data_dir, "vectorizer.pkl"))
    print(f"Model and vectorizer saved successfully with {model_type} + {vectorizer_type}.")

if __name__ == "__main__":
    train_model()  # Default run
