from crewai import Agent
from utils.llm import get_ollama_llm
from tools.aliexpress_scraper import AliExpressScraperTool
from tools.amazon_scraper import AmazonScraperTool


def create_aliexpress_scraper_agent():
    """Agent 4: AliExpress supplier finder"""
    return Agent(
        role="AliExpress Sourcing Specialist",
        goal="Find the best suppliers on AliExpress with optimal pricing and reliability",
        backstory="""You are an expert at sourcing products from AliExpress. 
        You evaluate suppliers based on price, ratings, order volume, shipping times, 
        and product quality. You identify the most reliable suppliers with the best 
        value proposition for dropshipping. You prioritize suppliers with high ratings 
        (4.5+), many orders, and reasonable shipping times.""",
        tools=[AliExpressScraperTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_amazon_scraper_agent():
    """Agent 5: Amazon competitor analyzer"""
    return Agent(
        role="Amazon Market Intelligence",
        goal="Analyze Amazon competitor prices, ratings, and market positioning",
        backstory="""You specialize in analyzing Amazon marketplace data to understand 
        competitive pricing, customer satisfaction, and market demand. You identify
        price ranges, review sentiments, and bestseller trends. Your insights help 
        determine optimal retail pricing and competitive positioning.""",
        tools=[AmazonScraperTool()],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_pricing_strategist_agent():
    """Agent 6: Pricing and margin calculator"""
    return Agent(
        role="Pricing Strategy Expert",
        goal="Calculate optimal pricing with maximum profitability while staying competitive",
        backstory="""You are a pricing strategist with expertise in e-commerce margins. 
        You calculate total costs (product + shipping), analyze competitor prices, 
        and determine the optimal retail price that maximizes profit while remaining 
        attractive to customers. You ensure minimum 30% profit margins and account 
        for geographic pricing variations (US vs EU markets have different pricing power).
        
        IMPORTANT: You MUST use the actual data from previous tasks:
        - Supplier prices and shipping costs from AliExpress sourcing task
        - Competitor prices from Amazon pricing task
        - Calculate real numbers, not placeholders
        
        For each product, you will:
        1. Extract supplier price and shipping cost from AliExpress data
        2. Calculate total cost (supplier price + shipping)
        3. Analyze competitor price range from Amazon data
        4. Determine optimal retail price (competitive but with 30%+ margin)
        5. Calculate profit margin percentage
        6. Calculate profit amount per unit
        7. Consider geographic pricing variations if applicable
        
        Return detailed pricing strategy with actual calculated numbers for each product.
        """,
        tools=[],
        llm=get_ollama_llm(),
        verbose=True,
        allow_delegation=False
    )
