import time
from typing import List, Dict
from tracelens.config.aws import cloudwatch_logs_client
from tracelens.config.settings import settings


class CloudWatchInsightsClient:
    def __init__(self):
        self.client = cloudwatch_logs_client()

    def run_query(
        self,
        log_group_names: List[str],
        query_string: str,
        start_time: int,
        end_time: int
    ) -> List[Dict]:

        response = self.client.start_query(
            logGroupNames=log_group_names,
            startTime=start_time,
            endTime=end_time,
            queryString=query_string,
            limit=settings.insights_query_limit
        )

        query_id = response["queryId"]

        start = time.time()
        while True:
            result = self.client.get_query_results(queryId=query_id)
            status = result["status"]

            if status == "Complete":
                return result["results"]

            if time.time() - start > settings.query_timeout_seconds:
                raise TimeoutError("CloudWatch Logs Insights query timed out")

            time.sleep(1)
