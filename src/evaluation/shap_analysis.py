import os
import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

# --------------------------------------------------
# CREATE OUTPUT DIRECTORY
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
# FEATURES AND TARGET
# --------------------------------------------------

X = df.drop(columns=["Dropout"])

y = df["Dropout"]

# --------------------------------------------------
# FEATURE LISTS
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
# SPLIT
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
# FEATURE NAMES
# --------------------------------------------------

encoded_features = preprocessor.named_transformers_[
    "cat"
].named_steps[
    "encoder"
].get_feature_names_out(
    categorical_features
)

feature_names = (
    numerical_features
    + list(encoded_features)
)

# --------------------------------------------------
# SHAP EXPLAINER
# --------------------------------------------------

explainer = shap.Explainer(
    model,
    X_train_processed
)

print("\nSHAP Explainer Created")

# --------------------------------------------------
# SHAP VALUES
# --------------------------------------------------

sample_data = X_test_processed[:500]

shap_values = explainer(sample_data)

print("\nSHAP Values Generated")

# --------------------------------------------------
# SHAP SUMMARY PLOT
# --------------------------------------------------

plt.figure()

shap.summary_plot(
    shap_values,
    sample_data,
    feature_names=feature_names,
    show=False
)

plt.savefig(
    "reports/figures/shap_summary.png",
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# SHAP BAR PLOT
# --------------------------------------------------

plt.figure()

shap.plots.bar(
    shap_values,
    show=False
)

plt.savefig(
    "reports/figures/shap_bar.png",
    bbox_inches="tight"
)

plt.close()

# --------------------------------------------------
# SHAP WATERFALL PLOT
# --------------------------------------------------

plt.figure(figsize=(10, 6))

shap.plots.waterfall(
    shap_values[0],
    show=False
)

plt.savefig(
    "reports/figures/shap_waterfall.png",
    bbox_inches="tight"
)

plt.close()

print("\nSHAP Waterfall Plot Saved")

print("\nSHAP Visualizations Saved Successfully")

print("\nGenerated Files:")
print("reports/figures/shap_summary.png")
print("reports/figures/shap_bar.png")