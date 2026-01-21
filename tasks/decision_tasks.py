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
        
        Scoring dimensions (each 0-100):
        1. Trend Score (25% weight): Based on Google Trends, social engagement, trend direction
        2. Profit Score (25% weight): Based on profit margin, pricing competitiveness, cost structure
        3. Competition Score (15% weight): Lower competition = higher score (inverse)
        4. Demand Score (20% weight): Based on market size, search volume, engagement metrics
        5. Quality Score (10% weight): Based on review ratings, sentiment, red flags
        6. Shipping Score (5% weight): Based on weight, shipping time, shipping cost
        
        For each product:
        - Calculate each dimension score (0-100)
        - Apply weights to get overall_score (0-100)
        - Provide detailed reasoning for each score
        - Highlight strengths and weaknesses
        
        Formula:
        overall_score = (trend*0.25 + profit*0.25 + (100-competition)*0.15 + demand*0.20 + quality*0.10 + shipping*0.05)
        
        Return complete scoring for each product.
        """,
        agent=create_scoring_engine_agent(),
        context=context,
        expected_output="""
        Product scores per product:
        - trend_score (0-100)
        - profit_score (0-100)
        - competition_score (0-100, lower is better)
        - demand_score (0-100)
        - quality_score (0-100)
        - shipping_score (0-100)
        - overall_score (0-100, weighted average)
        - reasoning (detailed explanation for each score)
        """
    )


def create_final_decision_task(context):
    """Task 10: Make final GO/NO-GO decision"""
    return Task(
        description="""
        Make final approval decision for each product based on comprehensive analysis:
        
        Review all data:
        - Market analysis
        - Pricing strategy and margins
        - Review analysis and quality indicators
        - Trend validation
        - Product scores
        - Duplicate check results
        
        Approval criteria (ALL must be met):
        1. Overall score >= 75/100
        2. Profit margin >= 30%
        3. No major quality red flags
        4. Product weight < 5kg
        5. Trend is sustainable (not a dying fad)
        6. Clear target market identified
        7. Not a duplicate
        
        For each product:
        - Make GO or NO-GO decision
        - Provide detailed reasoning
        - If NO-GO, explain exactly why (which criteria failed)
        - If GO, confirm all criteria are met
        
        Return final decision for each product.
        """,
        agent=create_decision_maker_agent(),
        context=context,
        expected_output="""
        Final decision per product:
        - is_approved (boolean)
        - rejection_reason (if NO-GO, explain why)
        - approval_criteria_met (list of criteria that passed)
        - approval_criteria_failed (list of criteria that failed)
        - recommendation (GO/NO-GO with reasoning)
        """
    )
