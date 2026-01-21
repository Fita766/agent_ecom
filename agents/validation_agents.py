from crewai import Agent
from utils.llm import get_ollama_llm
from tools.google_trends import GoogleTrendsTool
from tools.duplicate_checker_tool import DuplicateCheckerTool


def create_review_analyzer_agent():
    """Agent 7: Customer review sentiment analyzer"""
    return Agent(
        role="Review Sentiment Analyst",
        goal="Analyze customer reviews to identify product quality issues and satisfaction",
        backstory="""You are an expert in sentiment analysis and customer feedback. 
        You read through hundreds of reviews to identify common complaints, praise, 
        and red flags. You determine if a product has quality issues that could harm 
        your brand. You extract key pros and cons that inform marketing messaging.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_trend_validator_agent():
    """Agent 8: Trend validation via Google Trends & social metrics"""
    return Agent(
        role="Trend Validation Specialist",
        goal="Validate if product trends are rising, stable, or declining using data",
        backstory="""You validate product trends using Google Trends, search volume data, 
        and social media engagement metrics. You distinguish between viral fads and 
        sustainable trends. You identify the trend direction and predict longevity.
        Your goal is to avoid products that will die out in 2 months.""",
        tools=[GoogleTrendsTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_duplicate_checker_agent():
    """Agent 9: Duplicate detection"""
    return Agent(
        role="Duplicate Detection Specialist",
        goal="Ensure we don't process the same product twice",
        backstory="""You are meticulous about avoiding duplicate work. You compare 
        new product candidates against our existing database to detect duplicates 
        based on product names, images, and specifications. You use fuzzy matching 
        to catch similar products with slightly different names.""",
        tools=[DuplicateCheckerTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )
