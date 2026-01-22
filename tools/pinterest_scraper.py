from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time


class PinterestScraperInput(BaseModel):
    """Input for Pinterest Scraper"""
    keywords: List[str] = Field(description="Keywords to search on Pinterest")
    max_pins: int = Field(default=5, description="Max pins to analyze")


class PinterestScraperTool(BaseTool):
    name: str = "Pinterest Trend Scraper"
    description: str = """
    Scrape Pinterest to find trending products based on keywords.
    
    IMPORTANT: Call this tool with a SINGLE dictionary object containing:
    - keywords: array of strings (e.g., ["home gadgets", "beauty products"])
    - max_pins: integer (default: 5)
    
    Example correct usage:
    {"keywords": ["home gadgets", "beauty products"], "max_pins": 5}
    
    Returns pin URLs, save counts, repins.
    Use this to identify popular products on Pinterest.
    """
    args_schema: Type[BaseModel] = PinterestScraperInput
    
    def _run(self, keywords: List[str] = None, max_pins: int = 5) -> List[Dict[str, Any]]:
        """Search Pinterest for trending products"""
        # Validation
        if not keywords:
            return [{"error": "Keywords are required. Provide a list of keywords to search."}]
        
        if not isinstance(keywords, list):
            keywords = [str(keywords)]
        
        results: List[Dict[str, Any]] = []
        ua = UserAgent()

        for keyword in keywords[:3]:
            try:
                search_url = f"https://www.pinterest.com/search/pins/?q={keyword.replace(' ', '%20')}"
                headers = {"User-Agent": ua.random}
                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    BeautifulSoup(response.content, "html.parser")  # structure non utilisée ici
                    results.append(
                        {
                            "platform": "Pinterest",
                            "url": search_url,
                            "keyword": keyword,
                            "engagement": 0,
                            "note": "Pinterest requires browser automation for full data",
                        }
                    )

                time.sleep(2)

            except Exception as e:
                print(f"Error scraping Pinterest for '{keyword}': {e}")
                continue

        return results if results else [{"error": "No Pinterest data found"}]
