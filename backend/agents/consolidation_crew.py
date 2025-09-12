from crewai import Agent, Task, Crew
from langchain_community.llms import Ollama

# Initialize the LLM
llm = Ollama(model="llama3")

# Define the Consolidator agent
consolidator = Agent(
    role="Senior Intelligence Editor",
    goal="Review a collection of individual forensic reports from different analysts (visual and text-based) and synthesize them into a single, coherent, and structured summary. Identify any patterns, contradictions, or key findings across all reports.",
    backstory="You are a lead editor at a major intelligence agency, skilled at piecing together disparate pieces of information to form a complete picture. You don't perform new analysis; you synthesize existing findings.",
    llm=llm
)

def create_consolidation_crew(reports: str) -> Crew:
    """
    Create a consolidation crew for synthesizing multiple analysis reports.
    
    Args:
        reports (str): Concatenated string of all individual reports to analyze
        
    Returns:
        Crew: Configured CrewAI crew ready for execution
    """
    task = Task(
        description=f"""
        Review and synthesize the following collection of analysis reports into a single, 
        comprehensive summary. Focus on:
        - Key findings from visual analysis
        - Verified claims and fact-checks
        - Patterns or contradictions across reports
        - Overall assessment of content authenticity

        Reports to analyze:
        {reports}
        """,
        agent=consolidator,
        expected_output="A structured markdown summary containing an executive overview, key findings, supporting evidence, and final recommendations."
    )
    
    # Create and return the crew
    return Crew(
        agents=[consolidator],
        tasks=[task]
    )