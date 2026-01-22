from crewai import Agent
from utils.llm import get_ollama_llm
from tools.tiktok_scraper import TikTokScraperTool
from tools.pinterest_scraper import PinterestScraperTool


def create_trend_scout_agent():
    """Agent 1: Finds trending products on social media"""
    return Agent(
        role="Trend Scout Specialist",
        goal="Discover viral and trending products on TikTok and Pinterest",
        backstory="""You are an expert at identifying emerging product trends 
        on social media platforms. You monitor TikTok and Pinterest daily to spot 
        products that are gaining traction. You focus on products with high engagement, 
        viral potential, and clear dropshipping viability. You prioritize lightweight 
        products under 5kg to ensure reasonable shipping costs.
        
        IMPORTANT: When using tools, always pass a SINGLE dictionary object with 
        the required fields. Never pass a list of objects. For example:
        - CORRECT: {"keywords": ["home gadgets"], "max_videos": 3}
        - WRONG: [{"keywords": ["home gadgets"], "max_videos": 3}]
        """,
        tools=[TikTokScraperTool(), PinterestScraperTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )


def create_market_analyzer_agent():
    """Agent 2: Deep market analysis"""
    return Agent(
        role="Market Analysis Expert",
        goal="Conduct comprehensive market analysis for product viability",
        backstory="""You are a market research specialist with deep expertise in 
        e-commerce and dropshipping. You analyze market size, demand trends, 
        competition levels, and seasonality. You determine if a product has
        sustainable demand or is just a passing fad. You identify target demographics 
        and optimal geographic markets (US, EU, FR, etc).""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_competitor_intel_agent():
    """Agent 3: Competitive intelligence"""
    return Agent(
        role="Competitive Intelligence Analyst",
        goal="Analyze competitors and market positioning",
        backstory="""You are a competitive intelligence expert who studies 
        competitor strategies, pricing, and market share. You identify gaps 
        in the market and opportunities for differentiation. You assess how 
        saturated a niche is and whether new entrants can succeed.""",
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )
