from uuid import uuid4
from fastapi import FastAPI
from .models import AnalyzeUrlRequest, AnalysisReport
from core.pipeline import run_full_analysis

app = FastAPI(
    title="Vigil AI Pro API",
    description="AI-powered media analysis and fact-checking service",
    version="1.0.0"
)

@app.post("/analyze-url", response_model=AnalysisReport)
async def analyze_url(request: AnalyzeUrlRequest) -> AnalysisReport:
    """
    Analyze a URL containing media content for potential misinformation.
    
    Args:
        request (AnalyzeUrlRequest): Request containing the URL to analyze
        
    Returns:
        AnalysisReport: Comprehensive analysis report
    """
    # Generate unique request ID
    request_id = str(uuid4())
    
    # Run the full analysis pipeline
    result = run_full_analysis(
        url=str(request.url),
        request_id=request_id
    )
    
    # Convert dictionary to Pydantic model
    return AnalysisReport(**result)