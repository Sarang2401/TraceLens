from typing import List, Dict


def filter_valid_trace_logs(raw_logs: List[Dict]) -> List[Dict]:
    return [
        log for log in raw_logs
        if "trace_id" in log or "traceId" in log or "traceid" in log
    ]
