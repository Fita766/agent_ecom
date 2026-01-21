from crewai import Task
from agents.management_agents import create_report_generator_agent
import json
from datetime import datetime
from pathlib import Path


def create_final_report_task(context):
    """Task 15: Generate comprehensive final report"""
    return Task(
        description="""
        Create detailed, professional report summarizing entire workflow:
        
        Report sections:
        1. Executive Summary
           - Total products analyzed
           - Products approved/rejected
           - Key findings
        
        2. Product Analysis Details
           - For each product: name, category, scores, decision
           - Market analysis summary
           - Pricing strategy summary
           - Review analysis summary
        
        3. Approved Products
           - Complete details for GO products
           - Shopify URLs
           - Next steps
        
        4. Rejected Products
           - Reasons for rejection
           - What would be needed for approval
        
        5. Recommendations
           - Best products to focus on
           - Marketing suggestions
           - Optimization opportunities
        
        6. Metrics & Statistics
           - Average scores
           - Approval rate
           - Top performing categories
        
        Save report as:
        - JSON file (structured data)
        - Markdown file (human-readable)
        - Store in output/ directory
        
        Return report file paths and summary.
        """,
        agent=create_report_generator_agent(),
        context=context,
        expected_output="""
        Final report:
        - report_json_path
        - report_markdown_path
        - executive_summary
        - total_products_analyzed
        - products_approved_count
        - products_rejected_count
        - top_recommended_products (list)
        - report_generated_at (timestamp)
        """
    )
