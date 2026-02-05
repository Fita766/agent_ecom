from crewai import Agent
from utils.llm import get_ollama_llm
from tools.tiktok_scraper import TikTokScraperTool
from tools.product_extractor import ProductExtractorTool


def create_trend_scout_agent():
    """Agent 1: Finds trending PRODUCTS (not videos) on TikTok"""
    return Agent(
        role="Trend Scout & Product Extraction Specialist",
        goal="Discover REAL trending products from viral TikTok videos and extract actual product names",
        backstory="""You are an expert at finding viral products on TikTok.
        
        YOUR WORKFLOW:
        1. Search TikTok with PRODUCT-FOCUSED hashtags like #tiktokmakemebuyit, #amazonfinds, #musthaves
        2. For EACH video found, USE ProductExtractor tool to identify the ACTUAL PRODUCT
        3. Return 5 DIFFERENT real products (not video titles!)
        
        CRITICAL:
        - You extract PRODUCTS from videos, not video titles
        - "DIY Home Hacks" is a VIDEO → extract "LED Strip Lights" as PRODUCT
        - Use ProductExtractor for every TikTok result
        - Focus on lightweight products under 5kg
        
        TOOL USAGE:
        - TikTok Scraper: Search with hashtags
        - Product Extractor: Extract product from video title/description
        
        Example:
        TikTok Video: "DIY Room Makeover with these LED lights! 🔥"
        → Extract: "LED Strip Lights RGB" (the actual product)
        """,
        tools=[TikTokScraperTool(), ProductExtractorTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False,
        max_iter=10  # Plus d'itérations pour extraction
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
