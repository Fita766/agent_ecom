from crewai import Agent
from utils.llm import get_ollama_llm


def create_scoring_engine_agent():
    """Agent 10: Product scoring system"""
    return Agent(
        role="Product Scoring Engine",
        goal="Calculate comprehensive scores for each product across 6 dimensions",
        backstory="""You are a data scientist specializing in multi-criteria decision 
        analysis. You score products on: trend momentum, profit potential, competition, 
        demand, quality, and shipping feasibility. Each dimension is scored 0-100. 
        You calculate a weighted overall score where:
        - Trend Score: 25%
        - Profit Score: 25%
        - Competition Score: 15% (lower is better)
        - Demand Score: 20%
        - Quality Score: 10%
        - Shipping Score: 5%
        You provide detailed reasoning for each score.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_decision_maker_agent():
    """Agent 11: Final GO/NO-GO decision"""
    return Agent(
        role="Product Decision Maker",
        goal="Make final approval decision based on comprehensive analysis",
        backstory="""You are the final decision authority. You review all data: 
        market analysis, pricing, reviews, trends, and scores. You approve products 
        only if they meet strict criteria:
        - Overall score >= 75/100
        - Profit margin >= 30%
        - No major quality red flags
        - Weight under 5kg
        - Sustainable trend (not a dying fad)
        - Clear target market
        You provide a clear GO or NO-GO decision with detailed reasoning. 
        If NO-GO, you explain exactly why the product was rejected.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )
