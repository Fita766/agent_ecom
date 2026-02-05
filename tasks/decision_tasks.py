from crewai import Task
from agents.decision_agents import (
    create_scoring_engine_agent,
    create_decision_maker_agent
)


def create_product_scoring_task(context):
    """Task 9: Calculate comprehensive product scores"""
    return Task(
        description="""
        Calculate comprehensive scores for each product across 6 dimensions:
        
        CRITICAL: Extract data from ALL previous tasks in the context:
        - Task 1: Product names, engagement metrics (likes, comments, shares)
        - Task 2: Market size, competition level, target demographics
        - Task 3: Number of competitors, market saturation
        - Task 4: Supplier data, shipping costs, shipping times
        - Task 5: Competitor prices, price ranges
        - Task 6: Review analysis, sentiment scores, pros/cons
        - Task 7: Google Trends scores, trend direction, search volume
        - Task 8: Pricing strategy, profit margins
        
        For EACH product from Task 1:
        
        Scoring dimensions (each 0-100):
        1. Trend Score (25% weight): 
           - Use Google Trends score from Task 7
           - Use TikTok views/engagement from Task 1
           - Use trend direction (Rising=high, Stable=medium, Declining=low)
        
        2. Profit Score (25% weight):
           - Use profit_margin_percent from Task 8 (pricing strategy)
           - Higher margin = higher score
           - 30% margin = 70 points, 50% margin = 100 points
        
        3. Competition Score (15% weight): 
           - Use competition_level from Task 2 (Low=high score, High=low score)
           - Use number_of_competitors from Task 3
           - Inverse: Lower competition = higher score
        
        4. Demand Score (20% weight):
           - Use market_size from Task 2 (Huge=100, Large=80, Medium=60, Small=40)
           - Use search_volume from Task 7
           - Use engagement metrics from Task 1
        
        5. Quality Score (10% weight):
           - Use review sentiment from Task 6
           - Use average_rating if available
           - Deduct points for red_flags
        
        6. Shipping Score (5% weight):
           - Use shipping_time_days from Task 4 (lower is better)
           - Use shipping_cost (lower is better)
           - Use estimated_weight_category (under 5kg = good)
        
        Formula:
        overall_score = (trend*0.25 + profit*0.25 + (100-competition)*0.15 + demand*0.20 + quality*0.10 + shipping*0.05)
        
        IMPORTANT:
        - Process ALL products, not just one
        - Use REAL data from context, not assumptions
        - If data is missing, use best estimate but note it
        - Return JSON format with all products
        
        Return complete scoring for EACH product in JSON format.
        """,
        agent=create_scoring_engine_agent(),
        context=context,
        expected_output="""
        JSON object with scores for each product:
        {
          "products": [
            {
              "product_name": "Product Name",
              "scores": {
                "trend_score": 75,
                "profit_score": 70,
                "competition_score": 30,
                "demand_score": 85,
                "quality_score": 80,
                "shipping_score": 90
              },
              "overall_score": 73,
              "reasoning": {
                "trend_score": "Detailed explanation...",
                "profit_score": "Detailed explanation...",
                ...
              },
              "strengths": ["List of strengths"],
              "weaknesses": ["List of weaknesses"]
            },
            ...
          ]
        }
        """
    )


def create_final_decision_task(context):
    """Task 10: Make final GO/NO-GO decision"""
    return Task(
        description="""
        Make final approval decision for each product based on comprehensive analysis:
        
        CRITICAL: Extract data from ALL previous tasks in the context:
        - Task 9 (Scoring): overall_score for each product
        - Task 8 (Pricing): profit_margin_percent for each product
        - Task 6 (Reviews): red_flags, sentiment analysis
        - Task 1 (Trend Discovery): estimated_weight_category
        - Task 7 (Trend Validation): trend_longevity_prediction, trend_direction
        - Task 2 (Market Analysis): target_demographics, target_geographies
        - Task 8 (Duplicate Check): is_duplicate for each product
        
        For EACH product from Task 1, check ALL approval criteria:
        
        Approval criteria (Goal: Identify potential winners, be lenient on missing data):
        1. Overall score >= 60/100 (lowered from 75 to allow more candidates)
        2. Profit margin >= 20% (lowered from 30%)
        3. No major quality red flags (from Task 6 review analysis)
        4. Product weight: IGNORE weight criteria (as requested)
        5. Trend: If prediction exists, must not be "Dead". If missing, assume "Stable".
        6. Target market identified (from Task 2)
        7. Not a duplicate (from Task 8)
        
        IMPORTANT:
        - Process ALL products from Task 1
        - For each product, check criteria
        - If data is missing (e.g. weight, trend prediction), DO NOT REJECT. specific "Data not available" counts as PASS for that criterion.
        - Only reject if there are clear identifying RED FLAGS (e.g. extremely low score < 40, explicitly "Dead" trend).
        - List which criteria passed and which failed
        
        If data is missing for a criterion, mark it as PASSED (Benefit of the doubt).
        
        Return final decision for EACH product in JSON format.
        """,
        agent=create_decision_maker_agent(),
        context=context,
        expected_output="""
        JSON object with final decision for each product:
        {
          "Product Name 1": {
            "is_approved": true,
            "rejection_reason": null,
            "approval_criteria_met": ["1", "2", "3", "4", "5", "6", "7"],
            "approval_criteria_failed": [],
            "criteria_details": {
              "1": {"met": true, "value": 78, "required": 75, "reason": "Overall score meets threshold"},
              "2": {"met": true, "value": 35, "required": 30, "reason": "Profit margin exceeds minimum"},
              ...
            },
            "recommendation": "GO - All criteria met"
          },
          "Product Name 2": {
            "is_approved": false,
            "rejection_reason": "Overall score too low (73 < 75) and profit margin insufficient (25% < 30%)",
            "approval_criteria_met": ["3", "4", "5", "6", "7"],
            "approval_criteria_failed": ["1", "2"],
            "criteria_details": {
              "1": {"met": false, "value": 73, "required": 75, "reason": "Overall score below threshold"},
              "2": {"met": false, "value": 25, "required": 30, "reason": "Profit margin below minimum"},
              ...
            },
            "recommendation": "NO-GO - Criteria 1 and 2 failed"
          },
          ...
        }
        """
    )
