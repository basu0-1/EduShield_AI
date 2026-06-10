import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.impute import SimpleImputer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from model_config import (
    DATA_PATH,
    TARGET_COLUMN,
    RANDOM_STATE,
    TEST_SIZE
)
from xgboost import XGBClassifier

# LOAD DATA
df = pd.read_csv(DATA_PATH)

print("\nDataset Loaded Successfully")

# FEATURES AND TARGET
X = df.drop(columns=[TARGET_COLUMN])

y = df[TARGET_COLUMN]

# IDENTIFY FEATURE TYPES
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

        (
            "imputer",
            SimpleImputer(strategy="median")
        ),

        (
            "scaler",
            StandardScaler()
        )

    ]

)

categorical_transformer = Pipeline(

    steps=[

        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),

        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore")
        )

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
# SPLIT DATA
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=TEST_SIZE,

    random_state=RANDOM_STATE,

    stratify=y

)


# --------------------------------------------------
# PREPROCESS DATA
# --------------------------------------------------

X_train_processed = preprocessor.fit_transform(X_train)

X_test_processed = preprocessor.transform(X_test)

print("\nPreprocessing Completed")


# --------------------------------------------------
# MODELS
# --------------------------------------------------

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000,
            random_state=RANDOM_STATE
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE
        ),

    "XGBoost":
        XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            eval_metric="logloss"
        )
}


# --------------------------------------------------
# TRAINING LOOP
# --------------------------------------------------

results = {}

best_model = None

best_score = 0

best_model_name = ""


for model_name, model in models.items():

    print(f"\nTraining {model_name}...")

    model.fit(
        X_train_processed,
        y_train
    )

    predictions = model.predict(
        X_test_processed
    )

    probabilities = model.predict_proba(
        X_test_processed
    )[:, 1]

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

    results[model_name] = {

        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC AUC": roc_auc

    }

    print(results[model_name])

    if roc_auc > best_score:

        best_score = roc_auc

        best_model = model

        best_model_name = model_name


# --------------------------------------------------
# SAVE BEST MODEL
# --------------------------------------------------

joblib.dump(
    best_model,
    "models/best_model.pkl"
)

joblib.dump(
    preprocessor,
    "models/preprocessor.pkl"
)


print("\n===================================")
print("BEST MODEL")
print("===================================")

print(best_model_name)

print(f"ROC AUC: {best_score:.4f}")

print("\nModel Saved Successfully")
