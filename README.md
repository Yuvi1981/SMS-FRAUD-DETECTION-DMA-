# SMS-FRAUD-DETECTION-DMA-
## End-to-End SMS Spam Classification, Explainability & Volume Forecasting System
### Data Mining & Analytics (DMA) Mini Project — JSPM's RSCOE

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/Academic-Project-purple.svg)]()

A comprehensive, production-grade machine learning and text analytics platform that detects SMS smishing/spam attacks and forecasts daily message traffic. The project features a modern **React + Tailwind** dashboard backed by **FastAPI**, an alternate **Streamlit** dashboard, pre-trained scikit-learn models, and a formal **8-page academic mini-project report** (`.docx` & `.pdf`).

---

## 📑 Table of Contents
1. [Key Highlights & Results](#-key-highlights--results)
2. [Architectures & Methodology](#-architectures--methodology)
3. [Running the Application](#-running-the-application)
   - [Option A: Full-Stack React + FastAPI Dashboard (Recommended)](#option-a-full-stack-react--fastapi-dashboard-recommended)
   - [Option B: Classic Streamlit Dashboard](#option-b-classic-streamlit-dashboard)
4. [Academic Mini-Project Report (8 Pages)](#-academic-mini-project-report-8-pages)
5. [Repository Structure](#-repository-structure)
6. [Dashboard Views & Features](#-dashboard-views--features)
7. [Simulated Timestamps Notice](#-simulated-timestamps-notice)
8. [Reproducibility & Verification](#-reproducibility--verification)

---

## 📊 Key Highlights & Results

Trained and evaluated on the **UCI SMS Spam Collection** (5,169 unique, deduplicated messages: 4,516 legitimate / 653 spam) partitioned via a strict stratified 80/20 train/test split (1,034 test messages) with zero data leakage.

| Model Architecture | Accuracy | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Latency (1k queries) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (L2 Balanced)** | **0.9913** | **0.9766** | **0.9542** | **0.9653** | **0.9971** | **0.9878** | **1.18 ms** | 🏆 **Champion** |
| **Multinomial Naive Bayes ($\alpha=0.1$)** | 0.9845 | 0.9600 | 0.9160 | 0.9375 | 0.9954 | 0.9830 | 1.64 ms | Runner-Up |
| **k-Nearest Neighbors ($k=5$, distance)** | 0.9758 | 0.9569 | 0.8473 | 0.8988 | 0.9869 | 0.9665 | 191.13 ms | Baseline |
| **Bayesian Network (TAN / Naive)** | 0.9758 | 0.9569 | 0.8473 | 0.8988 | 0.9791 | 0.9380 | 261.57 ms | Baseline |

### 🔍 Odds Ratio ($e^\beta$) Interpretability
- **Top Spam Drivers:** `phonetoken` ($512,955\times$), `urltoken` ($29,465\times$), `moneytoken` ($9,231\times$), `claim` ($58.27\times$), `prize` ($42.1\times$).
- **Top Ham Drivers:** `ok` ($0.04\times$), `home` ($0.09\times$).

### 📈 Daily Volume Forecasting (30-Day Holdout)
- **ARIMA(1,1,1):** MAE `2.48`, RMSE `2.98`, **MAPE `12.11%`** (outperforming Seasonal Naive baseline at 23.80% MAPE).

---

## 🛠️ Running the Application

### Option A: Full-Stack React + FastAPI Dashboard (Recommended)

1. **Install Python backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI backend server (Port 8000):**
   ```bash
   cd backend
   python -m uvicorn server:app --host 127.0.0.1 --port 8000
   ```
   *Health Check:* `http://localhost:8000/api/status`  
   *Swagger Docs:* `http://localhost:8000/docs`

3. **Install frontend dependencies and launch Vite (Port 5173):**
   ```bash
   npm install
   npx vite --port 5173 --host
   ```
   *Access the web app:* **`http://localhost:5173`**

---

### Option B: Classic Streamlit Dashboard

If you prefer running the single-process Streamlit interface:
```bash
pip install -r app/requirements.txt
streamlit run app/main.py
```
*Access Streamlit at:* `http://localhost:8501`

---

## 📄 Academic Mini-Project Report (8 Pages)

A complete, formal academic report has been authored and formatted to **exactly 8 pages** following the institutional guidelines of JSPM's Rajarshi Shahu College of Engineering (RSCOE), Pune:

- **Word Document:** [`report/DMA_Mini_Project_Report_Filled.docx`](report/DMA_Mini_Project_Report_Filled.docx)
- **Exported PDF:** [`report/DMA_Mini_Project_Report_Filled.pdf`](report/DMA_Mini_Project_Report_Filled.pdf)
- **Page Previews:** [`report/pdf_pages/`](report/pdf_pages/) (`page_1.png` through `page_8.png`)

```
Page 1: Institutional Cover (JSPM RSCOE, Title, Student Name, Roll No 09, Div TY Div C-1)
Page 2: Table of Contents (10 Numbered Headings Intact)
Page 3: 1. Title, 2. Abstract, 3. Introduction, 4. Problem Statement, 5. Objectives
Page 4: 6. Dataset & Libraries Required (Tables 1 & 2), 7. Approach / Methodology
Page 5: 8. Implementation (Hyperparameters & 4 Code Listings)
Page 6: 9. Results (Part 1: Model Comparison Table 3, ROC Curve Fig 1, Confusion Matrix Fig 2)
Page 7: 9. Results (Part 2: Odds Ratios Table 4, Bayesian DAG Fig 3 & Table 5, ARIMA Forecast Fig 4 & Table 6)
Page 8: 10. Conclusion (Champion Selection Rationale, Insights, Simulated Dates Notice, Future Scope)
```

---

## 📁 Repository Structure

```
SMS-FRAUD-DETECTION-DMA-/
├── backend/
│   └── server.py                       # FastAPI REST API serving models & analytics
├── src/                                # React 18 + TypeScript + Tailwind UI
│   ├── components/                     # Layout, Sidebar, KPI cards, Charts
│   ├── views/                          # 7 Feature Views (Overview, LivePred, EDA, etc.)
│   ├── services/api.ts                 # Type-safe Axios client connecting to FastAPI
│   └── App.tsx                         # Master routing & dashboard layout
├── app/                                # Standalone Streamlit application
│   ├── main.py                         # Streamlit dashboard entrypoint
│   ├── components.py                   # Streamlit UI cards, badges & charts
│   └── theme.py                        # Streamlit color tokens & CSS
├── data/
│   ├── raw/SMSSpamCollection           # Raw UCI SMS dataset
│   └── processed/                      # Preprocessed, train/test splits & daily counts
├── outputs/
│   ├── models/                         # Serialized joblib models (LR, NB, k-NN, vectorizers)
│   ├── tables/                         # Evaluation tables (model_comparison.csv, odds ratios)
│   ├── figures/                        # High-resolution ROC curves, confusion matrices, DAG
│   └── ui_screenshots/                 # Automated test screenshots of all 7 features
├── report/
│   ├── DMA_Mini_Project_Report_Filled.docx  # 8-page academic report
│   ├── DMA_Mini_Project_Report_Filled.pdf   # Verified 8-page PDF export
│   └── pdf_pages/                          # Page-by-page rendering images (pages 1-8)
├── scripts/
│   ├── fill_report.py                  # Automated 8-page DOCX & PDF generation script
│   ├── verify_features_interactive.py  # Selenium headless E2E verification test suite
│   └── generate_artifacts.py           # ML training, cross-validation & artifact generation
├── requirements.txt                    # Python environment dependencies
├── package.json                        # Node.js dependencies
├── tailwind.config.js                  # Tailwind design system configuration
└── vite.config.ts                      # Vite build tool configuration
```

---

## 🖥️ Dashboard Views & Features

1. **Overview Dashboard:** Total corpus counts (5,169 SMS), spam prevalence rate (12.63%), champion F1 (`0.9653`), class balance donut chart, and 5-stage ML pipeline sequence.
2. **Live Prediction & Explainability:** Interactive text classifier with one-click presets, probability meters, odds-ratio keyword chips explaining *why* the model decided, and 3-model side-by-side consensus.
3. **Exploratory Data Analysis (EDA):** Character length and word count distributions, class summary statistics, top Chi-square discriminators, and searchable/filterable corpus explorer.
4. **Model Benchmark:** Dynamic metric switching (Accuracy, Precision, Recall, F1, ROC-AUC), interactive comparison bar charts, and champion selection rationale.
5. **Word Insights & Odds Ratios:** Real-time token lookup card displaying coefficient $\beta$ and odds multiplier $e^\beta$, alongside dual tables for top spam and ham drivers.
6. **Bayesian Network:** Interactive Directed Acyclic Graph (DAG) with clickable scenario presets (*Urgent Financial Bait*, *Clean Conversational*) and real-time belief updating $P(\text{Spam} \mid \mathbf{e})$.
7. **Volume Forecast & Time Series:** 365-day daily spam volume series, 7d/14d moving average smoothing toggles, 30-day ARIMA(1,1,1) holdout forecast with 95% confidence bands, and residual diagnostics.

---

## ⚠️ Simulated Timestamps Notice

Neither the UCI SMS Spam Collection nor related SMS corpora include real calendar timestamps. In strict accordance with the project specification:
- Timestamps and daily message volumes are **SIMULATED** using a base level, mild annual growth trend, weekly seasonality (lower volume on weekends), and Gaussian noise.
- This is explicitly documented with alert banners throughout the dashboard, in the project report, and in experimental evaluation tables.

---

## 🧪 Reproducibility & Verification

To re-run the complete model training, evaluation, and artifact generation from scratch:
```bash
python scripts/generate_artifacts.py
```

To run the interactive headless browser verification across all 7 dashboard features:
```bash
python scripts/verify_features_interactive.py
```

To re-build and export the exact 8-page academic report:
```bash
python scripts/fill_report.py
```

---

## 👤 Author
- **Student Name:** Yuvraj Kadam (RBT24CS150)
- **Roll No:** 09
- **Class / Division:** TY Div C-1
- **Course:** Data Mining & Analytics (DMA)
- **Institution:** JSPM's Rajarshi Shahu College of Engineering, Tathawade, Pune
- **Academic Year:** 2026-27 (Semester-I)
