# Real Estate Intelligence & AI Decision Engine — System Architecture

## 1. Overview
The platform connects classical Business Intelligence with modern Supervised & Unsupervised Machine Learning, Forecasting, and a Generative AI Layer.

## 2. Directory Taxonomy
- `learning/`: Personal sandbox for manual practice and algorithm learning.
- `real_estate_intelligence_dataset/`: Raw immutable data, processed tables, and ML-ready matrices.
- `ml/`: Production Machine Learning engine.
  - `supervised/`: Regression (Property Pricing, Rent Estimation) and Classification (Lead Conversion, Deal Outcome).
  - `unsupervised/`: Clustering (Customer & Market Segmentation) and Dimensionality Reduction.
  - `anomaly_detection/`: Score & Threshold detection engine (Expenses, Maintenance, Pricing).
  - `forecasting/`: Cash flow and time-series forecasting abstraction.
  - `preprocessing/`, `evaluation/`, `tuning/`, `explainability/`, `registry/`: Modular ML lifecycle components.
- `models/`: Trained model serialization directory (`.joblib` / `.onnx` artifacts only).
- `backend/`: REST API, schemas, domain services, and ML inference serving.
- `frontend/`: UI Dashboard and interactive visual controls.
- `ai_layer/`: Generative AI, RAG, and multi-agent workflows foundation.
- `tests/`: Automated unit, integration, and ML validation suites.
- `reports/`: Execution checkpoints, SQL validation matrices, and analytical reports.
- `docs/`: Architectural specifications and technical design documents.
