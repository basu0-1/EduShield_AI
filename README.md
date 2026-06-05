<div align="center">

# 🎓 EduShield AI

### AI-Powered Student Dropout Prediction & Early Warning System

Predict • Explain • Intervene • Retain

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![SHAP](https://img.shields.io/badge/SHAP-ExplainableAI-green)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

---

## 📌 Project Overview

EduShield AI is an intelligent Early Warning System that identifies students at risk of dropping out using Machine Learning and Explainable AI.

The system helps educational institutions:

- 🎯 Detect at-risk students early
- 📊 Analyze academic and behavioral factors
- 🧠 Understand model decisions using SHAP
- 💡 Generate intervention recommendations
- 📈 Improve student retention rates

---

## 🚀 Key Features

### 📦 Data Pipeline

✔ Data Loading  
✔ Data Cleaning  
✔ Missing Value Handling  
✔ Data Preprocessing

---

### ⚙ Feature Engineering

Custom Features:

| Feature | Purpose |
|----------|----------|
| Student Pressure Index | Academic pressure measurement |
| Academic Risk Score | Overall academic risk |
| Income Stress Ratio | Financial stress indicator |
| GPA Consistency Score | GPA stability |
| Attendance Efficiency | Attendance performance |
| Study Efficiency Score | Productivity score |
| Financial Risk Indicator | Financial vulnerability |
| Academic Momentum | Performance trend |
| Attendance Risk Index | Attendance-based risk |
| Stress Burden Score | Combined stress impact |

---

### 🤖 Machine Learning

Models Implemented:

- Logistic Regression
- Random Forest

🏆 Best Model:

```text
Logistic Regression
ROC AUC = 0.8203
```

---

## 📈 Model Performance

| Metric | Score |
|----------|----------|
| Accuracy | 81.4% |
| Precision | 67.2% |
| Recall | 40.9% |
| F1 Score | 50.9% |
| ROC AUC | 82.0% |

---

## 🧠 Explainable AI

Implemented using SHAP

Features:

✔ SHAP Summary Plot

✔ SHAP Feature Importance

✔ SHAP Waterfall Plot

Provides transparency into model predictions.

---

## 🖥 Dashboard Modules

### 🏠 Home Page

- Project Overview
- Navigation System

### 🎯 Prediction Page

- Student Information Form
- Risk Prediction
- Risk Gauge
- Recommendations

### 📊 Analytics Page

- KPI Cards
- Dropout Distribution
- Department-wise Analysis

---

## 🏗 Project Architecture

```text
Student Dataset
        │
        ▼
Data Preprocessing
        │
        ▼
Feature Engineering
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Explainable AI (SHAP)
        │
        ▼
Streamlit Dashboard
        │
        ▼
Early Intervention Recommendations
```

---

## 📂 Project Structure

```text
EduShield_AI

├── data
│   ├── raw
│   └── processed
│
├── models
│   ├── best_model.pkl
│   └── preprocessor.pkl
│
├── reports
│   └── figures
│
├── src
│   ├── preprocessing
│   ├── features
│   ├── training
│   ├── evaluation
│   ├── explainability
│   └── dashboard
│
├── app.py
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

### Programming

- Python

### Machine Learning

- Scikit-learn
- Pandas
- NumPy

### Visualization

- Plotly
- Matplotlib
- Seaborn

### Explainability

- SHAP

### Dashboard

- Streamlit

---

## ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/EduShield_AI.git
```

### Move Into Project

```bash
cd EduShield_AI
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Dashboard

```bash
streamlit run app.py
```

---

## 🎯 Future Scope

- 📄 PDF Risk Reports
- 📤 Batch Prediction
- 📧 Email Alert System
- ☁ Cloud Deployment
- 📱 Mobile Dashboard
- 🔔 Real-Time Notifications

---

## 👨‍💻 Developer

**BASUMATI PRADHAN**

AI-Powered Student Retention & Early Warning System

---

## ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the project

🚀 Share with others
