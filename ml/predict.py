import os
import joblib
import pandas as pd

# Absolute path to ml/ directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "risk_model.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

print("🔍 Loading model from:", MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(TFIDF_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_risk(text, length, has_attachment, sentiment, past_interactions):
    text_vec = tfidf.transform([text]).toarray()
    num_vec = scaler.transform([[length, has_attachment, sentiment, past_interactions]])

    X = pd.concat(
        [pd.DataFrame(text_vec), pd.DataFrame(num_vec)],
        axis=1
    )

    probs = model.predict_proba(X)[0]
    classes = model.classes_

    return {
        "predicted_label": classes[probs.argmax()],
        "risk_score": float(max(probs)),
        "confidence": float(max(probs))
    }
