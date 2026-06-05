import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    precision_recall_curve
)

# --------------------------------------------------
# CREATE FIGURES DIRECTORY
# --------------------------------------------------

os.makedirs(
    "reports/figures",
    exist_ok=True
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_PATH = r"C:\Projects\EduShield_AI\data\processed\student_dropout_featured.csv"

df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully")

# --------------------------------------------------
# FEATURES & TARGET
# --------------------------------------------------

X = df.drop(columns=["Dropout"])

y = df["Dropout"]

# --------------------------------------------------
# FEATURE TYPES
# --------------------------------------------------

numerical_features = [

    "Age",
    "Family_Income",
    "Study_Hours_per_Day",
    "Attendance_Rate",
    "Assignment_Delay_Days",
    "Travel_Time_Minutes",
    "Stress_Index",
    "GPA",
    "Semester_GPA",
    "CGPA",

    "Student_Pressure_Index",
    "Academic_Risk_Score",
    "Income_Stress_Ratio",
    "GPA_Consistency_Score",
    "Attendance_Efficiency",
    "Study_Efficiency_Score",
    "Financial_Risk_Indicator",
    "Academic_Momentum",
    "Attendance_Risk_Index",
    "Stress_Burden_Score"

]

categorical_features = [

    "Gender",
    "Internet_Access",
    "Part_Time_Job",
    "Scholarship",
    "Semester",
    "Department",
    "Parental_Education"

]

# --------------------------------------------------
# PREPROCESSING
# --------------------------------------------------

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numerical_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        )
    ]
)

# --------------------------------------------------
# TRAIN TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)

print("\nPreprocessing Completed")

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(
    "models/best_model.pkl"
)

print("\nBest Model Loaded Successfully")

# --------------------------------------------------
# PREDICTIONS
# --------------------------------------------------

predictions = model.predict(
    X_test_processed
)

probabilities = model.predict_proba(
    X_test_processed
)[:, 1]

# --------------------------------------------------
# METRICS
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions
)

recall = recall_score(
    y_test,
    predictions
)

f1 = f1_score(
    y_test,
    predictions
)

roc_auc = roc_auc_score(
    y_test,
    probabilities
)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("\n===================================")
print("MODEL EVALUATION RESULTS")
print("===================================")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc_auc:.4f}")

# --------------------------------------------------
# CLASSIFICATION REPORT
# --------------------------------------------------

print("\nClassification Report\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# --------------------------------------------------
# CONFUSION MATRIX
# --------------------------------------------------

cm = confusion_matrix(
    y_test,
    predictions
)

print("\nConfusion Matrix\n")

print(cm)

plt.figure(figsize=(6,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig(
    "reports/figures/confusion_matrix.png",
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# ROC CURVE
# --------------------------------------------------

fpr, tpr, _ = roc_curve(
    y_test,
    probabilities
)

plt.figure(figsize=(8,6))

plt.plot(fpr, tpr)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")

plt.savefig(
    "reports/figures/roc_curve.png",
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# PRECISION RECALL CURVE
# --------------------------------------------------

precision_vals, recall_vals, _ = precision_recall_curve(
    y_test,
    probabilities
)

plt.figure(figsize=(8,6))

plt.plot(
    recall_vals,
    precision_vals
)

plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision Recall Curve")

plt.savefig(
    "reports/figures/precision_recall_curve.png",
    bbox_inches="tight"
)

plt.close()

print("\nEvaluation Completed Successfully")

print("\nSaved Files:")
print("reports/figures/confusion_matrix.png")
print("reports/figures/roc_curve.png")
print("reports/figures/precision_recall_curve.png")