from preprocess import load_and_preprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

X, y, tfidf, scaler = load_and_preprocess(
    "../data_samples/emails.csv"
)


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

# Save artifacts
joblib.dump(model, "risk_model.pkl")
joblib.dump(tfidf, "tfidf.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model trained and saved.")
