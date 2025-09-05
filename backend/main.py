# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import video_processor
import fact_checker

app = FastAPI()

# Configure CORS
origins = ["http://localhost:3000"] # React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_url: str

@app.get("/")
def read_root():
    return {"status": "Vigil AI Lite API is running."}

@app.post("/analyze")
async def analyze_video(request: VideoRequest):
    """
    Main endpoint to analyze a video. Implements the 'Triage & Escalate' model.
    """
    try:
        # 1. Get video metadata
        metadata = video_processor.download_video_and_get_metadata(request.video_url)
        video_title = metadata.get("title", "")

        # 2. TRIAGE: Check with Google Fact Check API first
        fact_check_result = fact_checker.query_google_fact_check(query_text=video_title)
        
        if fact_check_result:
            # Cleanup the downloaded video file
            video_processor.cleanup_files([metadata["video_path"]])
            return {"source": "Google Fact-Check Database", "report": fact_check_result}

        # 3. ESCALATE: If no result, proceed with Gemini analysis
        keyframes = video_processor.extract_keyframes(metadata["video_path"])
        gemini_report = fact_checker.analyze_with_gemini(metadata, keyframes)
        
        # 4. Cleanup all temporary files
        files_to_clean = [metadata["video_path"]] + keyframes
        video_processor.cleanup_files(files_to_clean)

        return {"source": "Vigil AI Generative Analysis", "report": gemini_report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
