from datetime import datetime, timedelta, timezone
from typing import List, Dict
from tracelens.ingestion.cloudwatch_client import CloudWatchInsightsClient
from tracelens.ingestion.insights_query import build_trace_query
from tracelens.config.settings import settings


class LogFetcher:
    def __init__(self):
        self.client = CloudWatchInsightsClient()

    def fetch_logs_by_trace_id(self, trace_id: str) -> List[Dict]:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=settings.default_lookback_minutes)

        results = self.client.run_query(
            log_group_names=settings.log_groups,
            query_string=build_trace_query(trace_id),
            start_time=int(start_time.timestamp()),
            end_time=int(end_time.timestamp())
        )

        logs = []
        for entry in results:
            record = {}
            for field in entry:
                record[field["field"]] = field["value"]
            logs.append(record)

        return logs
