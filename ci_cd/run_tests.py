import pandas as pd
import os

# Ensure training and test data exist
def test_data_existence():
    assert os.path.exists("data-feature-engineering/train.csv"), "❌ Train data is missing!"
    assert os.path.exists("data-feature-engineering/test.csv"), "❌ Test data is missing!"
    print("✅ Data existence check passed.")

# Validate dataset integrity
def test_data_integrity():
    df = pd.read_csv("data-feature-engineering/train.csv")

    # Check for missing values
    assert df.isnull().sum().max() == 0, "❌ Dataset contains missing values!"

    # Ensure the dataset is large enough
    assert len(df) > 1000, "❌ Dataset is too small!"

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
