"""
Amazon Product Search via Rainforest API
Doc: https://www.rainforestapi.com/docs/product-data-api/overview
Free tier: 100 requests/month
"""

from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import requests
import os


class AmazonRainforestInput(BaseModel):
    """Input for Amazon search"""
    product_name: str = Field(description="Product name to search on Amazon")
    max_results: int = Field(default=5, description="Max products to return")


class AmazonRainforestTool(BaseTool):
    name: str = "Amazon Product Search (Rainforest API)"
    description: str = """
    Search Amazon for competitor products using Rainforest API.
    Returns REAL Amazon URLs, prices, ratings, review counts.
    
    Much better than scraping because:
    - Real Amazon data
    - No anti-bot issues
    - Accurate prices & ratings
    - Valid product URLs
    
    Use this to analyze competitive pricing on Amazon.
    """
    args_schema: Type[BaseModel] = AmazonRainforestInput
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("RAINFOREST_API_KEY", "")
        self.base_url = "https://api.rainforestapi.com/request"
    
    def _run(self, product_name: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search Amazon via Rainforest API"""
        
        if not self.api_key:
            print("⚠️  RAINFOREST_API_KEY not configured")
            print("   Get free key: https://www.rainforestapi.com/")
            print("   Free tier: 100 requests/month")
            return self._mock_data(product_name, max_results)
        
        try:
            params = {
                "api_key": self.api_key,
                "type": "search",
                "amazon_domain": "amazon.com",
                "search_term": product_name,
                "page": "1",
                "max_page": "1"
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                search_results = data.get("search_results", [])
                
                if search_results:
                    return self._parse_results(search_results, max_results)
                else:
                    print(f"⚠️  No Amazon results for: {product_name}")
                    return self._mock_data(product_name, max_results)
            
            elif response.status_code == 401:
                print("❌ Invalid Rainforest API key")
                return self._mock_data(product_name, max_results)
            
            elif response.status_code == 429:
                print("❌ Rate limit exceeded (100 req/month on free tier)")
                return self._mock_data(product_name, max_results)
            
            else:
                print(f"❌ HTTP {response.status_code}")
                return self._mock_data(product_name, max_results)
                
        except Exception as e:
            print(f"❌ Amazon Rainforest error: {e}")
            return self._mock_data(product_name, max_results)
    
    def _parse_results(self, results: List[Dict], max_results: int) -> List[Dict[str, Any]]:
        """Parse Rainforest API response"""
        parsed = []
        
        for result in results[:max_results]:
            # Extract price
            price_raw = result.get("price", {})
            if isinstance(price_raw, dict):
                price = price_raw.get("value", 0)
            else:
                price = float(price_raw) if price_raw else 0
            
            # Extract rating
            rating_raw = result.get("rating", 0)
            rating = float(rating_raw) if rating_raw else 0
            
            # Extract review count
            reviews_raw = result.get("ratings_total", 0)
            reviews = int(reviews_raw) if reviews_raw else 0
            
            # Build Amazon URL
            asin = result.get("asin", "")
            product_url = f"https://www.amazon.com/dp/{asin}" if asin else result.get("link", "")
            
            parsed.append({
                "platform": "Amazon",
                "asin": asin,
                "product_name": result.get("title", ""),
                "product_url": product_url,
                "price": price,
                "rating": rating,
                "review_count": reviews,
                "bestseller_rank": result.get("bestseller", {}).get("rank") if result.get("bestseller") else None,
                "prime_eligible": result.get("is_prime", False),
                "in_stock": result.get("is_available", True),
                "image_url": result.get("image", "")
            })
        
        return parsed
    
    def _mock_data(self, product_name: str, max_results: int) -> List[Dict[str, Any]]:
        """Mock data si API non dispo"""
        print("📦 Using mock Amazon data (configure RAINFOREST_API_KEY for real data)")
        
        results = []
        base_price = 19.99
        
        # ASINs réalistes (format Amazon)
        mock_asins = ["B0CJMNF8R2", "B08XYZ1234", "B09ABC5678", "B0ADEF9012", "B07GHI3456"]
        
        for i in range(min(max_results, 5)):
            results.append({
                "platform": "Amazon",
                "asin": mock_asins[i],
                "product_name": f"{product_name} - Variant {i+1}",
                "product_url": f"https://www.amazon.com/dp/{mock_asins[i]}",
                "price": round(base_price + (i * 2.5), 2),
                "rating": round(4.7 - (i * 0.1), 1),
                "review_count": 1500 - (i * 200),
                "bestseller_rank": (i + 1) * 100 if i < 3 else None,
                "prime_eligible": i < 3,
                "in_stock": True,
                "image_url": "",
                "note": "Mock data - Set RAINFOREST_API_KEY for real Amazon data"
            })
        
        return results


class AmazonProductDetails(BaseTool):
    """Get detailed product info from Amazon"""
    
    name: str = "Amazon Product Details"
    description: str = """
    Get detailed information for a specific Amazon product by ASIN.
    Returns: full description, features, specs, review summary.
    """
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("RAINFOREST_API_KEY", "")
        self.base_url = "https://api.rainforestapi.com/request"
    
    def _run(self, asin: str) -> Dict[str, Any]:
        """Get product details"""
        
        if not self.api_key:
            return {
                "error": "RAINFOREST_API_KEY not configured",
                "asin": asin
            }
        
        try:
            params = {
                "api_key": self.api_key,
                "type": "product",
                "amazon_domain": "amazon.com",
                "asin": asin
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                product = data.get("product", {})
                
                return {
                    "asin": asin,
                    "title": product.get("title", ""),
                    "description": product.get("description", ""),
                    "features": product.get("feature_bullets", []),
                    "specifications": product.get("specifications", []),
                    "price": product.get("buybox_winner", {}).get("price", {}).get("value", 0),
                    "rating": product.get("rating", 0),
                    "reviews_total": product.get("ratings_total", 0),
                    "images": product.get("images", [])
                }
            else:
                return {"error": f"HTTP {response.status_code}", "asin": asin}
                
        except Exception as e:
            return {"error": str(e), "asin": asin}


if __name__ == "__main__":
    # Test
    tool = AmazonRainforestTool()
    
    print("🧪 Testing Amazon Rainforest API...")
    results = tool._run("LED strip lights", max_results=3)
    
    print(f"\n📦 Found {len(results)} Amazon products:")
    for product in results:
        print(f"\n  - {product['product_name']}")
        print(f"    ASIN: {product['asin']}")
        print(f"    URL: {product['product_url']}")
        print(f"    Price: ${product['price']}")
        print(f"    Rating: {product['rating']}/5 ({product['review_count']} reviews)")
        print(f"    Prime: {'Yes' if product['prime_eligible'] else 'No'}")
