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

# Retrieve the SageMaker Execution Role ARN
sagemaker_client = boto3.client("sagemaker")
iam_client = boto3.client("iam")

roles = iam_client.list_roles()["Roles"]
sagemaker_role = next(
    (role["Arn"] for role in roles if "SageMaker" in role["RoleName"] and "ExecutionRole" in role["RoleName"]),
    None,
)

if not sagemaker_role:
    raise ValueError("❌ ERROR: No SageMaker Execution Role found in your AWS account. Please create one.")

# Generate unique names using timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
model_name = f"retainai-xgboost-{timestamp}"
config_name = f"{model_name}-config"
endpoint_name = f"{model_name}-endpoint"

# Check if model already exists
try:
    sagemaker_client.describe_model(ModelName=model_name)
    print(f"⚠️ Model {model_name} already exists, skipping creation.")
except sagemaker_client.exceptions.ClientError:
    print(f"🚀 Creating model {model_name}...")
    sagemaker_client.create_model(
        ModelName=model_name,
        PrimaryContainer={
            "Image": xgboost_image_uri,
            "ModelDataUrl": model_artifact,
        },
        ExecutionRoleArn=sagemaker_role,
    )
    print(f"✅ Model {model_name} created.")

# Check if endpoint config already exists
try:
    sagemaker_client.describe_endpoint_config(EndpointConfigName=config_name)
    print(f"⚠️ Endpoint config {config_name} already exists, skipping creation.")
except sagemaker_client.exceptions.ClientError:
    print(f"🚀 Creating endpoint config {config_name} with data capture enabled...")
    
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
        DataCaptureConfig={
            "EnableCapture": True,
            "InitialSamplingPercentage": 100,  # Capture all requests
            "DestinationS3Uri": f"s3://{session.default_bucket()}/monitoring",
            "CaptureOptions": [{"CaptureMode": "Input"}, {"CaptureMode": "Output"}],
            "CaptureContentTypeHeader": {"JsonContentTypes": ["application/json"]},
        },
    )
    print(f"✅ Endpoint config {config_name} created with data capture.")

# Check if endpoint already exists
try:
    endpoint_status = sagemaker_client.describe_endpoint(EndpointName=endpoint_name)["EndpointStatus"]
    if endpoint_status in ["Creating", "Updating", "InService"]:
        print(f"⚠️ Endpoint {endpoint_name} already exists with status {endpoint_status}, skipping creation.")
    else:
        print(f"🚀 Updating existing endpoint {endpoint_name}...")
        sagemaker_client.update_endpoint(EndpointName=endpoint_name, EndpointConfigName=config_name)
        print(f"✅ Updated endpoint {endpoint_name}.")
except sagemaker_client.exceptions.ClientError:
    print(f"🚀 Creating new endpoint {endpoint_name}...")
    sagemaker_client.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=config_name)
    print(f"✅ Model {model_name} deployed at endpoint {endpoint_name} using role {sagemaker_role}.")
