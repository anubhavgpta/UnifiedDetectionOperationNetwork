# UDON – Intrusion Detection System (Backend)

UDON (Unified Detection Operations Network) is a modular, ML-ready Intrusion Detection System designed to perform real-time network packet capture, analysis, and risk classification.

This repository represents the backend subsystem, built using FastAPI and Scapy, and designed for seamless integration with a machine learning classifier that assesses the risk of each packet or protocol.

---

## Core Features

- Sequential Packet Capture — no skipped packets; IDs are generated in strict sequence.
- FastAPI REST Backend — clean and modular API endpoints for frontend interaction.
- Threaded Capture Engine — non-blocking, live packet sniffing using Scapy.
- ML-Ready Interface — built-in model stub and integration layer for easy ML plug-in.
- Structured Logging — timestamps and session tracking for every backend operation.

---

## Project Structure

```
backend/
│
├── app/
│   ├── main.py                  # FastAPI initialization and route registration
│   ├── config.py                # (Optional) global configuration parameters
│   │
│   ├── capture/
│   │   ├── packetSniffer.py     # Core sequential packet capture engine
│   │   └── packetParser.py      # Parses packets and applies ML risk evaluation
│   │
│   ├── ml/
│   │   ├── featureExtractor.py  # Converts packet metadata into ML features
│   │   ├── modelStub.py         # Randomized classifier for simulation
│   │   └── modelInterface.py    # Unified ML integration interface (plug-and-play)
│   │
│   ├── routes/
│   │   └── packetRoutes.py      # REST API endpoints for control and data retrieval
│   │
│   ├── utils/
│   │   ├── idGenerator.py       # Generates continuous packet IDs (thread-safe)
│   │   └── logger.py            # Logs system operations with timestamps
│   │
│   └── schemas/                 # (Reserved for Pydantic models if needed later)
│
├── tests/
│   └── testPacketCapture.py     # (Optional) for future unit testing
│
├── requirements.txt             # Python dependencies
├── .env                         # Environment configuration file
└── README.md                    # Documentation
```

---

## System Overview

### 1. Packet Capture Flow

1. The frontend dashboard sends a `POST /api/packets/start` request.  
2. `packetSniffer.py` launches Scapy’s live capture thread and begins sniffing sequentially.  
3. Each packet triggers the `parsePacket()` function:
   - Extracts metadata (source, destination, protocol, length, timestamp)
   - Converts it into features via `featureExtractor.py`
   - Sends those features into the ML layer
   - Returns a structured JSON entry including `"risk": "LOW"` or `"HIGH"`
4. Captured packets are stored in memory and can be fetched through `GET /api/packets/latest`.

### 2. API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/api/packets/start` | `POST` | Starts live packet capture |
| `/api/packets/stop` | `POST` | Stops packet capture |
| `/api/packets/latest` | `GET` | Retrieves recent packets with metadata and risk |
| `/api/packets/reset` | `DELETE` | Clears all captured data and resets state |
| `/api/packets/status` | `GET` | Returns sniffer state and packet count |

---

## Installation and Setup

### Step 1: Create a Virtual Environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate  # on Linux/macOS
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Server
```bash
uvicorn app.main:app --reload
```

Server will start on:
```
http://127.0.0.1:8000
```

---

## Dependencies

| Library | Purpose |
|----------|----------|
| FastAPI | Web framework for backend REST APIs |
| Uvicorn | ASGI server for FastAPI |
| Scapy | Low-level packet capture and inspection |
| Pydantic | Data validation and serialization |
| python-dotenv | (Optional) Environment variable loading |

Install them manually if needed:
```bash
pip install fastapi uvicorn scapy pydantic python-dotenv
```

---

## Machine Learning Integration

The backend includes a model interface system designed for easy ML integration.

### Current Components
- `modelStub.py` — Simulates ML predictions randomly (for testing)
- `featureExtractor.py` — Converts packets to model-ready input
- `modelInterface.py` — Provides an abstract base class and handler

### To Add a Real Model

1. Train your model externally (for example, using scikit-learn or TensorFlow).
2. Save it (for example, using `joblib` or `torch.save`).
3. Create a new file in `/ml` (for example, `realModel.py`) implementing:

```python
from app.ml.modelInterface import BaseModelInterface
import joblib

class RealRiskModel(BaseModelInterface):
    def __init__(self):
        self.model = None
        self.modelLoaded = False

    def loadModel(self, modelPath: str) -> None:
        self.model = joblib.load(modelPath)
        self.modelLoaded = True

    def predict(self, features: dict) -> str:
        result = self.model.predict([list(features.values())])[0]
        return "HIGH" if result == 1 else "LOW"
```

4. Update `packetParser.py`:
```python
from app.ml.realModel import RealRiskModel
classifier = RealRiskModel()
classifier.loadModel("path/to/your/trained_model.pkl")
```

After this update, the backend will automatically serve ML-based predictions to the frontend.

---

## Logging

All runtime logs are stored under:
```
backend/logs/
```

Log files are automatically created per module (for example, `packet_sniffer.log`)  
and contain timestamps, severity levels, and event messages.

---

## Frontend Integration

The React frontend communicates with this backend via these endpoints:
```
http://127.0.0.1:8000/api/packets/start
http://127.0.0.1:8000/api/packets/stop
http://127.0.0.1:8000/api/packets/latest
http://127.0.0.1:8000/api/packets/reset
```

Ensure both frontend and backend are running concurrently.  
Your frontend (`Dashboard.tsx`) expects the following packet structure:
```json
{
  "id": 1,
  "source": "192.168.0.1",
  "destination": "192.168.0.2",
  "protocol": "TCP",
  "length": 128,
  "timestamp": "14:52:10",
  "risk": "HIGH"
}
```

---

## Development Notes

- Run the backend with `--reload` for automatic updates during development.
- The capture thread uses Scapy in a non-blocking daemon mode.
- Risk labels are currently randomized; replace them with trained model outputs.
- Administrative privileges (Windows) or `sudo` (Linux) are required for live packet sniffing.

---

## Authors

- Anubhav Gupta — Backend Development and Architecture Design and ML Model Integration and Risk Classification

---

## Summary

- Real-time packet capture  
- Sequential ID generation  
- Structured logging and diagnostics  
- REST API for frontend integration  
- Modular ML-ready backend architecture

This backend is now fully operational and prepared for integration with a trained machine learning model.
