"""
Demo log fetcher — returns mock CloudWatch Logs for demo scenarios.

Drop-in replacement for LogFetcher that serves pre-built demo data
instead of querying AWS CloudWatch Logs Insights.
"""

from typing import List, Dict
from tracelens.ingestion.demo_scenarios import DEMO_SCENARIOS


class DemoLogFetcher:
    """Fetcher that returns mock logs for known demo trace IDs."""

    def fetch_logs_by_trace_id(self, trace_id: str) -> List[Dict]:
        scenario = DEMO_SCENARIOS.get(trace_id)

        if scenario is None:
            available = list(DEMO_SCENARIOS.keys())
            raise KeyError(
                f"Unknown demo trace_id '{trace_id}'. "
                f"Available demo traces: {available}"
            )

        return scenario["logs"]
