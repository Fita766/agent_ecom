from crewai import Task
from agents.research_agents import (
    create_trend_scout_agent,
    create_market_analyzer_agent,
    create_competitor_intel_agent
)


# Hashtags TikTok optimisés pour produits viraux
TIKTOK_PRODUCT_HASHTAGS = [
    "tiktokmakemebuyit",
    "amazonfinds",
    "musthaves",
    "founditonamazon",
    "tiktokshop",
    "productreview",
    "tiktokviral",
    "amazongadgets"
]


def create_trend_discovery_task():
    """Task 1: Find trending PRODUCTS (not videos!) from TikTok"""
    return Task(
        description=f"""
        YOUR MISSION: Find 5 REAL trending PRODUCTS from TikTok (NOT video titles!)
        
        STEP-BY-STEP WORKFLOW:
        
        1. SEARCH TIKTOK with product-focused hashtags:
           Use TikTok Scraper with these keywords: {TIKTOK_PRODUCT_HASHTAGS[:3]}
           
           Example call:
           {{"keywords": ["tiktokmakemebuyit", "amazonfinds"], "max_videos": 10, "region": "us"}}
        
        2. FOR EACH VIDEO FOUND:
           - Use Product Extractor tool to identify the ACTUAL PRODUCT
           - Input: video title + description + hashtags
           - Output: Real product name, category, description
           
           CRITICAL: "DIY Home Hacks" is NOT a product!
           → Extract "LED Strip Lights" from the video content
        
        3. COLLECT 5 DIFFERENT PRODUCTS:
           - Each must be a REAL physical product (not a video title)
           - No duplicates
           - Lightweight (under 5kg estimated)
           - Clear product name and category
        
        4. FOR EACH PRODUCT, INCLUDE:
           - product_name: ACTUAL product (e.g., "LED Strip Lights RGB 5M")
           - description: Brief product description
           - category: Home & Garden, Beauty, Tech, Fashion, Kitchen, Pet
           - source_platform: "TikTok"
           - source_url: Original TikTok video URL
           - engagement_metrics: {{likes, comments, shares}}
           - estimated_weight_category: "under 1kg" or "1-3kg" or "3-5kg"
        
        VALIDATION:
        ❌ BAD: {{"product_name": "DIY Home Hacks"}}  ← This is a VIDEO!
        ✅ GOOD: {{"product_name": "LED Strip Lights RGB", "category": "Home & Garden"}}
        
        Return a JSON array of 5 distinct products.
        """,
        agent=create_trend_scout_agent(),
        expected_output="""
        JSON array of 5 real products (NOT video titles):
        [
          {{
            "product_name": "LED Strip Lights RGB 5M",
            "description": "Color-changing LED strips with remote control",
            "category": "Home & Garden",
            "source_platform": "TikTok",
            "source_url": "https://tiktok.com/@user/video/123",
            "engagement_metrics": {{"likes": 125000, "comments": 5000, "shares": 25000}},
            "estimated_weight_category": "under 1kg"
          }},
          ... (4 more DIFFERENT products)
        ]
        """
    )


def create_market_analysis_task(context):
    """Task 2: Analyze market for each REAL product"""
    return Task(
        description="""
        For EACH REAL PRODUCT from trend discovery (NOT video titles!):
        
        1. Verify you received actual products:
           ✅ "LED Strip Lights" → REAL product
           ❌ "DIY Home Hacks" → VIDEO title (reject!)
        
        2. Conduct market analysis:
           - Determine target niche and subcategory
           - Estimate market size (Small/Medium/Large/Huge)
           - Assess competition level (Low/Medium/High/Very High)
           - Identify target geographies (US, EU, FR, UK, etc)
           - Determine seasonality (if any)
           - Assess trend direction (Rising/Stable/Declining)
        
        3. Answer key questions:
           - Is this a saturated market?
           - Who is the target customer?
           - What geographies show most demand?
           - Is demand seasonal or year-round?
           - Can a new store compete?
        
        4. FOR EACH PRODUCT provide:
           - niche: Specific product niche
           - market_size_estimate: Small/Medium/Large/Huge
           - competition_level: Low/Medium/High/Very High
           - target_geographies: ["US", "UK", "CA", ...]
           - seasonality: Description or "None"
           - trend_direction: Rising/Stable/Declining
           - target_demographics: Age, income, interests
           - saturated: Yes/No with reasoning
           - demand_sustainable: Yes/No with reasoning
        
        IMPORTANT: Analyze ONLY real products with actual names!
        Reject any entry that looks like "[Product Name X]" or video titles.
        """,
        agent=create_market_analyzer_agent(),
        context=context,
        expected_output="""
        Market analysis for EACH REAL product:
        {{
          "products": [
            {{
              "product_name": "LED Strip Lights RGB 5M",
              "analysis": {{
                "niche": "Smart home lighting and room decoration",
                "market_size_estimate": "Large",
                "competition_level": "Medium",
                "target_geographies": ["US", "UK", "CA", "DE"],
                "seasonality": "Slight peak in winter (holidays)",
                "trend_direction": "Rising",
                "target_demographics": "Ages 18-35, tech-savvy, home decor enthusiasts",
                "saturated": "Moderately saturated but high demand",
                "demand_sustainable": "Yes - growing smart home market"
              }}
            }},
            ... (other products)
          ]
        }}
        """
    )


def create_competitor_analysis_task(context):
    """Task 3: Competitive intelligence"""
    return Task(
        description="""
        Analyze competitive landscape for each REAL product:
        
        1. Verify products are real (not video titles or templates)
        
        2. For each product:
           - Identify number of established competitors
           - Analyze their market positioning
           - Find gaps and opportunities
           - Assess barrier to entry
           - Determine if market is oversaturated
        
        3. Questions to answer:
           - How many established players?
           - What's their pricing strategy?
           - What's their unique value proposition?
           - Can we differentiate effectively?
           - Is there room for a new entrant?
        
        4. Provide detailed competitive analysis
        
        REJECT any template entries like "[Product Name 2]" or video titles!
        """,
        agent=create_competitor_intel_agent(),
        context=context,
        expected_output="""
        Competitive analysis for EACH product:
        {{
          "products": [
            {{
              "product_name": "LED Strip Lights RGB 5M",
              "analysis": {{
                "number_of_competitors": 25-50,
                "market_saturation_level": "Medium-High",
                "differentiation_opportunities": ["Better mobile app", "Energy efficiency", "Custom lengths"],
                "barrier_to_entry": "Moderate - requires reliable supplier and good marketing",
                "recommendation": "Yes - if differentiated with unique features"
              }}
            }},
            ... (other products)
          ]
        }}
        """
    )
