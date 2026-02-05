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
from agents.marketing_agents import (
    create_marketing_strategy_agent,
    create_tiktok_ads_agent,
    create_google_ads_agent,
    create_facebook_ads_agent
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
from tasks.marketing_tasks import (
    create_marketing_strategy_task,
    create_tiktok_ads_campaign_task,
    create_google_ads_campaign_task,
    create_facebook_ads_campaign_task
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
    from tasks.scraping_tasks import create_pricing_strategy_task
    pricing_task = create_pricing_strategy_task([aliexpress_task, amazon_task])
    
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
    
    # Phase 8: Marketing Strategy & Campaigns (depends on product pages and reviews)
    marketing_strategy_task = create_marketing_strategy_task([
        decision_task, review_task, scoring_task, 
        product_page_task, market_task
    ])
    tiktok_ads_task = create_tiktok_ads_campaign_task([
        decision_task, marketing_strategy_task, trend_task
    ])
    google_ads_task = create_google_ads_campaign_task([
        decision_task, marketing_strategy_task, seo_task
    ])
    facebook_ads_task = create_facebook_ads_campaign_task([
        decision_task, marketing_strategy_task, product_page_task
    ])
    
    # Phase 9: Reporting
    report_task = create_final_report_task([
        trend_task, market_task, competitor_task,
        aliexpress_task, amazon_task, review_task,
        trend_validation_task, duplicate_task,
        scoring_task, decision_task,
        theme_task, product_page_task, landing_page_task, seo_task,
        marketing_strategy_task, tiktok_ads_task, google_ads_task, facebook_ads_task
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
            create_marketing_strategy_agent(),
            create_tiktok_ads_agent(),
            create_google_ads_agent(),
            create_facebook_ads_agent(),
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
            marketing_strategy_task,
            tiktok_ads_task,
            google_ads_task,
            facebook_ads_task,
            report_task
        ],
        process=Process.sequential,
        verbose=True,
        memory=True
    )
    
    return crew


def save_results_to_database(results: Dict[str, Any], db: ProductDatabase):
    """Save workflow results to database and files"""
    from datetime import datetime
    import sqlite3
    from uuid import uuid4
    
    print(f"\nSaving results to database and files...")
    
    # Convertir les résultats en string pour sauvegarde
    if isinstance(results, dict):
        result_text = results.get('raw', str(results))
        result_dict = results
    else:
        result_text = str(results)
        result_dict = {"raw_output": result_text}
    
    # 1. Sauvegarder dans un fichier JSON avec timestamp (structure complète)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_file = Path(settings.OUTPUT_DIR) / f"results_{timestamp}.json"
    json_file.parent.mkdir(exist_ok=True)
    
    json_data = {
        "timestamp": datetime.now().isoformat(),
        "workflow_summary": {
            "total_tasks": result_dict.get("total_tasks", 0),
            "tasks_with_output": result_dict.get("tasks_with_output", 0),
            "final_output_available": bool(result_dict.get("final_output"))
        },
        "final_output": result_dict.get("final_output", ""),
        "task_results": {}
    }
    
    # Ajouter les résultats détaillés de chaque tâche
    if "task_details" in result_dict:
        for task_detail in result_dict["task_details"]:
            task_key = f"task_{task_detail['task_number']}_{task_detail['agent']}"
            json_data["task_results"][task_key] = {
                "task_number": task_detail["task_number"],
                "agent": task_detail["agent"],
                "description": task_detail["description"],
                "output": task_detail["output"]
            }
    
    # Ajouter aussi les résultats bruts pour compatibilité
    json_data["raw_results"] = result_text
    json_data["all_task_outputs"] = result_dict.get("tasks", {})
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"  -> JSON saved: {json_file}")
    
    # 2. Sauvegarder dans un fichier texte lisible
    txt_file = Path(settings.OUTPUT_DIR) / f"results_{timestamp}.txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"WORKFLOW RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(result_text)
        f.write("\n\n" + "=" * 80 + "\n")
    
    print(f"  -> Text file saved: {txt_file}")
    
    # 3. Sauvegarder le dernier résultat (écrase le précédent)
    last_file = Path(settings.OUTPUT_DIR) / "last_results.txt"
    with open(last_file, "w", encoding="utf-8") as f:
        f.write(result_text)
    print(f"  -> Last results saved: {last_file}")
    
    # 4. Sauvegarder dans la base de données
    try:
        conn = sqlite3.connect(db.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO products (id, name, category, data, overall_score, is_approved, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid4()),
            f"Workflow Run - {timestamp}",
            "other",
            json.dumps(json_data, default=str),
            0.0,
            1 if "approved" in result_text.lower() else 0,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        print(f"  -> Database saved: {db.db_path}")
    except Exception as e:
        print(f"  -> Error saving to database: {e}")
    
    print(f"\nResults saved to: {settings.OUTPUT_DIR}/")
    print(f"Database: {db.db_path}")
    print(f"\n[INFO] Total tasks processed: {result_dict.get('total_tasks', 0)}")
    print(f"[INFO] Tasks with output: {result_dict.get('tasks_with_output', 0)}")


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
        
        # TOUJOURS extraire les résultats de toutes les tâches pour créer un rapport complet
        print("\n[INFO] Extracting results from all tasks...")
        all_task_results = {}
        task_details = []
        
        # Récupérer les résultats des tâches depuis le crew
        if hasattr(crew, 'tasks'):
            for i, task in enumerate(crew.tasks):
                task_name = task.description[:100] if hasattr(task, 'description') and task.description else f"Task {i+1}"
                task_agent = task.agent.role if hasattr(task, 'agent') and hasattr(task.agent, 'role') else "Unknown Agent"
                
                task_output = None
                if hasattr(task, 'output') and task.output:
                    task_output = str(task.output)
                elif hasattr(task, 'result') and task.result:
                    task_output = str(task.result)
                
                if task_output:
                    all_task_results[f"Task_{i+1}_{task_agent}"] = task_output
                    task_details.append({
                        "task_number": i + 1,
                        "agent": task_agent,
                        "description": task_name,
                        "output": task_output
                    })
        
        # Créer un rapport complet avec tous les résultats
        final_output = str(results) if results else ""
        
        # Construire le rapport complet
        report_text = "=" * 80 + "\n"
        report_text += "WORKFLOW COMPLETE REPORT\n"
        report_text += "=" * 80 + "\n\n"
        
        # Ajouter le résultat final si disponible
        if final_output and final_output.strip() and final_output != "None":
            report_text += "FINAL WORKFLOW OUTPUT:\n"
            report_text += "-" * 80 + "\n"
            report_text += final_output + "\n\n"
        
        # Ajouter tous les résultats des tâches
        if task_details:
            report_text += "=" * 80 + "\n"
            report_text += "DETAILED TASK RESULTS\n"
            report_text += "=" * 80 + "\n\n"
            
            for task_detail in task_details:
                report_text += f"\n{'='*80}\n"
                report_text += f"TASK {task_detail['task_number']}: {task_detail['agent']}\n"
                report_text += f"{'='*80}\n"
                report_text += f"Description: {task_detail['description']}\n"
                report_text += f"{'-'*80}\n"
                report_text += f"Output:\n{task_detail['output']}\n"
                report_text += f"\n{'='*80}\n\n"
        else:
            report_text += "\n[WARNING] No task outputs found. Check console logs above.\n\n"
        
        # Créer la structure de résultats complète
        results_dict = {
            "raw": report_text,
            "final_output": final_output,
            "tasks": all_task_results,
            "task_details": task_details,
            "total_tasks": len(task_details),
            "tasks_with_output": len([t for t in task_details if t.get('output')])
        }
        
        # Save results
        save_results_to_database(results_dict, db)
        
        # Print summary
        print(f"\n" + "=" * 70)
        print(f"All results saved successfully!")
        print(f"Check: {settings.OUTPUT_DIR}/last_results.txt for quick access")
        print(f"Check: {settings.OUTPUT_DIR}/results_*.json for detailed JSON")
        print("=" * 70)
        
        return results
        
    except Exception as e:
        print(f"\nError during workflow execution: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()
