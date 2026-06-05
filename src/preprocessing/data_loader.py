import pandas as pd


def load_data(file_path):

    """
    Load dataset from CSV file
    """

    df = pd.read_csv(file_path)

    return df


if __name__ == "__main__":

    # Dataset Path
    file_path = r"C:\Projects\EduShield_AI\data\raw\student_dropout_dataset_v3.csv"


    # Load Dataset
    df = load_data(file_path)
    print(df["Dropout"].value_counts())


    print("\n==============================")
    print("DATASET LOADED SUCCESSFULLY")
    print("==============================\n")


    # First 5 Rows
    print("FIRST 5 ROWS:\n")
    print(df.head())


    # Dataset Shape
    print("\n==============================")
    print("DATASET SHAPE")
    print("==============================")
    print(df.shape)


    # Column Names
    print("\n==============================")
    print("COLUMN NAMES")
    print("==============================")
    print(df.columns.tolist())


    # Data Types
    print("\n==============================")
    print("DATA TYPES")
    print("==============================")
    print(df.dtypes)


    # Missing Values
    print("\n==============================")
    print("MISSING VALUES")
    print("==============================")
    print(df.isnull().sum())


    # Duplicate Values
    print("\n==============================")
    print("DUPLICATE ROWS")
    print("==============================")
    print(df.duplicated().sum())


    # Dataset Info
    print("\n==============================")
    print("DATASET INFO")
    print("==============================")
    print(df.info())