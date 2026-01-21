from crewai import Task
from agents.validation_agents import (
    create_review_analyzer_agent,
    create_trend_validator_agent,
    create_duplicate_checker_agent
)
from utils.database import ProductDatabase


def create_review_analysis_task(context):
    """Task 6: Analyze customer reviews for quality assessment"""
    return Task(
        description="""
        For each product candidate, analyze customer reviews to assess quality:
        
        1. Extract reviews from Amazon and AliExpress supplier pages
        2. Perform sentiment analysis on reviews
        3. Identify common complaints and praise points
        4. Calculate average rating
        5. Identify red flags (quality issues, shipping problems, etc)
        6. Extract main pros and cons
        
        Focus on:
        - Review sentiment (positive/negative/neutral)
        - Recurring issues mentioned
        - Product quality indicators
        - Shipping and delivery feedback
        - Customer satisfaction trends
        
        Return comprehensive review analysis for each product.
        """,
        agent=create_review_analyzer_agent(),
        context=context,
        expected_output="""
        Review analysis per product:
        - total_reviews
        - average_rating
        - sentiment_score (-1 to 1)
        - positive_count
        - negative_count
        - neutral_count
        - main_pros (list)
        - main_cons (list)
        - red_flags (list of critical issues)
        """
    )


def create_trend_validation_task(context):
    """Task 7: Validate trends using Google Trends and social metrics"""
    return Task(
        description="""
        Validate product trends using data sources:
        
        1. Use Google Trends to check search volume and trend direction
        2. Analyze TikTok engagement metrics (views, likes, shares)
        3. Check Pinterest save/repin trends
        4. Determine if trend is Rising, Stable, or Declining
        5. Predict trend longevity (viral fad vs sustainable trend)
        6. Identify geographic markets with highest interest
        
        For each product:
        - Get Google Trends score (0-100)
        - Analyze trend direction over last 3 months
        - Check if trend is sustainable or dying out
        - Identify rising related queries
        - Assess social media momentum
        
        Return trend validation results.
        """,
        agent=create_trend_validator_agent(),
        context=context,
        expected_output="""
        Trend validation per product:
        - google_trends_score (0-100)
        - trend_direction (Rising/Stable/Declining)
        - tiktok_views
        - pinterest_saves
        - search_volume_monthly (estimated)
        - trend_longevity_prediction (Short-term fad / Medium-term / Long-term trend)
        - top_geographic_markets (list)
        """
    )


def create_duplicate_check_task(context):
    """Task 8: Check for duplicate products in database"""
    return Task(
        description="""
        Check if product candidates already exist in our database:
        
        1. Compare product names using fuzzy matching
        2. Check product images for visual similarity
        3. Compare product specifications
        4. Determine similarity score (0-1)
        5. Flag duplicates if similarity >= 0.8
        
        Use the ProductDatabase to check existing products.
        If duplicate found, mark product and provide existing product ID.
        
        Return duplicate check results for each product.
        """,
        agent=create_duplicate_checker_agent(),
        context=context,
        expected_output="""
        Duplicate check per product:
        - is_duplicate (boolean)
        - existing_product_id (if duplicate found)
        - similarity_score (0-1)
        - reason (explanation)
        """
    )
