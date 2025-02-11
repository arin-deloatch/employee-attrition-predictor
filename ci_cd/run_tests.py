import unittest
import pandas as pd

class TestFeatureEngineering(unittest.TestCase):
    def test_data_shape(self):
        df = pd.read_csv("data-feature-engineering/data.csv")
        self.assertGreater(df.shape[0], 0, "Dataset should not be empty")

    def test_missing_values(self):
        df = pd.read_csv("data-feature-engineering/data.csv")
        self.assertFalse(df.isnull().sum().sum() > 0, "Dataset should not have missing values")

if __name__ == '__main__':
    unittest.main()
