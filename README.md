# Intrusion Detection System (IDS)

This repository contains a modular, extensible Intrusion Detection System designed for real-time traffic monitoring, machine-learning based risk scoring, and security analytics. The project includes a backend API, frontend dashboard, and machine learning pipeline trained on CICIDS2017. The system is intended for research, demonstration, and educational purposes.

---

## Overview

The IDS consists of the following major components:

1. **Backend Service**
   A REST API built to process network events, perform risk classification, store logs, and manage alerts. The backend integrates directly with the ML model.

2. **Frontend Dashboard**
   A web-based user interface for visualizing traffic streams, viewing alerts, exploring logs, and interacting with the system in real time.

3. **Machine Learning Module**
   A complete pipeline for preprocessing, training, evaluating, and exporting the risk classification model. It includes Jupyter Notebooks and Python scripts.

4. **Data Layer**
   The system can store and retrieve logs, alerts, and processed events using simple JSON stores, Redis, or other storage options.

---

## Features

* Real-time network traffic monitoring
* Machine learning-based risk assessment
* Low, medium, and high threat classification
* Alerts generated for high-risk events
* Log viewer with search and filtering
* Modular backend API for integration with external systems
* Frontend dashboard for operational monitoring
* CICIDS2017 preprocessing and model training pipeline
* Support for offline batch scoring or real-time ingestion

---

## Repository Structure

Below is the typical directory layout used in this project. Your actual structure may differ slightly.

```
intrusion-detection-system/
│
├── src/
│   ├── backend/               Backend service (API, risk scoring, ingestion)
│   ├── frontend/              UI application (React or similar)
│   ├── ml/                    Notebooks, training scripts, model files
│
├── data/                      Sample traffic or small demo datasets
│
├── docs/                      Architecture and design documentation
│
├── tests/                     Unit and integration tests
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

## Installation

Before running the system, ensure you have the required dependencies installed.

### Backend Setup

```
cd src/backend
python -m venv venv
source venv/bin/activate    (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### Frontend Setup

```
cd src/frontend
npm install
npm run dev
```

---

## Running the System

### Backend

```
python app.py
```

### Frontend

```
npm run dev
```

This will start the backend, the frontend, and any supporting services such as Redis.

---

## Dataset Usage (CICIDS2017)

The CICIDS2017 dataset is not included in the repository due to size constraints.
You can download the dataset from:

[https://www.unb.ca/cic/datasets/nsl.html](https://www.unb.ca/cic/datasets/nsl.html)

Place the raw CSVs in:

```
src/ml/data_raw/
```

Training and preprocessing scripts expect this directory structure.

---

## Machine Learning Pipeline

The ML component includes:

* Data preprocessing scripts
* Notebooks for exploratory data analysis
* Feature engineering
* Model training and evaluation
* Exporting a final trained model (`model.pkl`, `scaler.pkl`)

Training scripts are located in:

```
src/ml/training/
```

Notebooks are stored in:

```
src/ml/notebooks/
```

The final trained model is loaded by the backend at runtime for real-time scoring.

---

## API Endpoints

The backend exposes several REST endpoints. Common examples:

### POST `/api/risk-score`

Submits a single traffic event and returns a risk classification.

### GET `/api/logs`

Retrieves stored log entries.

### GET `/api/alerts`

Returns alerts generated for high-risk traffic.

### POST `/api/ingest`

Ingests raw network traffic data.

More detailed documentation is available in `docs/api_reference.md`.

---

## Logs and Alerts

The backend maintains two data streams:

1. **Logs**
   Includes every processed traffic event, classified with a severity score.

2. **Alerts**
   Contains only high-risk events requiring action.

These streams can be consumed by external services or viewed through the dashboard.

---

## Testing

Run the test suite using:

```
pytest tests/
```

Tests include API validation, model inference checks, and preprocessing unit tests.

---
