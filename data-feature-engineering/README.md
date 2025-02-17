# Project Folder (data-feature-engineering) Instructions

This repository contains Jupyter Notebook files for analyzing and managing data related to the project. Below are the steps to run the notebooks in the correct order and ensure a smooth workflow.

## Prerequisites
Before running the notebooks, make sure you have the following:
1. **AWS Credentials**:
   - Ensure your AWS credentials are configured on your local machine or in your environment (e.g., using the `~/.aws/credentials` file).
2. **Python Environment**:
   - Python 3.8 or higher is recommended.
   - Required packages:
     - `boto3`
     - `sagemaker`
     - `pandas`
     - `awswrangler`
     - `matplotlib`
     - `seaborn`
   - Install missing packages using:
     ```bash
     pip install -r requirements.txt
     ```
3. **Jupyter Notebook**:
   - Ensure Jupyter is installed and can run `.ipynb` files.

## Running the Notebooks

Follow these steps to execute the workflow:

### 1. **Initialize S3 Environment**
   - Open and run the `s3_init.ipynb` notebook.
   - This notebook sets up the connection to AWS S3 and prepares the environment for accessing the necessary data files.
   - Ensure that the required S3 buckets and file paths are correctly configured.

   **Command to Start Notebook**:
   ```bash
   jupyter notebook s3_init.ipynb
   ```

### 2. **Data Exploration**
   - Open and run the `data_exploration.ipynb` notebook.
   - This notebook performs data quality checks, including:
     - Checking for missing values.
     - Analyzing feature distributions.
     - Calculating correlations between features.
   - The output of this step is critical for understanding the dataset and preparing for further analysis.

   **Command to Start Notebook**:
   ```bash
   jupyter notebook data_exploration.ipynb
   ```

### 3. **Initialize Athena Environment**
   - Open and run the `athena_init.ipynb` notebook.
   - This notebook configures the connection to AWS Athena and initializes queries for analyzing data directly from the Athena database.
   - Ensure that your Athena database, tables, and query paths are correctly set up.

   **Command to Start Notebook**:
   ```bash
   jupyter notebook athena_init.ipynb
   ```

### 4. **Initialize Feature Store**
- Open and run the `feature_store_init.ipynb` notebook.
- Stores structured feature data in Amazon SageMaker Feature Store
- Enables versioning and governance for machine learning features
- Provides a queryable offline feature store via AWS Athena
- Ensures feature consistency across training and inference pipelines
- Automates data ingestion, validation, and retrieval for future use
## Notes
- **Execution Order**:
  The notebooks must be executed in the following order to ensure all dependencies are met:
  1. `s3_init.ipynb`
  2. `data_exploration.ipynb`
  3. `athena_init.ipynb`
  4. `feature_store_init.ipynb`

- **Troubleshooting**:
  - If you encounter any issues with AWS connections, verify your AWS credentials and ensure you have the necessary permissions for S3 and Athena.
  - For missing Python packages, use the `pip install` command to install them.
