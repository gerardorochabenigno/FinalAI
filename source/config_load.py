import yaml
import boto3

def cargar_config(path="config/credentials.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

def get_textract_client():
    config = cargar_config()
    aws_config = config.get("aws", {})

    if not all(k in aws_config for k in ["access_key_id", "secret_access_key", "region"]):
        raise ValueError("Faltan credenciales de AWS en el archivo YAML")

    return boto3.client(
        "textract",
        aws_access_key_id=aws_config["access_key_id"],
        aws_secret_access_key=aws_config["secret_access_key"],
        region_name=aws_config["region"]
    )