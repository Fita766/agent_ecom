from crewai import Task
from agents.scraper_agents import (
    create_aliexpress_scraper_agent,
    create_amazon_scraper_agent,
    create_pricing_strategist_agent
)


def create_aliexpress_sourcing_task(context):
    """Task 4: Find suppliers on AliExpress"""
    return Task(
        description="""
        For each product, find suppliers on AliExpress:
        
        Search AliExpress for the product and retrieve:
        1. Top 5 suppliers by rating and orders
        2. Product prices (in USD)
        3. Supplier ratings (must be 4.0+)
        4. Total orders/sales
        5. Shipping costs and times
        6. Product availability (stock)
        7. Estimated weight and dimensions
        
        Prioritize suppliers with:
        - Rating >= 4.5/5
        - 100+ orders
        - Free or low shipping
        - Fast shipping (under 30 days)
        
        Identify the BEST supplier for each product.
        """,
        agent=create_aliexpress_scraper_agent(),
        context=context,
        expected_output="""
        For each product, list of suppliers:
        - platform: AliExpress
        - supplier_name
        - price
        - rating
        - total_orders
        - shipping_cost
        - shipping_time_days
        - product_url
        
        Plus: best_supplier (the optimal choice)
        """
    )


def create_amazon_pricing_task(context):
    """Task 5: Get competitor pricing from Amazon"""
    return Task(
        description="""
        For each product, scrape Amazon to find competitor prices:
        
        Search Amazon for similar/identical products:
        1. Get top 5 competitor listings
        2. Extract prices
        3. Note ratings and review counts
        4. Identify price range (min-max)
        
        This data will help determine competitive retail pricing.
        Look for products with similar features/specs.
        
        Return price range and average competitor price.
        """,
        agent=create_amazon_scraper_agent(),
        context=context,
        expected_output="""
        Amazon competitor data per product:
        - competitor_listings (list of 5)
        - price_range_min
        - price_range_max
        - average_price
        """
    )


def create_pricing_strategy_task(context):
    """Task 6: Calculate optimal pricing strategy"""
    return Task(
        description="""
        Calculate optimal pricing strategy for each product:
        
        1. Calculate total cost (supplier price + shipping from AliExpress)
        2. Analyze competitor prices from Amazon
        3. Determine optimal retail price with minimum 30% margin
        4. Account for geographic pricing variations (US vs EU)
        5. Calculate profit margin percentage
        6. Calculate profit amount per unit
        
        Pricing strategy must ensure:
        - Minimum 30% profit margin
        - Competitive with market prices
        - Account for shipping costs
        - Consider geographic markets (US, EU, FR, etc)
        
        Return pricing strategy for each product.
        """,
        agent=create_pricing_strategist_agent(),
        context=context,
        expected_output="""
        Pricing strategy per product:
        - cost_price
        - shipping_cost
        - total_cost
        - suggested_retail_price
        - profit_margin_percent
        - profit_amount
        - competitive_price_range_min
        - competitive_price_range_max
        - recommended_geography_pricing (dict with prices per geography)
        """
    )
