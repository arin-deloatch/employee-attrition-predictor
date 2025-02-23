import os
import boto3
import sagemaker

# Retrieve the dynamic model URL from an environment variable
model_artifact = os.getenv("MODEL_URL")
if not model_artifact:
    raise ValueError("MODEL_URL environment variable is not set.")

# Initialize SageMaker session and role
session = sagemaker.Session()
role = sagemaker.get_execution_role()

# Define model name (you might also want to include versioning or timestamps)
model_name = "retainai-xgboost"

# Create SageMaker client
sagemaker_client = boto3.client("sagemaker")

# Create the SageMaker model using the dynamic model URL
sagemaker_client.create_model(
    ModelName=model_name,
    PrimaryContainer={
        "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:latest",
        "ModelDataUrl": model_artifact,
    },
    ExecutionRoleArn=role,
)

# Create endpoint configuration
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
