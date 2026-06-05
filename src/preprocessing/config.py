# Dataset Path
DATA_PATH = r"C:\Projects\EduShield_AI\data\raw\student_dropout_dataset_v3.csv"


# Target Column
TARGET_COLUMN = "Dropout"


# Columns To Remove
DROP_COLUMNS = [
    "Student_ID"
]


# Numerical Features
NUMERICAL_FEATURES = [

    "Age",
    "Family_Income",
    "Study_Hours_per_Day",
    "Attendance_Rate",
    "Assignment_Delay_Days",
    "Travel_Time_Minutes",
    "Stress_Index",
    "GPA",
    "Semester_GPA",
    "CGPA"

]


# Categorical Features
CATEGORICAL_FEATURES = [

    "Gender",
    "Internet_Access",
    "Part_Time_Job",
    "Scholarship",
    "Semester",
    "Department",
    "Parental_Education"

]