from typing import Dict, Any


def generate_explanation(
    timeline: Dict[str, Any],
    analysis: Dict[str, Any],
    confidence: float
) -> str:

    if analysis["status"] != "ANALYZED":
        return (
            "TraceLens could not determine a root cause because the "
            "observed logs did not match any known failure patterns "
            "with sufficient confidence."
        )

    services = ", ".join(timeline.get("services_involved", []))
    pattern = analysis["matched_pattern"]
    root_cause = analysis["root_cause"]

    evidence_lines = []
    for e in analysis.get("evidence", []):
        evidence_lines.append(
            f"- [{e['timestamp']}] {e['service']}: {e['message']}"
        )

    evidence_block = "\n".join(evidence_lines)

    return (
        f"The failure involved the following services: {services}.\n\n"
        f"The observed behavior matches the failure pattern '{pattern}'. "
        f"The root cause is identified as: {root_cause}.\n\n"
        f"Key evidence from the trace:\n"
        f"{evidence_block}\n\n"
        f"Confidence in this analysis: {confidence * 100:.1f}%."
    )
