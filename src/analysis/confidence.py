from typing import Dict, Any


def compute_confidence(
    analysis_result: Dict[str, Any],
    total_events: int
) -> float:

    if analysis_result["status"] != "ANALYZED":
        return 0.0

    evidence_count = len(analysis_result.get("evidence", []))
    if total_events == 0:
        return 0.0

    evidence_coverage = evidence_count / total_events
    similarity = analysis_result.get("pattern_similarity", 0.0)
    hint = analysis_result.get("confidence_hint", 0.0)

    confidence = hint * evidence_coverage * similarity

    return round(min(confidence, 1.0), 3)
