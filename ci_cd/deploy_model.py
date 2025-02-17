import boto3
import sagemaker
import os

# Get SageMaker session and role
session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Define model name and S3 bucket
model_name = "retainai-xgboost"
bucket = session.default_bucket()
model_artifact = f"s3://{bucket}/model/xgboost_model.tar.gz"

# Create SageMaker model
sagemaker_client = boto3.client("sagemaker")
sagemaker_client.create_model(
    ModelName=model_name,
    PrimaryContainer={
        "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:latest",
        "ModelDataUrl": model_artifact,
    },
    ExecutionRoleArn=role,
)

# Create endpoint config
config_name = "retainai-xgboost-config"
sagemaker_client.create_endpoint_config(
    EndpointConfigName=config_name,
    ProductionVariants=[
        {
            "VariantName": "default",
            "ModelName": model_name,
            "InstanceType": "ml.m5.large",
            "InitialInstanceCount": 1,
        }
    ],
)

# Deploy model endpoint
endpoint_name = "retainai-xgboost-endpoint"
sagemaker_client.create_endpoint(
    EndpointName=endpoint_name, EndpointConfigName=config_name
)

print(f"Model {model_name} deployed at endpoint {endpoint_name}")
