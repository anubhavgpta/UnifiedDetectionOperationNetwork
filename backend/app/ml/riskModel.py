"""
riskModel.py
-------------
This module provides the interface between the packet capture engine and
the Machine Learning model responsible for classifying packets based on
their risk level (e.g., LOW, HIGH).

Author: Your Name
Project: UDON - Intrusion Detection System
"""

import random
import numpy as np

# Placeholder model class
class RiskModel:
    def __init__(self):
        # In the final implementation, your partner will load a trained ML model here.
        # For example:
        # self.model = joblib.load("model.pkl")
        pass

    def preprocess(self, packet):
        """
        Convert raw packet data into numerical features that the ML model can process.
        This may include encoding categorical data (e.g., protocol type) and normalizing numerical values.
        """
        try:
            features = np.array([
                len(packet.get("source", "")),       # Example feature: source IP length
                len(packet.get("destination", "")),  # Example feature: destination IP length
                packet.get("length", 0),             # Example feature: packet size
                {"TCP": 1, "UDP": 2, "ICMP": 3, "HTTP": 4, "DNS": 5, "ARP": 6}.get(packet.get("protocol", ""), 0)
            ])
            return features.reshape(1, -1)
        except Exception as e:
            raise ValueError(f"Feature extraction failed: {e}")

    def predictRisk(self, packet):
        """
        Predicts the risk level for a given packet.
        Returns either 'LOW' or 'HIGH'.
        """
        # Placeholder for testing: use a random choice
        # This will later be replaced with the actual model's prediction
        simulatedRisk = random.choice(["LOW", "HIGH"])
        return simulatedRisk


# Singleton instance (imported by other modules)
riskModel = RiskModel()
