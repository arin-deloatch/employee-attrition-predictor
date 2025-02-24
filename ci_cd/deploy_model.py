import os
import boto3
import sagemaker
from datetime import datetime

# Retrieve the dynamic model URL from an environment variable
model_artifact = os.getenv("MODEL_URL")
if not model_artifact:
    raise ValueError("❌ ERROR: MODEL_URL environment variable is not set.")

# Initialize SageMaker session
session = sagemaker.Session()

# Get AWS region dynamically
region = session.boto_region_name
if not region:
    raise ValueError("❌ ERROR: Unable to determine AWS region.")

# Get the latest SageMaker XGBoost container image for the region
xgboost_image_uri = sagemaker.image_uris.retrieve("xgboost", region, version="latest")

# Dynamically retrieve the SageMaker Execution Role ARN
iam_client = boto3.client("iam")
roles = iam_client.list_roles()["Roles"]

# Find a role that has "SageMakerExecutionRole" or similar in its name
sagemaker_role = None
for role in roles:
    if "SageMaker" in role["RoleName"] and "ExecutionRole" in role["RoleName"]:
        sagemaker_role = role["Arn"]
        break

if not sagemaker_role:
    raise ValueError("❌ ERROR: No SageMaker Execution Role found in your AWS account. Please create one.")

# Generate a unique model name using timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
model_name = f"retainai-xgboost-{timestamp}"
config_name = f"{model_name}-config"
endpoint_name = f"{model_name}-endpoint"

# Create SageMaker client
sagemaker_client = boto3.client("sagemaker")

# Create the SageMaker model using the dynamic model URL
sagemaker_client.create_model(
    ModelName=model_name,
    PrimaryContainer={
        "Image": xgboost_image_uri,  # Use the correct SageMaker-provided image
        "ModelDataUrl": model_artifact,
    },
    ExecutionRoleArn=sagemaker_role,
)

# Create endpoint configuration
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
sagemaker_client.create_endpoint(
    EndpointName=endpoint_name, EndpointConfigName=config_name
)

print(f"✅ Model {model_name} deployed at endpoint {endpoint_name} using role {sagemaker_role}")
