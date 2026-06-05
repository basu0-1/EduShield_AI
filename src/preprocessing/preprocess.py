'''clean data,
handle missing values,
encode categories,
scale numerical values,
split train/test data,
save preprocessing pipeline.'''
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

from config import (
    DATA_PATH,
    TARGET_COLUMN,
    DROP_COLUMNS,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES
)


# Load Dataset
df = pd.read_csv(DATA_PATH)


print("\nDataset Loaded Successfully")


# Remove Unnecessary Columns
existing_drop_columns = [

    col for col in DROP_COLUMNS
    if col in df.columns

]

df = df.drop(columns=existing_drop_columns)


print("\nDropped Unnecessary Columns")


# Split Features and Target
X = df.drop(columns=[TARGET_COLUMN])

y = df[TARGET_COLUMN]


print("\nSeparated Features and Target")


# Numerical Pipeline
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


# Categorical Pipeline
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


# Full Preprocessing Pipeline
preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            numeric_transformer,
            NUMERICAL_FEATURES
        ),

        (
            "cat",
            categorical_transformer,
            CATEGORICAL_FEATURES
        )

    ]

)


print("\nPreprocessing Pipeline Created")


# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)


print("\nTrain-Test Split Completed")


# Fit and Transform Training Data
X_train_processed = preprocessor.fit_transform(X_train)


# Transform Testing Data
X_test_processed = preprocessor.transform(X_test)


print("\nData Preprocessing Completed")


# Save Preprocessor
joblib.dump(
    preprocessor,
    "models/preprocessor.pkl"
)


print("\nPreprocessor Saved Successfully")


# Final Shapes
print("\nTraining Data Shape:")
print(X_train_processed.shape)

print("\nTesting Data Shape:")
print(X_test_processed.shape)