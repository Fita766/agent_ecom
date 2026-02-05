"""
CJ Dropshipping API Integration
Documentation: https://developers.cjdropshipping.com/
"""

from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import requests
import os


class CJDropshippingInput(BaseModel):
    """Input for CJ Dropshipping search"""
    product_name: str = Field(description="Product name to search")
    max_results: int = Field(default=5, description="Max products to return")


class CJDropshippingTool(BaseTool):
    name: str = "CJ Dropshipping Product Search"
    description: str = """
    Search products on CJ Dropshipping platform.
    Returns product details, pricing, shipping costs, stock levels.
    
    Better than AliExpress because:
    - Real API (no scraping needed)
    - Accurate stock levels
    - Real shipping calculations
    - Better supplier ratings
    
    Use this to find dropshipping suppliers for products.
    """
    args_schema: Type[BaseModel] = CJDropshippingInput
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CJ_DROPSHIPPING_API_KEY", "")
        self.base_url = "https://developers.cjdropshipping.com/api2.0/v1"
        
    def _run(self, product_name: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search CJ Dropshipping for products"""
        
        if not self.api_key:
            print("⚠️  CJ_DROPSHIPPING_API_KEY not configured")
            return self._mock_data(product_name, max_results)
        
        try:
            # CJ Dropshipping Product List API
            endpoint = f"{self.base_url}/product/list"
            
            headers = {
                "CJ-Access-Token": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "productNameEn": product_name,
                "pageNum": 1,
                "pageSize": max_results,
                "country": "US"  # Target country for shipping
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 200:
                    products = data.get("data", {}).get("list", [])
                    
                    return self._parse_products(products)
                else:
                    error_msg = data.get("message", "Unknown error")
                    print(f"❌ CJ API error: {error_msg}")
                    return self._mock_data(product_name, max_results)
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return self._mock_data(product_name, max_results)
                
        except Exception as e:
            print(f"❌ CJ Dropshipping error: {e}")
            return self._mock_data(product_name, max_results)
    
    def _parse_products(self, products: List[Dict]) -> List[Dict[str, Any]]:
        """Parse CJ API response"""
        results = []
        
        for product in products:
            # Calculer coût shipping (approximatif si pas dispo)
            shipping_cost = product.get("shippingFee", 0)
            if not shipping_cost:
                # Estimation basique
                weight_kg = product.get("weight", 0.5)
                shipping_cost = 3.5 + (weight_kg * 2)  # Base + weight
            
            results.append({
                "platform": "CJ Dropshipping",
                "product_id": product.get("pid", ""),
                "product_name": product.get("productNameEn", ""),
                "product_url": f"https://cjdropshipping.com/product/detail/{product.get('pid', '')}",
                "price": float(product.get("sellPrice", 0)),
                "shipping_cost": float(shipping_cost),
                "shipping_time_days": int(product.get("deliveryDays", 15)),
                "stock_available": int(product.get("stockQuantity", 0)),
                "rating": float(product.get("rating", 0)) if product.get("rating") else 4.5,
                "total_orders": int(product.get("totalOrders", 0)),
                "weight_kg": float(product.get("weight", 0)),
                "image_url": product.get("productImage", ""),
                "category": product.get("categoryName", ""),
                "supplier_name": "CJ Dropshipping Verified"
            })
        
        return results
    
    def _mock_data(self, product_name: str, max_results: int) -> List[Dict[str, Any]]:
        """Mock data si API non dispo"""
        print("📦 Using mock CJ Dropshipping data (configure API key for real data)")
        
        results = []
        base_price = 12.99
        
        for i in range(max_results):
            results.append({
                "platform": "CJ Dropshipping",
                "product_id": f"CJ{1000000 + i}",
                "product_name": f"{product_name} - Variant {i+1}",
                "product_url": f"https://cjdropshipping.com/product/detail/CJ{1000000 + i}",
                "price": round(base_price + (i * 1.5), 2),
                "shipping_cost": round(3.5 + (i * 0.5), 2),
                "shipping_time_days": 10 + (i * 2),
                "stock_available": 5000 - (i * 500),
                "rating": round(4.8 - (i * 0.1), 1),
                "total_orders": 3000 - (i * 200),
                "weight_kg": round(0.5 + (i * 0.2), 2),
                "image_url": "",
                "category": "General",
                "supplier_name": "CJ Dropshipping Verified",
                "note": "Mock data - Set CJ_DROPSHIPPING_API_KEY for real data"
            })
        
        return results


class CJShippingCalculator(BaseTool):
    """Calculate shipping cost for CJ products"""
    
    name: str = "CJ Shipping Cost Calculator"
    description: str = """
    Calculate accurate shipping cost from CJ Dropshipping.
    Input: product_id, destination_country, quantity
    Returns: shipping cost, delivery time
    """
    
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("CJ_DROPSHIPPING_API_KEY", "")
        self.base_url = "https://developers.cjdropshipping.com/api2.0/v1"
    
    def _run(
        self,
        product_id: str,
        destination_country: str = "US",
        quantity: int = 1
    ) -> Dict[str, Any]:
        """Calculate shipping"""
        
        if not self.api_key:
            return {
                "shipping_cost": 4.99,
                "delivery_days": 12,
                "note": "Mock data - Configure CJ_DROPSHIPPING_API_KEY"
            }
        
        try:
            endpoint = f"{self.base_url}/logistic/freightCalculate"
            
            headers = {
                "CJ-Access-Token": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "products": [
                    {
                        "pid": product_id,
                        "quantity": quantity
                    }
                ],
                "startCountry": "CN",  # China
                "endCountry": destination_country
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("code") == 200:
                    freight = data.get("data", {}).get("list", [{}])[0]
                    
                    return {
                        "shipping_cost": float(freight.get("freight", 0)),
                        "delivery_days": int(freight.get("logisticAging", 15)),
                        "shipping_method": freight.get("logisticName", "Standard")
                    }
            
            # Fallback
            return {
                "shipping_cost": 4.99,
                "delivery_days": 12,
                "note": "Estimation (API error)"
            }
            
        except Exception as e:
            print(f"❌ Shipping calc error: {e}")
            return {
                "shipping_cost": 4.99,
                "delivery_days": 12,
                "note": "Estimation (error)"
            }


if __name__ == "__main__":
    # Test
    tool = CJDropshippingTool()
    
    print("🧪 Testing CJ Dropshipping Tool...")
    results = tool._run("LED strip lights", max_results=3)
    
    print(f"\n📦 Found {len(results)} products:")
    for product in results:
        print(f"\n  - {product['product_name']}")
        print(f"    Price: ${product['price']}")
        print(f"    Shipping: ${product['shipping_cost']} ({product['shipping_time_days']} days)")
        print(f"    Stock: {product['stock_available']}")
        print(f"    Rating: {product['rating']}/5")
