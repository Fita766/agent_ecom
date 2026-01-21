from crewai import Task
from agents.research_agents import (
    create_trend_scout_agent,
    create_market_analyzer_agent,
    create_competitor_intel_agent
)


def create_trend_discovery_task():
    """Task 1: Find trending products"""
    return Task(
        description="""
        Search TikTok and Pinterest for trending products with viral potential.
        
        Search for products in these categories:
        - Home & Garden gadgets
        - Beauty & Personal Care
        - Pet accessories
        - Fashion accessories
        - Kitchen tools
        - Tech gadgets under 5kg
        
        For each product found:
        1. Extract product name and description
        2. Get engagement metrics (views, likes, shares, saves)
        3. Get video/pin URLs
        4. Estimate product category
        
        Focus on products with:
        - High engagement (10k+ views/saves)
        - Recent posts (last 30 days)
        - Clear product visuals
        - Lightweight (under 5kg estimated)
        
        Return top 5 trending products with complete data.
        """,
        agent=create_trend_scout_agent(),
        expected_output="""
        A JSON list of 5 trending products with:
        - product_name
        - description
        - category
        - source_platform
        - source_url
        - engagement_metrics
        - estimated_weight_category
        """
    )


def create_market_analysis_task(context):
    """Task 2: Analyze market for each product"""
    return Task(
        description="""
        For each product from the trend discovery, conduct deep market analysis:
        
        1. Determine target niche and category
        2. Estimate market size (Small/Medium/Large/Huge)
        3. Assess competition level (Low/Medium/High/Very High)
        4. Identify target geographies (US, EU, FR, UK, etc)
        5. Determine seasonality (if any)
        6. Assess trend direction (Rising/Stable/Declining)
        
        Consider:
        - Is this a saturated market?
        - Who is the target customer (demographics)?
        - What geographies show most demand?
        - Is demand seasonal or year-round?
        - Can a new store compete effectively?
        
        Provide market analysis for each product.
        """,
        agent=create_market_analyzer_agent(),
        context=context,
        expected_output="""
        Market analysis for each product:
        - niche
        - market_size_estimate
        - competition_level
        - target_geographies (list)
        - seasonality
        - trend_direction
        - target_demographics
        """
    )


def create_competitor_analysis_task(context):
    """Task 3: Competitive intelligence"""
    return Task(
        description="""
        Analyze competitive landscape for each product:
        
        1. Identify how many competitors exist
        2. Analyze their market positioning
        3. Find gaps and opportunities
        4. Assess barrier to entry
        5. Determine if market is oversaturated
        
        Questions to answer:
        - How many established players exist?
        - What's their pricing strategy?
        - What's their unique value proposition?
        - Can we differentiate effectively?
        - Is there room for a new entrant?
        
        Provide competitive analysis per product.
        """,
        agent=create_competitor_intel_agent(),
        context=context,
        expected_output="""
        Competitive analysis:
        - number_of_competitors
        - market_saturation_level
        - differentiation_opportunities
        - barrier_to_entry
        - recommendation (Can we compete? Yes/No/Maybe)
        """
    )
