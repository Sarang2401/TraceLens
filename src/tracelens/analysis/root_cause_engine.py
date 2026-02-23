from typing import Dict, List, Any
from tracelens.rag.knowledge_base import FailureKnowledgeBase


class RootCauseEngine:
    def __init__(self, kb: FailureKnowledgeBase):
        self.kb = kb

    def analyze(self, timeline: Dict[str, Any]) -> Dict[str, Any]:
        events = timeline.get("events", [])

        if not events:
            raise ValueError("Timeline contains no events")

        event_texts = [
            f"{e['service']} {e['event_type']} {e['summary']}"
            for e in events
        ]

        retrieved = self.kb.retrieve(event_texts)

        if not retrieved:
            return {
                "status": "INSUFFICIENT_EVIDENCE",
                "reason": "No known failure patterns matched the observed logs",
                "root_cause": None,
                "infra_fix": None,
                "matched_pattern": None,
                "evidence": []
            }

        best_match, similarity = retrieved[0]

        evidence = self._extract_evidence(
            events,
            best_match["signals"]
        )

        return {
            "status": "ANALYZED",
            "matched_pattern": best_match["pattern_id"],
            "root_cause": best_match["root_cause"],
            "infra_fix": best_match["infra_fix"],
            "pattern_similarity": round(similarity, 4),
            "evidence": evidence,
            "confidence_hint": best_match["confidence_hint"]
        }

    def _extract_evidence(
        self,
        events: List[Dict[str, Any]],
        signals: List[str]
    ) -> List[Dict[str, Any]]:
        matched = []

        for event in events:
            message = event["summary"].lower()
            for signal in signals:
                if signal.lower() in message:
                    matched.append({
                        "sequence": event["sequence"],
                        "service": event["service"],
                        "timestamp": event["timestamp"],
                        "message": event["summary"]
                    })
                    break

        return matched
