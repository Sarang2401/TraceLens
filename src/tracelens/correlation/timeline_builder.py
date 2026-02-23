from typing import List, Dict
from tracelens.correlation.normalizer import normalize_log_event


def build_timeline(trace_id: str, raw_logs: List[Dict]) -> Dict:
    normalized = [normalize_log_event(log) for log in raw_logs]

    normalized.sort(
        key=lambda x: (
            x["timestamp"],
            x["source"]["log_stream"],
            hash(x["message"])
        )
    )

    events = []
    services = set()

    for idx, event in enumerate(normalized, start=1):
        services.add(event["service"])
        events.append({
            "sequence": idx,
            "service": event["service"],
            "timestamp": event["timestamp"],
            "level": event["level"],
            "event_type": event["event_type"],
            "summary": event["message"],
            "metadata": event["metadata"]
        })

    return {
        "trace_id": trace_id,
        "start_time": normalized[0]["timestamp"] if normalized else None,
        "end_time": normalized[-1]["timestamp"] if normalized else None,
        "services_involved": sorted(list(services)),
        "events": events
    }
