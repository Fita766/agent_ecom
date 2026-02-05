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
        - image_url
        
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
        - competitor_listings (list of 5, including product_url and image_url)
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
        
        CRITICAL: You MUST access data from previous tasks in the context:
        - Task 4 (AliExpress sourcing): Look for "suppliers" array and "best_supplier" field
        - Task 5 (Amazon pricing): Look for "competitor_listings", "price_range_min", "price_range_max", "average_price"
        
        STEPS:
        1. Extract product names from Task 1 (trend_task output)
        2. For EACH product, find its data in Task 4 and Task 5 outputs
        3. Extract supplier data from Task 4:
           - Find the product in the Task 4 output
           - Get "best_supplier" name
           - Find that supplier in the "suppliers" array
           - Extract "price" and "shipping_cost" from that supplier
           - Calculate: total_cost = price + shipping_cost
        
        4. Extract competitor data from Task 5:
           - Find the product in Task 5 output
           - Extract "price_range_min", "price_range_max", "average_price"
        
        5. Calculate pricing:
           - Minimum retail price = total_cost / 0.70 (ensures 30% margin)
           - Check if this price is competitive (within price_range_min to price_range_max)
           - If too high, adjust to be competitive but maintain 30%+ margin
           - Final retail price = max(minimum_retail_price, competitive_price)
        
        6. Calculate metrics:
           - profit_margin_percent = ((retail_price - total_cost) / retail_price) * 100
           - profit_amount = retail_price - total_cost
        
        IMPORTANT: 
        - Process ALL products from Task 1, not just one
        - Use REAL numbers from the context, not placeholders
        - If data is missing for a product, note it but still calculate what you can
        - Return JSON format with all products
        
        Return detailed pricing strategy with ACTUAL CALCULATED NUMBERS for EACH product.
        """,
        agent=create_pricing_strategist_agent(),
        context=context,
        expected_output="""
        JSON object with pricing strategy for each product:
        {
          "Product Name 1": {
            "supplier_data": {
              "best_supplier": "Supplier Name",
              "cost_price": 12.99,
              "shipping_cost": 4.95,
              "total_cost": 17.94
            },
            "pricing": {
              "suggested_retail_price": 25.63,
              "profit_margin_percent": 30.0,
              "profit_amount": 7.69
            },
            "competitive_analysis": {
              "price_range_min": 15.99,
              "price_range_max": 24.99,
              "average_competitor_price": 20.96
            }
          },
          "Product Name 2": { ... }
        }
        """
    )
