from crewai.tools.base_tool import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field
import shopify
from utils.config import settings


class ShopifyToolInput(BaseModel):
    """Input for Shopify operations"""
    action: str = Field(description="Action: create_product, get_themes, activate_theme")
    product_data: Dict[str, Any] = Field(default_factory=dict)


class ShopifyTool(BaseTool):
    name: str = "Shopify Store Manager"
    description: str = """
    Manage Shopify store: create products, set themes, publish pages.
    Use this to automate Shopify store setup.
    """
    args_schema: Type[BaseModel] = ShopifyToolInput
    
    def __init__(self):
        super().__init__()
        self._init_shopify()
    
    def _init_shopify(self) -> None:
        """Initialize Shopify session"""
        shop_url = f"https://{settings.SHOPIFY_STORE_URL}.myshopify.com"
        api_version = "2024-01"

        shopify.ShopifyResource.set_site(shop_url)
        shopify.ShopifyResource.set_user(settings.SHOPIFY_ADMIN_TOKEN)
    
    def _run(self, action: str, product_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute Shopify action"""
        product_data = product_data or {}
        
        if action == "create_product":
            return self._create_product(product_data)
        elif action == "get_themes":
            return self._get_themes()
        elif action == "activate_theme":
            return self._activate_theme(product_data.get("theme_id"))
        else:
            return {"error": f"Unknown action: {action}"}
    
    def _create_product(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            product = shopify.Product()
            product.title = data.get("title", "New Product")
            product.body_html = data.get("description", "")
            product.vendor = data.get("vendor", "My Store")
            product.product_type = data.get("category", "")

            variant = shopify.Variant()
            variant.price = str(data.get("price", 0))
            variant.sku = data.get("sku", "")
            product.variants = [variant]

            if data.get("images"):
                product.images = [shopify.Image({"src": url}) for url in data["images"][:5]]

            if product.save():
                return {
                    "success": True,
                    "product_id": product.id,
                    "product_url": f"https://{settings.SHOPIFY_STORE_URL}.myshopify.com/products/{product.handle}",
                }
            else:
                return {"success": False, "errors": product.errors.full_messages()}

        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_themes(self) -> Dict[str, Any]:
        try:
            themes = shopify.Theme.find()
            return {"themes": [{"id": t.id, "name": t.name, "role": t.role} for t in themes]}
        except Exception as e:
            return {"error": str(e)}
    
    def _activate_theme(self, theme_id: int) -> Dict[str, Any]:
        try:
            theme = shopify.Theme.find(theme_id)
            theme.role = "main"
            if theme.save():
                return {"success": True, "theme_id": theme_id}
            else:
                return {"success": False, "errors": theme.errors.full_messages()}
        except Exception as e:
            return {"error": str(e)}
