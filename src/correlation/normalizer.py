from typing import Dict
from dateutil import parser


def normalize_log_event(raw: Dict) -> Dict:
    timestamp = parser.parse(raw["@timestamp"]).isoformat()

    return {
        "trace_id": raw.get("trace_id") or raw.get("traceId") or raw.get("traceid"),
        "service": raw.get("service", "unknown"),
        "component": raw.get("component", "unknown"),
        "timestamp": timestamp,
        "level": raw.get("level", "INFO"),
        "event_type": raw.get("event_type", "UNKNOWN"),
        "message": raw.get("@message"),
        "metadata": {
            "request_id": raw.get("request_id"),
            "http_status": raw.get("http_status"),
            "latency_ms": raw.get("latency_ms"),
            "dependency": raw.get("dependency"),
            "exception_type": raw.get("exception_type"),
            "stacktrace": raw.get("stacktrace")
        },
        "source": {
            "log_group": raw.get("@log"),
            "log_stream": raw.get("@logStream")
        }
    }
