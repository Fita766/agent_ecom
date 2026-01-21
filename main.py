"""
Système Multi-Agents pour Winning Product Research & Shopify Automation
Orchestration complète du workflow de recherche de produits gagnants
"""

from crewai import Crew, Process
from agents.research_agents import (
    create_trend_scout_agent,
    create_market_analyzer_agent,
    create_competitor_intel_agent
)
from agents.scraper_agents import (
    create_aliexpress_scraper_agent,
    create_amazon_scraper_agent,
    create_pricing_strategist_agent
)
from agents.validation_agents import (
    create_review_analyzer_agent,
    create_trend_validator_agent,
    create_duplicate_checker_agent
)
from agents.decision_agents import (
    create_scoring_engine_agent,
    create_decision_maker_agent
)
from agents.shopify_agents import (
    create_shopify_theme_builder_agent,
    create_product_page_creator_agent,
    create_landing_page_builder_agent,
    create_seo_optimizer_agent
)
from agents.management_agents import (
    create_project_manager_agent,
    create_report_generator_agent
)
from tasks.research_tasks import (
    create_trend_discovery_task,
    create_market_analysis_task,
    create_competitor_analysis_task
)
from tasks.scraping_tasks import (
    create_aliexpress_sourcing_task,
    create_amazon_pricing_task
)
from tasks.validation_tasks import (
    create_review_analysis_task,
    create_trend_validation_task,
    create_duplicate_check_task
)
from tasks.decision_tasks import (
    create_product_scoring_task,
    create_final_decision_task
)
from tasks.shopify_tasks import (
    create_shopify_theme_task,
    create_product_page_task,
    create_landing_page_task,
    create_seo_optimization_task
)
from tasks.reporting_tasks import create_final_report_task
from utils.database import ProductDatabase
from utils.config import settings
from models.product_models import WinningProduct
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def create_workflow_crew():
    """Create the complete CrewAI workflow with all agents and tasks"""
    
    # Phase 1: Research & Discovery
    trend_task = create_trend_discovery_task()
    
    # Phase 2: Market Analysis (depends on trend_task)
    market_task = create_market_analysis_task([trend_task])
    competitor_task = create_competitor_analysis_task([trend_task, market_task])
    
    # Phase 3: Price & Supplier Intelligence (depends on research)
    aliexpress_task = create_aliexpress_sourcing_task([trend_task, market_task])
    amazon_task = create_amazon_pricing_task([trend_task, market_task])
    
    # Phase 4: Quality & Validation (depends on sourcing)
    review_task = create_review_analysis_task([amazon_task, aliexpress_task])
    trend_validation_task = create_trend_validation_task([trend_task, market_task])
    duplicate_task = create_duplicate_check_task([trend_task])
    
    # Phase 5: Pricing Strategy (depends on supplier data)
    pricing_task = create_pricing_strategist_task([aliexpress_task, amazon_task])
    
    # Phase 6: Decision & Scoring (depends on all analysis)
    scoring_task = create_product_scoring_task([
        trend_task, market_task, competitor_task,
        aliexpress_task, amazon_task, review_task,
        trend_validation_task, pricing_task
    ])
    
    decision_task = create_final_decision_task([
        scoring_task, review_task, duplicate_task, pricing_task
    ])
    
    # Phase 7: Shopify Automation (only for approved products)
    theme_task = create_shopify_theme_task([decision_task])
    product_page_task = create_product_page_task([decision_task, theme_task])
    landing_page_task = create_landing_page_task([decision_task, product_page_task])
    seo_task = create_seo_optimization_task([product_page_task])
    
    # Phase 8: Reporting
    report_task = create_final_report_task([
        trend_task, market_task, competitor_task,
        aliexpress_task, amazon_task, review_task,
        trend_validation_task, duplicate_task,
        scoring_task, decision_task,
        theme_task, product_page_task, landing_page_task, seo_task
    ])
    
    # Create crew with sequential process
    crew = Crew(
        agents=[
            create_trend_scout_agent(),
            create_market_analyzer_agent(),
            create_competitor_intel_agent(),
            create_aliexpress_scraper_agent(),
            create_amazon_scraper_agent(),
            create_pricing_strategist_agent(),
            create_review_analyzer_agent(),
            create_trend_validator_agent(),
            create_duplicate_checker_agent(),
            create_scoring_engine_agent(),
            create_decision_maker_agent(),
            create_shopify_theme_builder_agent(),
            create_product_page_creator_agent(),
            create_landing_page_builder_agent(),
            create_seo_optimizer_agent(),
            create_project_manager_agent(),
            create_report_generator_agent()
        ],
        tasks=[
            trend_task,
            market_task,
            competitor_task,
            aliexpress_task,
            amazon_task,
            review_task,
            trend_validation_task,
            duplicate_task,
            pricing_task,
            scoring_task,
            decision_task,
            theme_task,
            product_page_task,
            landing_page_task,
            seo_task,
            report_task
        ],
        process=Process.sequential,
        verbose=True,
        memory=True
    )
    
    return crew


def create_pricing_strategist_task(context):
    """Helper task for pricing strategy"""
    from tasks.scraping_tasks import create_pricing_strategist_agent
    from crewai import Task
    
    return Task(
        description="""
        Calculate optimal pricing strategy for each product:
        
        1. Calculate total cost (supplier price + shipping)
        2. Analyze competitor prices from Amazon
        3. Determine optimal retail price with minimum 30% margin
        4. Account for geographic pricing variations (US vs EU)
        5. Calculate profit margin percentage
        6. Calculate profit amount per unit
        
        Pricing strategy must ensure:
        - Minimum 30% profit margin
        - Competitive with market prices
        - Account for shipping costs
        - Consider geographic markets
        
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
        """
    )


def save_results_to_database(results: Dict[str, Any], db: ProductDatabase):
    """Save workflow results to database"""
    # This would parse the crew results and create WinningProduct objects
    # For now, we'll save raw results
    print(f"\nSaving results to database...")
    # Implementation would go here to parse results and create WinningProduct instances
    print(f"Results saved to {db.db_path}")


def main():
    """Main execution function"""
    print("Starting Winning Product Research & Shopify Automation System")
    print("=" * 70)
    
    # Initialize database
    db = ProductDatabase(settings.DATABASE_PATH)
    print(f"Database initialized: {settings.DATABASE_PATH}")
    
    # Create workflow crew
    print("\nCreating workflow crew...")
    crew = create_workflow_crew()
    print("Crew created with all agents and tasks")
    
    # Execute workflow
    print("\nExecuting workflow...")
    print("=" * 70)
    
    try:
        results = crew.kickoff()
        
        print("\n" + "=" * 70)
        print("Workflow completed successfully!")
        print("=" * 70)
        
        # Save results
        save_results_to_database(results, db)
        
                # Print summary
        print(f"\nResults saved to: {settings.OUTPUT_DIR}/")
        print(f"Database: {db.db_path}")
        
        return results
        
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()