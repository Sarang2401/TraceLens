from fastapi import APIRouter, HTTPException
from tracelens.api.schemas import AnalyzeRequest, AnalyzeResponse
from tracelens.ingestion.log_fetcher import LogFetcher
from tracelens.correlation.timeline_builder import build_timeline
from tracelens.rag.knowledge_base import FailureKnowledgeBase
from tracelens.analysis.root_cause_engine import RootCauseEngine
from tracelens.analysis.confidence import compute_confidence
from tracelens.analysis.explanation import generate_explanation

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_trace(request: AnalyzeRequest):
    try:
        # 1. Fetch logs
        fetcher = LogFetcher()
        raw_logs = fetcher.fetch_logs_by_trace_id(request.trace_id)

        if not raw_logs:
            raise HTTPException(
                status_code=404,
                detail="No logs found for given trace_id"
            )

        # 2. Build deterministic timeline
        timeline = build_timeline(
            trace_id=request.trace_id,
            raw_logs=raw_logs
        )

        # 3. Load RAG knowledge base
        kb = FailureKnowledgeBase(
            kb_path="src/tracelens/rag/failure_patterns.json"
        )

        # 4. Analyze
        engine = RootCauseEngine(kb)
        analysis = engine.analyze(timeline)

        # 5. Confidence
        confidence = compute_confidence(
            analysis_result=analysis,
            total_events=len(timeline.get("events", []))
        )

        # 6. Explanation
        explanation = generate_explanation(
            timeline=timeline,
            analysis=analysis,
            confidence=confidence
        )

        return AnalyzeResponse(
            status=analysis["status"],
            trace_id=request.trace_id,
            root_cause=analysis.get("root_cause"),
            infra_fix=analysis.get("infra_fix"),
            matched_pattern=analysis.get("matched_pattern"),
            confidence=confidence,
            evidence=analysis.get("evidence", []),
            explanation=explanation
        )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
