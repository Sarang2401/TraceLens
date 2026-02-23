from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException
from tracelens.api.schemas import AnalyzeRequest, AnalyzeResponse
from tracelens.ingestion.log_fetcher import LogFetcher
from tracelens.ingestion.demo_fetcher import DemoLogFetcher
from tracelens.ingestion.demo_scenarios import DEMO_SCENARIOS
from tracelens.correlation.trace_filter import filter_valid_trace_logs
from tracelens.correlation.timeline_builder import build_timeline
from tracelens.rag.knowledge_base import FailureKnowledgeBase
from tracelens.analysis.root_cause_engine import RootCauseEngine
from tracelens.analysis.confidence import compute_confidence
from tracelens.analysis.explanation import generate_explanation

router = APIRouter()

# Module-level singletons — avoids re-reading JSON and recomputing
# embeddings on every request.
_KB_PATH = Path(__file__).resolve().parent.parent / "rag" / "failure_patterns.json"
_kb = FailureKnowledgeBase(kb_path=str(_KB_PATH))
_engine = RootCauseEngine(_kb)


# ── Shared analysis pipeline ─────────────────────────────────────────────

def _run_analysis_pipeline(trace_id: str, raw_logs: List[dict]) -> AnalyzeResponse:
    """Run the full TraceLens analysis pipeline on a set of raw logs."""

    if not raw_logs:
        raise HTTPException(
            status_code=404,
            detail="No logs found for given trace_id"
        )

    # 1. Filter valid trace logs
    filtered_logs = filter_valid_trace_logs(raw_logs)

    if not filtered_logs:
        raise HTTPException(
            status_code=404,
            detail="No valid trace logs found after filtering"
        )

    # 2. Build deterministic timeline
    timeline = build_timeline(
        trace_id=trace_id,
        raw_logs=filtered_logs
    )

    # 3. Analyze via RAG engine
    analysis = _engine.analyze(timeline)

    # 4. Confidence scoring
    confidence = compute_confidence(
        analysis_result=analysis,
        total_events=len(timeline.get("events", []))
    )

    # 5. Human-readable explanation
    explanation = generate_explanation(
        timeline=timeline,
        analysis=analysis,
        confidence=confidence
    )

    return AnalyzeResponse(
        status=analysis["status"],
        trace_id=trace_id,
        root_cause=analysis.get("root_cause"),
        infra_fix=analysis.get("infra_fix"),
        matched_pattern=analysis.get("matched_pattern"),
        confidence=confidence,
        evidence=analysis.get("evidence", []),
        explanation=explanation
    )


# ── Production endpoint ──────────────────────────────────────────────────

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_trace(request: AnalyzeRequest):
    """Analyze a trace from live CloudWatch Logs (requires AWS credentials)."""
    try:
        fetcher = LogFetcher()
        raw_logs = fetcher.fetch_logs_by_trace_id(request.trace_id)
        return _run_analysis_pipeline(request.trace_id, raw_logs)

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# ── Demo endpoints ───────────────────────────────────────────────────────

@router.get("/demo/scenarios")
def list_demo_scenarios():
    """List available demo scenarios with their trace IDs and descriptions."""
    return [
        {
            "trace_id": scenario["trace_id"],
            "name": scenario["name"],
            "description": scenario["description"],
            "log_count": len(scenario["logs"]),
        }
        for scenario in DEMO_SCENARIOS.values()
    ]


@router.post("/demo/analyze", response_model=AnalyzeResponse)
def demo_analyze_trace(request: AnalyzeRequest):
    """
    Analyze a demo trace using mock CloudWatch data.
    No AWS credentials required — uses pre-built demo scenarios.
    The full RAG pipeline (embeddings, vector search, analysis) runs on the mock data.
    """
    try:
        fetcher = DemoLogFetcher()
        raw_logs = fetcher.fetch_logs_by_trace_id(request.trace_id)
        return _run_analysis_pipeline(request.trace_id, raw_logs)

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
