from preprocess import load_and_preprocess
import joblib
from sklearn.metrics import classification_report, confusion_matrix

X, y, _, _ = load_and_preprocess(
    "../data_samples/emails.csv"
)


model = joblib.load("risk_model.pkl")
y_pred = model.predict(X)

print("Classification Report:")
print(classification_report(y, y_pred))

print("Confusion Matrix:")
print(confusion_matrix(y, y_pred))
