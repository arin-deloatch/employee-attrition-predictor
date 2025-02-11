import boto3

sagemaker = boto3.client("sagemaker")

# Define Model Package
#TODO:
model_name = ""
image_uri = ""

response = sagemaker.create_model(
    ModelName=model_name,
    PrimaryContainer={"Image": image_uri},
    ExecutionRoleArn="arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole"
)

print("Model deployed:", response)
