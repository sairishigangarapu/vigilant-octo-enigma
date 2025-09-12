from crewai import Agent, Task, Crew, Process
from langchain_community.llms import Ollama
from .tools import GoogleFactCheckTool

# Initialize the LLM
llm = Ollama(model="llama3")

# Define the Visual Analyst agent
visual_analyst = Agent(
    role="Forensic Image Analyst",
    goal="Meticulously analyze a given image for any signs of digital manipulation, deepfakes, or inconsistencies. Provide a detailed report of your findings.",
    backstory="You are a seasoned digital forensics expert with a keen eye for detail, specializing in identifying sophisticated AI-generated images and manipulations.",
    llm=llm
)

# Define the Text Analyst agent with fact-checking tool
text_analyst = Agent(
    role="Fact-Checking Journalist",
    goal="Analyze a given text, identify the core claims being made, and verify their authenticity using available tools. Report on the veracity of the claims.",
    backstory="You are a sharp, investigative journalist known for your ability to quickly dissect articles and statements, cross-referencing claims to uncover the truth.",
    llm=llm,
    tools=[GoogleFactCheckTool()]
)

def create_triage_crew(image_paths: list[str], transcript_content: str) -> Crew:
    """
    Create a triage crew for analyzing media content.
    
    Args:
        image_paths (list[str]): List of paths to images that need analysis
        transcript_content (str): Content of the transcript to analyze
        
    Returns:
        Crew: Configured CrewAI crew ready for execution
    """
    tasks = []
    
    # Create tasks for each image
    for idx, image_path in enumerate(image_paths):
        tasks.append(
            Task(
                description=f"Analyze image at {image_path} for signs of manipulation or AI generation. Provide a detailed report.",
                agent=visual_analyst
            )
        )
    
    # Create task for transcript analysis
    tasks.append(
        Task(
            description="Analyze the transcript content, identify key claims, and verify their authenticity. Provide a comprehensive fact-check report.",
            agent=text_analyst,
            context={"transcript": transcript_content}
        )
    )
    
    # Create and return the crew
    return Crew(
        agents=[visual_analyst, text_analyst],
        tasks=tasks,
        process=Process.parallel
    )