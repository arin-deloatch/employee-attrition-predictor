import pandas as pd
import os

# Get the absolute path to the `data-feature-engineering` directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up one level
DATA_DIR = os.path.join(BASE_DIR, "data-feature-engineering")

# Ensure training and test data exist
def test_data_existence():
    train_path = os.path.join(DATA_DIR, "train.csv")
    test_path = os.path.join(DATA_DIR, "test.csv")

    assert os.path.exists(train_path), f"❌ Train data is missing at {train_path}!"
    assert os.path.exists(test_path), f"❌ Test data is missing at {test_path}!"
    
    print("✅ Data existence check passed.")

# Validate dataset integrity
def test_data_integrity():
    train_path = os.path.join(DATA_DIR, "train.csv")
    df = pd.read_csv(train_path)

    # Check for missing values
    assert df.isnull().sum().max() == 0, "❌ Dataset contains missing values!"

    # Ensure the dataset is large enough
    assert len(df) > 1000, f"❌ Dataset is too small! Found only {len(df)} rows."

    # Check for duplicate rows
    assert df.duplicated().sum() == 0, "❌ Dataset contains duplicate rows!"

    # Ensure all columns have consistent data types
    assert df.dtypes.nunique() > 1, "❌ Dataset may have incorrect column data types!"

    print("✅ Data integrity check passed.")

# Run all tests
if __name__ == "__main__":
    try:
        test_data_existence()
        test_data_integrity()
        print("✅ All tests passed!")
    except AssertionError as e:
        print(e)
        exit(1)  # Exit with an error code if tests fail
