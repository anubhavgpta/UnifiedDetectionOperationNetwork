"""
featureExtractor.py
--------------------
Converts parsed packet metadata into numerical features
for the trained risk model.
"""

from typing import Dict

def extractFeatures(packetData: Dict) -> Dict:
    """
    Extract features expected by the trained model.
    """
    # Base length feature
    features = {
        "length": packetData.get("length", 0),
    }

    # Add optional statistical placeholders since live packets won’t have them
    # (the trained model uses these)
    # For real-time use, these can be approximated or extended later
    features["packet_mean"] = packetData.get("length", 0) / 2  # rough heuristic
    features["packet_std"] = packetData.get("length", 0) / 4   # rough heuristic

    return features
