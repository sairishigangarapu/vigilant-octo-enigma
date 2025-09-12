from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama
from pydantic import BaseModel
from api.models import AnalysisReport

# Initialize the LLM
llm = Ollama(model="llama3")

# Define the Chief Analyst agent
chief_analyst = Agent(
    role="Chief Forensic Analyst",
    goal="Review a final consolidated summary of evidence and produce the definitive verdict. Your output must be a single, valid JSON object that strictly adheres to the provided AnalysisReport Pydantic model.",
    backstory="You are the head of the forensic analysis department. Your judgment is final. You are meticulous and your conclusions are based purely on the evidence presented in the summary. You always output in the required JSON format.",
    llm=llm
)

def create_chief_analyst_crew(consolidated_report: str) -> Crew:
    """
    Create a chief analyst crew for producing the final verdict.
    
    Args:
        consolidated_report (str): The consolidated report to analyze
        
    Returns:
        Crew: Configured CrewAI crew ready for execution
    """
    task = Task(
        description=f"""
        Review the following consolidated report and generate a final verdict in 
        structured JSON format.

        Report to analyze:
        {consolidated_report}

        Your final answer MUST be a JSON object that validates against this Pydantic model:
        {AnalysisReport.schema_json()}

        Requirements:
        - Ensure confidence_score is a float between 0.0 and 1.0
        - Include a clear final_verdict string
        - Provide a concise summary
        - Include all triage reports in the response
        """,
        agent=chief_analyst,
        expected_output="A single, valid JSON object."
    )
    
    # Create and return the crew
    return Crew(
        agents=[chief_analyst],
        tasks=[task]
    )