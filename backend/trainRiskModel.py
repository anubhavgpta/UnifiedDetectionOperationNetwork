import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# === Step 1: Load the processed data ===
df = pd.read_csv("processed_packets.csv")

# === Step 2: Encode labels ===
label_map = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
df["risk_encoded"] = df["risk"].map(label_map)

# === Step 3: Select features ===
X = df[["length", "packet_mean", "packet_std"]]
y = df["risk_encoded"]

# === Step 4: Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Step 5: Train model ===
model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

print("Model accuracy:", model.score(X_test, y_test))

# === Step 6: Save model ===
joblib.dump(model, "risk_model.pkl")
print("Model saved as risk_model.pkl")
