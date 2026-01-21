from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


class AmazonScraperInput(BaseModel):
    """Input for Amazon Scraper"""
    product_name: str = Field(description="Product name to search")
    max_results: int = Field(default=5, description="Max products to retrieve")


class AmazonScraperTool(BaseTool):
    name: str = "Amazon Competitor Scraper"
    description: str = """
    Scrape Amazon to find competitor prices, ratings, and reviews.
    Returns product URLs, prices, ratings, review counts.
    Use this to analyze competitive pricing on Amazon.
    """
    args_schema: Type[BaseModel] = AmazonScraperInput
    
    def _run(self, product_name: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search Amazon for competitor products"""
        results: List[Dict[str, Any]] = []
        ua = UserAgent()

        try:
            search_url = "https://www.amazon.com/s"
            params = {"k": product_name}
            headers = {
                "User-Agent": ua.random,
                "Accept-Language": "en-US,en;q=0.9",
            }

            response = requests.get(search_url, params=params, headers=headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                items = soup.find_all("div", {"data-component-type": "s-search-result"})[:max_results]

                for item in items:
                    try:
                        title = item.find("h2", {"class": "s-line-clamp-2"})
                        price = item.find("span", {"class": "a-price-whole"})
                        rating = item.find("span", {"class": "a-icon-alt"})
                        reviews = item.find("span", {"class": "a-size-base"})

                        results.append(
                            {
                                "platform": "Amazon",
                                "product_name": title.get_text(strip=True) if title else product_name,
                                "price": float(re.sub(r"[^\d.]", "", price.get_text())) if price else 0.0,
                                "rating": float(re.findall(r"\d+\.\d+", rating.get_text())[0]) if rating else 0.0,
                                "total_reviews": re.sub(r"[^\d]", "", reviews.get_text()) if reviews else "0",
                            }
                        )
                    except Exception:
                        continue

                if not results:
                    results.append(
                        {
                            "platform": "Amazon",
                            "product_name": product_name,
                            "price": 29.99,
                            "rating": 4.3,
                            "total_reviews": "1245",
                            "note": "Mock data - Amazon requires anti-bot measures",
                        }
                    )

        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            results.append({"error": str(e)})

        return results
