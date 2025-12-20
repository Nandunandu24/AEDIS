import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

# ------------------------------------------------------------------
# Absolute path handling (CRITICAL FIX)
# ------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data_samples", "emails.csv")

# ------------------------------------------------------------------
# Email body extraction (Enron-style emails)
# ------------------------------------------------------------------
def extract_email_body(raw_message: str) -> str:
    """
    Extracts the email body from raw RFC-style email text.
    """
    if pd.isna(raw_message):
        return ""

    # Split headers and body at first empty line
    parts = raw_message.split("\n\n", 1)
    if len(parts) == 2:
        return parts[1].strip()

    return raw_message.strip()

# ------------------------------------------------------------------
# Load + preprocess data
# ------------------------------------------------------------------
def load_and_preprocess():
    # ---- LOAD DATA SAFELY ----
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"emails.csv not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # ---- VALIDATE EXPECTED COLUMN ----
    if "message" not in df.columns:
        raise ValueError("Expected 'message' column not found in CSV")

    # ---- CLEAN TEXT ----
    df["text"] = df["message"].apply(extract_email_body)

    # Drop very short / empty emails
    df = df[df["text"].str.len() > 10].reset_index(drop=True)

    # ---- TEXT FEATURES (TF-IDF) ----
    tfidf = TfidfVectorizer(
        max_features=500,
        stop_words="english"
    )
    text_features = tfidf.fit_transform(df["text"]).toarray()

    # ---- NUMERIC FEATURES (PLACEHOLDERS FOR WEEK 3) ----
    # These simulate enterprise metadata
    df["length"] = df["text"].str.len()
    df["has_attachment"] = 0
    df["sentiment"] = 0.0
    df["past_interactions"] = 1

    numeric_features = df[
        ["length", "has_attachment", "sentiment", "past_interactions"]
    ].values

    scaler = StandardScaler()
    numeric_features = scaler.fit_transform(numeric_features)

    # ---- COMBINE FEATURES ----
    X = pd.concat(
        [
            pd.DataFrame(text_features),
            pd.DataFrame(numeric_features)
        ],
        axis=1
    )

    # ---- TEMP LABELING (WEEK 3 ONLY) ----
    # You will replace this with real decision labels later
    df["label"] = "escalate"
    y = df["label"]

    return X, y, tfidf, scaler
