"""
modelInterface.py
-----------------
Defines a unified interface for integrating trained ML models
into the UDON Intrusion Detection System backend.

This updated version:
Loads the trained model (risk_model.pkl)
Falls back to the RiskClassifierStub if unavailable
Supports multi-class predictions (LOW, MEDIUM, HIGH)
Automatically loads model once at startup
"""

import joblib
import numpy as np
from typing import Dict
from app.ml.modelStub import RiskClassifierStub


class BaseModelInterface:
    """
    Abstract base class defining the required ML interface methods.
    """

    def loadModel(self, modelPath: str) -> None:
        raise NotImplementedError("Subclasses must implement loadModel()")

    def predict(self, features: Dict) -> str:
        raise NotImplementedError("Subclasses must implement predict()")


class DefaultModelHandler(BaseModelInterface):
    """
    Default handler that loads and uses a trained risk model
    for packet classification. If unavailable, it falls back
    to the RiskClassifierStub (random predictions).
    """

    def __init__(self, modelPath: str = "risk_model.pkl"):
        self.modelPath = modelPath
        self.modelLoaded = False
        self.model = None
        self.stub = RiskClassifierStub()

        # Attempt to load model on startup
        self.loadModel()

    def loadModel(self, modelPath: str = None) -> None:
        """
        Loads the trained machine learning model from disk.
        Falls back to RiskClassifierStub if model not found or corrupted.
        """
        path = modelPath or self.modelPath
        try:
            print(f"[INFO] Loading trained risk model from {path} ...")
            self.model = joblib.load(path)
            self.modelLoaded = True
            print("[INFO] Model loaded successfully.")
        except Exception as e:
            print(f"[WARNING] Could not load model ({e}). Using fallback stub.")
            self.model = self.stub
            self.modelLoaded = False

    def predict(self, features: Dict) -> str:
        """
        Predicts risk level ('LOW', 'MEDIUM', 'HIGH') from packet features.
        If the trained model is not loaded, uses the stub.
        """
        if self.model is None:
            self.loadModel()

        # Convert features (dict) → numpy array
        try:
            X = np.array([list(features.values())])

            # If the real model is loaded
            if self.modelLoaded:
                # Handle sklearn models
                pred = int(self.model.predict(X)[0])

                # Map integer predictions to string labels
                label_map = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
                return label_map.get(pred, "LOW")

            # If not loaded, fallback to stub
            return self.stub.predict(features)

        except Exception as e:
            print(f"[ERROR] Model prediction failed: {e}")
            return self.stub.predict(features)
