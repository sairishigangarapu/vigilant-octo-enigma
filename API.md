# Vigil AI Lite API

## POST `/analyze`
Analyzes a video from a URL using a "Triage & Escalate" model.

**Request Body:**
{
  "video_url": "https://www.youtube.com/watch?v=..."
}

**Success Response (200):**
The response object contains a `source` field and a `report` object. The structure of the `report` depends on the `source`.

**Example (Source: Google Fact-Check Database):**
{
  "source": "Google Fact-Check Database",
  "report": {
    "text": "The claim text.",
    "claimant": "Claimant Name",
    "rating": "False",
    "url": "https://example.com/factcheck"
  }
}

**Example (Source: Vigil AI Generative Analysis):**
{
  "source": "Vigil AI Generative Analysis",
  "report": {
    "risk_level": "High Risk",
    "summary": "...",
    "context_check": { ... },
    "claim_verification": { ... },
    "visual_red_flags": [ ... ]
  }
}
