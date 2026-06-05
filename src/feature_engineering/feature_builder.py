import pandas as pd
import numpy as np

# Load Dataset
DATA_PATH = r"C:\Projects\EduShield_AI\data\raw\student_dropout_dataset_v3.csv"

df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully")


# --------------------------------------------------
# Handle Missing Values
# --------------------------------------------------

df["Family_Income"] = df["Family_Income"].fillna(
    df["Family_Income"].median()
)

df["Study_Hours_per_Day"] = df["Study_Hours_per_Day"].fillna(
    df["Study_Hours_per_Day"].median()
)

df["Stress_Index"] = df["Stress_Index"].fillna(
    df["Stress_Index"].median()
)

df["Parental_Education"] = df["Parental_Education"].fillna(
    df["Parental_Education"].mode()[0]
)

print("Missing Values Handled")


# --------------------------------------------------
# FEATURE 1
# Student Pressure Index
# --------------------------------------------------

df["Student_Pressure_Index"] = (
    df["Stress_Index"]
    * df["Assignment_Delay_Days"]
) / (
    df["Study_Hours_per_Day"] + 1
)


# --------------------------------------------------
# FEATURE 2
# Academic Risk Score
# --------------------------------------------------

df["Academic_Risk_Score"] = (
    (100 - df["Attendance_Rate"])
    + ((4 - df["GPA"]) * 10)
)


# --------------------------------------------------
# FEATURE 3
# Income Stress Ratio
# --------------------------------------------------

df["Income_Stress_Ratio"] = (
    df["Stress_Index"]
    / (df["Family_Income"] + 1)
)


# --------------------------------------------------
# FEATURE 4
# GPA Consistency Score
# --------------------------------------------------

df["GPA_Consistency_Score"] = abs(
    df["GPA"]
    - df["Semester_GPA"]
)


# --------------------------------------------------
# FEATURE 5
# Attendance Efficiency
# --------------------------------------------------

df["Attendance_Efficiency"] = (
    df["Attendance_Rate"]
    / (df["Travel_Time_Minutes"] + 1)
)


# --------------------------------------------------
# FEATURE 6
# Study Efficiency Score
# --------------------------------------------------

df["Study_Efficiency_Score"] = (
    df["GPA"]
    / (df["Study_Hours_per_Day"] + 1)
)


# --------------------------------------------------
# FEATURE 7
# Financial Risk Indicator
# --------------------------------------------------

df["Financial_Risk_Indicator"] = (
    1 / (df["Family_Income"] + 1)
) * 100000


# --------------------------------------------------
# FEATURE 8
# Academic Momentum
# --------------------------------------------------

df["Academic_Momentum"] = (
    df["Semester_GPA"]
    - df["CGPA"]
)


# --------------------------------------------------
# FEATURE 9
# Attendance Risk Index
# --------------------------------------------------

df["Attendance_Risk_Index"] = (
    100 - df["Attendance_Rate"]
)


# --------------------------------------------------
# FEATURE 10
# Stress Burden Score
# --------------------------------------------------

df["Stress_Burden_Score"] = (
    df["Stress_Index"]
    * (100 - df["Attendance_Rate"])
)


print("\nFeature Engineering Completed")


print("\nNew Features Created:")

new_features = [
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

for feature in new_features:
    print(feature)


# --------------------------------------------------
# Save Processed Dataset
# --------------------------------------------------

OUTPUT_PATH = r"C:\Projects\EduShield_AI\data\processed\student_dropout_featured.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nFeature Engineered Dataset Saved Successfully")

print("\nDataset Shape:")
print(df.shape)