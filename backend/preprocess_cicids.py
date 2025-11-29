"""
preprocess_cicids.py
--------------------
Prepares the Kaggle 'CICIDS2017: Cleaned & Preprocessed' dataset for
machine learning training compatible with the UDON backend.
"""

import pandas as pd
from app.ml.labeler import map_attack_label_to_risk  # make sure labeler.py exists

# === Step 1: Load dataset ===
input_path = "cicids2017_cleaned.csv"  # your file name
print(f"Loading dataset from {input_path} ...")
df = pd.read_csv(input_path)

print(f"Dataset loaded with {len(df)} rows and {len(df.columns)} columns.")

# === Step 2: Build numerical features ===
# Create a 'length' proxy using total forward length and backward packet length mean
df["length"] = df["Total Length of Fwd Packets"] + df["Bwd Packet Length Mean"]

# Normalize NaN or inf values
df = df.replace([float('inf'), -float('inf')], 0).fillna(0)

# === Step 3: Simple derived features ===
df["packet_mean"] = df["Packet Length Mean"]
df["packet_std"] = df["Packet Length Std"]

# === Step 4: Risk label mapping ===
df["risk"] = df["Attack Type"].apply(lambda x: map_attack_label_to_risk(x))

# === Step 5: Keep only the relevant features ===
columns_to_keep = ["length", "packet_mean", "packet_std", "risk"]
processed = df[columns_to_keep]

# === Step 6: Save ===
output_path = "processed_packets.csv"
processed.to_csv(output_path, index=False)
print(f"Processed dataset saved to {output_path}")
print(processed["risk"].value_counts())
