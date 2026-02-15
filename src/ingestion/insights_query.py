def build_trace_query(trace_id: str) -> str:
    return f"""
    fields @timestamp, @message, @logStream, @log
    | filter trace_id = "{trace_id}"
    | sort @timestamp asc
    """
