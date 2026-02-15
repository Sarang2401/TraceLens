from pydantic import BaseModel
from typing import List
import os


class TraceLensSettings(BaseModel):
    aws_region: str = os.getenv("AWS_REGION", "ap-south-1")
    log_groups: List[str] = os.getenv(
        "TRACE_LENS_LOG_GROUPS",
        "/aws/lambda/service-a,/aws/lambda/service-b"
    ).split(",")

    insights_query_limit: int = 10000
    query_timeout_seconds: int = 30

    default_lookback_minutes: int = 60


settings = TraceLensSettings()
