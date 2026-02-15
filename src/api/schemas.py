from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AnalyzeRequest(BaseModel):
    trace_id: str = Field(..., min_length=3)
    question: Optional[str] = Field(
        None,
        description="Natural language question about the trace"
    )


class EvidenceItem(BaseModel):
    sequence: int
    service: str
    timestamp: str
    message: str


class AnalyzeResponse(BaseModel):
    status: str
    trace_id: Optional[str]
    root_cause: Optional[str]
    infra_fix: Optional[str]
    matched_pattern: Optional[str]
    confidence: float
    evidence: List[EvidenceItem]
    explanation: str
