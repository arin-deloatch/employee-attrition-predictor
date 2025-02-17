import pandas as pd
import os

# Ensure training data exists
def test_data_existence():
    assert os.path.exists("data-feature-engineering/train.csv"), "Train data is missing"
    assert os.path.exists("data-feature-engineering/test.csv"), "Test data is missing"

# Validate dataset integrity
def test_data_integrity():
    df = pd.read_csv("data-feature-engineering/train.csv")
    assert df.isnull().sum().max() == 0, "Dataset contains missing values"
    assert len(df) > 1000, "Dataset is too small"

if __name__ == "__main__":
    test_data_existence()
    test_data_integrity()
    print("All tests passed!")
