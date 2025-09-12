import json
from typing import Dict, Any
from .processor import deconstruct_video
from .live_updater import LiveUpdater
from agents.triage_crew import create_triage_crew
from agents.consolidation_crew import create_consolidation_crew
from agents.chief_analyst_crew import create_chief_analyst_crew

def run_full_analysis(url: str, request_id: str) -> Dict[str, Any]:
    """
    Run the complete Vigil AI Pro analysis pipeline.
    
    Args:
        url (str): URL of the media to analyze
        request_id (str): Unique identifier for this analysis request
        
    Returns:
        Dict[str, Any]: Final analysis report as a dictionary
    """
    # Initialize live updates
    updater = LiveUpdater(request_id)
    
    # Step 1: Deconstruction
    updater.post_status("Deconstructing media...")
    media_chunks = deconstruct_video(url)
    
    with open(media_chunks["transcript_path"], "r", encoding="utf-8") as f:
        transcript_content = f.read()
    
    # Step 2: Triage Analysis
    updater.post_status("Starting parallel triage analysis...")
    triage_crew = create_triage_crew(
        image_paths=media_chunks["frames"],
        transcript_content=transcript_content
    )
    triage_results = triage_crew.kickoff()
    
    # Step 3: Consolidation
    updater.post_status("Consolidating triage reports...")
    consolidation_crew = create_consolidation_crew(triage_results)
    consolidated_summary = consolidation_crew.kickoff()
    
    # Step 4: Final Analysis
    updater.post_status("Performing final analysis...")
    chief_analyst_crew = create_chief_analyst_crew(consolidated_summary)
    final_report_json = chief_analyst_crew.kickoff()
    
    # Step 5: Final Report
    updater.post_status("Analysis complete.")
    final_report = json.loads(final_report_json)
    final_report["request_id"] = request_id
    
    return final_report