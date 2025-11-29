"""
packetParser.py
----------------
Extracts and standardizes metadata from raw Scapy packets,
then passes the structured data through the ML stub for risk scoring.
"""

from scapy.all import IP, TCP, UDP, ICMP # pylint: disable=no-name-in-module
from datetime import datetime
from typing import Dict
from app.ml.featureExtractor import extractFeatures
from app.ml.modelInterface import DefaultModelHandler

# Instantiate classifier once to avoid repeated initialization
classifier = DefaultModelHandler()

def parsePacket(packet, packetId: int) -> Dict:
    """
    Extracts packet metadata and classifies risk level.
    """
    try:
        source = destination = protocol = "UNKNOWN"
        length = len(packet)
        timestamp = datetime.now().strftime("%H:%M:%S")

        if packet.haslayer(IP):
            source = packet[IP].src
            destination = packet[IP].dst

            if packet.haslayer(TCP):
                protocol = "TCP"
            elif packet.haslayer(UDP):
                protocol = "UDP"
            elif packet.haslayer(ICMP):
                protocol = "ICMP"
            else:
                protocol = f"IP-{packet[IP].proto}"
        else:
            protocol = packet.name

        # Build structured packet data
        packetData = {
            "id": packetId,
            "source": source,
            "destination": destination,
            "protocol": protocol,
            "length": length,
            "timestamp": timestamp
        }

        # Extract features and classify risk
        features = extractFeatures(packetData)
        packetData["risk"] = classifier.predict(features)

        return packetData

    except Exception as e:
        return {
            "id": packetId,
            "source": "PARSE_ERROR",
            "destination": "PARSE_ERROR",
            "protocol": "UNKNOWN",
            "length": 0,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "risk": "LOW"
        }
