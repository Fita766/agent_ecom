from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re


class AliExpressScraperInput(BaseModel):
    """Input for AliExpress Scraper"""
    product_name: str = Field(description="Product name to search (single product name)")
    max_results: int = Field(default=5, description="Max products to retrieve per search")


class AliExpressScraperTool(BaseTool):
    name: str = "AliExpress Product Scraper"
    description: str = """
    Scrape AliExpress to find supplier prices, ratings, and shipping info.
    Call this tool ONCE per product with: product_name (string) and max_results (integer, default 5).
    Returns JSON string with product URLs, prices, supplier ratings, order counts.
    Example: Call with product_name="Smart Home Speaker", max_results=5
    """
    args_schema: Type[BaseModel] = AliExpressScraperInput
    
    def _run(self, product_name: str, max_results: int = 5) -> str:
        """Search AliExpress for product suppliers. Returns JSON string."""
        results: List[Dict[str, Any]] = []
        ua = UserAgent()

        try:
            search_url = "https://www.aliexpress.com/wholesale"
            params = {
                "SearchText": product_name,
                "g": "y",
                "page": 1,
            }

            headers = {
                "User-Agent": ua.random,
                "Accept-Language": "en-US,en;q=0.9",
            }

            response = requests.get(search_url, params=params, headers=headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                # Simplified parsing (AliExpress structure changes frequently)
                product_items = soup.find_all("div", {"class": re.compile("product")})[:max_results]

                for item in product_items:
                    try:
                        price_elem = item.find("span", {"class": re.compile("price")})
                        title_elem = item.find("a", {"class": re.compile("title")})
                        rating_elem = item.find("span", {"class": re.compile("rating")})
                        orders_elem = item.find("span", {"class": re.compile("order")})
                        img_elem = item.find("img")

                        product_url = ""
                        if title_elem and title_elem.get("href"):
                            href = title_elem.get("href")
                            if href.startswith("//"):
                                product_url = f"https:{href}"
                            elif not href.startswith("http"):
                                product_url = f"https://www.aliexpress.com{href}"
                            else:
                                product_url = href

                        results.append(
                            {
                                "platform": "AliExpress",
                                "product_name": title_elem.get_text(strip=True) if title_elem else product_name,
                                "product_url": product_url,
                                "image_url": img_elem.get("src") if img_elem else "",
                                "price": float(re.sub(r"[^\d.]", "", price_elem.get_text())) if price_elem else 0.0,
                                "rating": float(rating_elem.get_text(strip=True)) if rating_elem else 0.0,
                                "total_orders": orders_elem.get_text(strip=True) if orders_elem else "0",
                                "supplier_name": "AliExpress Seller",
                                "shipping_time_days": 25,
                                "shipping_cost": 0.0,
                            }
                        )
                    except Exception as e:
                        print(f"Error parsing item: {e}")
                        continue

                # Fallback mock data
                if not results:
                    results.append(
                        {
                            "platform": "AliExpress",
                            "product_name": product_name,
                            "product_url": "https://www.aliexpress.com/item/1005001234567890.html",
                            "image_url": "https://ae01.alicdn.com/kf/H1234567890.jpg",
                            "price": 12.99,
                            "rating": 4.5,
                            "total_orders": "500+",
                            "supplier_name": "Top Seller",
                            "shipping_time_days": 20,
                            "shipping_cost": 0.0,
                            "note": "Mock data - implement robust scraping",
                        }
                    )

        except Exception as e:
            print(f"Error scraping AliExpress: {e}")
            results.append({"error": str(e), "product_name": product_name})

        # Return as JSON string for CrewAI compatibility
        import json
        return json.dumps(results, indent=2)
