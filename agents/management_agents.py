from crewai import Agent
from utils.llm import get_ollama_llm


def create_project_manager_agent():
    """Agent 16: Orchestrates the entire workflow"""
    return Agent(
        role="Project Manager & Orchestrator",
        goal="Coordinate all agents and ensure smooth workflow execution",
        backstory="""You are the project manager overseeing the winning product 
        discovery and launch process. You coordinate between all specialist agents, 
        ensure data flows correctly, handle errors gracefully, and keep the project 
        on track. You make sure each agent completes their task before the next begins. 
        You track progress and report status.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=True,  # Can delegate to other agents
        max_iter=10
    )


def create_report_generator_agent():
    """Agent 17: Final comprehensive reporting"""
    return Agent(
        role="Report Generation Specialist",
        goal="Create detailed, professional reports summarizing all findings",
        backstory="""You are a business analyst who creates comprehensive reports. 
        You summarize all research, analysis, decisions, and actions taken. You create
        structured reports with executive summaries, detailed findings, scores, 
        recommendations, and next steps. You present data clearly with key metrics 
        highlighted. Your reports are actionable and easy to understand.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )
