# RetainAI: Employee Retention Intelligence
A machine learning project to predict employee attrition using historical HR data. The model analyzes key factors such as job satisfaction, performance, and compensation to identify employees at risk of leaving, helping organizations take proactive retention measures.

## Background

Employee attrition is a critical challenge for organizations, as losing valuable talent impacts productivity, team morale, and recruitment costs. This project aims to develop a predictive model to identify employees at risk of leaving the company, enabling HR teams to take proactive retention measures. By analyzing various employee-related factors, such as job satisfaction, performance metrics, work-life balance, and compensation, the model will predict whether an employee is likely to leave the organization or stay.

The objective of the model is to accurately classify employee attrition as a binary classification problem. This is a supervised machine learning task, where the model is trained using labeled historical data containing various employee attributes and their attrition status. The project focuses on building a reliable, explainable solution that can assist HR departments in identifying high-risk employees and addressing potential concerns before attrition occurs, ultimately improving organizational stability and employee satisfaction.

The employee attrition prediction model will be evaluated using both business use cases and model performance metrics. From a business perspective, the model’s success will be determined by its ability to accurately identify employees who are likely to leave, enabling HR teams to take timely actions. The primary evaluation metrics will include accuracy, precision, recall, and the F1-score, with a focus on recall to ensure that the model minimizes false negatives (employees who are at risk but not flagged by the model).

The data source is the [Employee Attrition Dataset](https://www.kaggle.com/datasets/stealthtechnologies/employee-attrition-dataset/data?select=train.csv) from Kaggle, which includes a variety of features such as demographic details, job roles, performance metrics, and compensation. The dataset requires data preparation steps such as handling missing values, encoding categorical variables, and normalizing numerical features. Exploratory data analysis will involve identifying patterns and correlations in the data to understand the key drivers of attrition. Based on the data, it is hypothesized that features like job satisfaction, monthly income, years at the company, work-life balance, and overtime status will be significant predictors of attrition. A random forest classifier will be used initially due to its robustness in handling both categorical and numerical data. Additionally, other models, such as logistic regression, gradient boosting machines, support vector machines, and neural networks, will be explored to compare performance.


## Sagemaker Setup 

1. Run AWS Sagemaker Studio 

2. Setup your github credentials, for example by [adding new SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

3. Clone this repository: 

```bash
git clone git@github.com:arin-deloatch/employee-attrition-predictor.git
```

4. Run dependencies and S3 bucket setup in `data-feature-engineering/s3_init.ipynb` 

5. Run Athena setup in `data-feature-engineering/athena_init.ipynb`