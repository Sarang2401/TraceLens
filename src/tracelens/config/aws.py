import boto3
from tracelens.config.settings import settings


def cloudwatch_logs_client():
    return boto3.client(
        "logs",
        region_name=settings.aws_region
    )
