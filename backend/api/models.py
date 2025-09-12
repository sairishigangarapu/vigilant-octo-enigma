from pydantic import BaseModel, HttpUrl, Field, field_validator
from typing import List
from uuid import UUID

class AnalyzeUrlRequest(BaseModel):
    url: HttpUrl

class TriageReport(BaseModel):
    agent: str
    report: str

class AnalysisReport(BaseModel):
    request_id: str
    status: str
    final_verdict: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    summary: str
    triage_reports: List[TriageReport]

    @field_validator('confidence_score')
    def validate_confidence_score(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence score must be between 0.0 and 1.0')
        return v