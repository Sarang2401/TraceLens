from pydantic import BaseModel, Field
from typing import List


class FailurePattern(BaseModel):
    pattern_id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Human readable pattern name")
    description: str = Field(..., description="What failed and how")
    signals: List[str] = Field(..., description="Log-level signals")
    root_cause: str = Field(..., description="Underlying cause")
    infra_fix: str = Field(..., description="Infrastructure-level remediation")
    confidence_hint: float = Field(..., ge=0.0, le=1.0)
