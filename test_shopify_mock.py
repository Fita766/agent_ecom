"""
Script de test Shopify avec données mock pour identifier les erreurs
"""
import json
from typing import Dict, Any
from pathlib import Path

# Mock des données de produit pour tester
MOCK_PRODUCT_DATA = {
    "Wireless Earbuds Bluetooth": {
        "title": "Wireless Earbuds Bluetooth - Noise Cancelling",
        "description": "Premium wireless earbuds with active noise cancellation, 30-hour battery life, and crystal-clear sound quality. Perfect for music lovers and professionals.",
        "vendor": "TechGadgets Co.",
        "category": "Electronics > Audio > Headphones",
        "price": "29.99",
        "sku": "WEB-001",
        "images": [
            "https://example.com/images/earbuds-1.jpg",
            "https://example.com/images/earbuds-2.jpg",
            "https://example.com/images/earbuds-3.jpg"
        ],
        "tags": ["wireless", "bluetooth", "noise-cancelling", "audio"],
        "inventory_quantity": 100
    },
    "Smart Watch Fitness Tracker": {
        "title": "Smart Watch Fitness Tracker - Health Monitor",
        "description": "Advanced fitness tracker with heart rate monitor, sleep tracking, and 7-day battery life. Water-resistant design for all activities.",
        "vendor": "FitTech Solutions",
        "category": "Electronics > Wearables > Smart Watches",
        "price": "49.99",
        "sku": "SWF-001",
        "images": [
            "https://example.com/images/watch-1.jpg",
            "https://example.com/images/watch-2.jpg"
        ],
        "tags": ["fitness", "smartwatch", "health", "tracker"],
        "inventory_quantity": 50
    },
    "Portable Air Fryer Compact": {
        "title": "Portable Air Fryer Compact - Healthy Cooking",
        "description": "Compact air fryer perfect for small spaces. Cook healthy meals with 85% less oil. Easy to clean and dishwasher safe.",
        "vendor": "CompactCooking Ltd.",
        "category": "Home & Kitchen > Kitchen Appliances > Air Fryers",
        "price": "34.99",
        "sku": "PAF-001",
        "images": [
            "https://example.com/images/airfryer-1.jpg",
            "https://example.com/images/airfryer-2.jpg"
        ],
        "tags": ["air-fryer", "healthy-cooking", "compact", "kitchen"],
        "inventory_quantity": 75
    }
}

MOCK_THEME_DATA = [
    {"id": 1, "name": "Dawn", "role": "main"},
    {"id": 2, "name": "Debut", "role": "unpublished"},
    {"id": 3, "name": "Craft", "role": "unpublished"}
]


def test_shopify_connection():
    """Test la connexion Shopify avec les credentials réels"""
    print("=" * 80)
    print("TEST 1: Connexion Shopify")
    print("=" * 80)
    
    try:
        import shopify
        from utils.config import settings
        
        shop_url = f"https://{settings.SHOPIFY_STORE_URL}.myshopify.com"
        api_version = "2024-01"
        
        print(f"Shop URL: {shop_url}")
        print(f"API Version: {api_version}")
        print(f"Admin Token: {'*' * 20}...{settings.SHOPIFY_ADMIN_TOKEN[-4:] if settings.SHOPIFY_ADMIN_TOKEN else 'NOT SET'}")
        
        shopify.ShopifyResource.set_site(shop_url)
        shopify.ShopifyResource.set_user(settings.SHOPIFY_ADMIN_TOKEN)
        
        # Test simple : récupérer les infos du shop
        shop = shopify.Shop.current()
        print(f"\n✅ Connexion réussie!")
        print(f"   Shop Name: {shop.name}")
        print(f"   Shop Domain: {shop.domain}")
        print(f"   Email: {shop.email}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False


def test_get_themes():
    """Test la récupération des thèmes"""
    print("\n" + "=" * 80)
    print("TEST 2: Récupération des thèmes")
    print("=" * 80)
    
    try:
        import shopify
        from utils.config import settings
        
        shop_url = f"https://{settings.SHOPIFY_STORE_URL}.myshopify.com"
        shopify.ShopifyResource.set_site(shop_url)
        shopify.ShopifyResource.set_user(settings.SHOPIFY_ADMIN_TOKEN)
        
        themes = shopify.Theme.find()
        print(f"\n✅ {len(themes)} thème(s) trouvé(s):")
        for theme in themes:
            print(f"   - ID: {theme.id}, Name: {theme.name}, Role: {theme.role}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_product_mock(product_name: str, product_data: Dict[str, Any]):
    """Test la création d'un produit avec données mock"""
    print("\n" + "=" * 80)
    print(f"TEST 3: Création produit '{product_name}' (MOCK)")
    print("=" * 80)
    
    print(f"\n📦 Données du produit:")
    print(json.dumps(product_data, indent=2, ensure_ascii=False))
    
    try:
        import shopify
        from utils.config import settings
        
        shop_url = f"https://{settings.SHOPIFY_STORE_URL}.myshopify.com"
        shopify.ShopifyResource.set_site(shop_url)
        shopify.ShopifyResource.set_user(settings.SHOPIFY_ADMIN_TOKEN)
        
        # Créer le produit
        product = shopify.Product()
        product.title = product_data["title"]
        product.body_html = product_data["description"]
        product.vendor = product_data["vendor"]
        product.product_type = product_data["category"]
        product.tags = ", ".join(product_data.get("tags", []))
        
        # Créer la variante
        variant = shopify.Variant()
        variant.price = str(product_data["price"])
        variant.sku = product_data["sku"]
        variant.inventory_quantity = product_data.get("inventory_quantity", 0)
        product.variants = [variant]
        
        # Ajouter les images
        if product_data.get("images"):
            product.images = [shopify.Image({"src": url}) for url in product_data["images"][:5]]
        
        print(f"\n🔄 Tentative de sauvegarde...")
        if product.save():
            print(f"\n✅ Produit créé avec succès!")
            print(f"   Product ID: {product.id}")
            print(f"   Handle: {product.handle}")
            print(f"   URL: https://{settings.SHOPIFY_STORE_URL}.myshopify.com/products/{product.handle}")
            return {
                "success": True,
                "product_id": product.id,
                "handle": product.handle,
                "url": f"https://{settings.SHOPIFY_STORE_URL}.myshopify.com/products/{product.handle}"
            }
        else:
            print(f"\n❌ Erreurs lors de la sauvegarde:")
            for error in product.errors.full_messages():
                print(f"   - {error}")
            return {
                "success": False,
                "errors": product.errors.full_messages()
            }
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def test_shopify_tool_directly():
    """Test direct de l'outil Shopify"""
    print("\n" + "=" * 80)
    print("TEST 4: Test direct de ShopifyTool")
    print("=" * 80)
    
    try:
        from tools.shopify_tool import ShopifyTool
        
        tool = ShopifyTool()
        print("\n✅ ShopifyTool initialisé")
        
        # Test get_themes
        print("\n🔄 Test: get_themes")
        result = tool._run("get_themes")
        print(f"   Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        # Test create_product avec mock data
        print("\n🔄 Test: create_product (mock)")
        mock_data = MOCK_PRODUCT_DATA["Wireless Earbuds Bluetooth"]
        result = tool._run("create_product", mock_data)
        print(f"   Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Lance tous les tests"""
    print("\n" + "=" * 80)
    print("TESTS SHOPIFY AVEC DONNÉES MOCK")
    print("=" * 80)
    
    results = {
        "connection": False,
        "get_themes": False,
        "create_product": False,
        "tool_direct": False
    }
    
    # Test 1: Connexion
    results["connection"] = test_shopify_connection()
    
    if results["connection"]:
        # Test 2: Get themes
        results["get_themes"] = test_get_themes()
        
        # Test 3: Create product (mock)
        product_name = "Wireless Earbuds Bluetooth"
        result = test_create_product_mock(product_name, MOCK_PRODUCT_DATA[product_name])
        results["create_product"] = result.get("success", False)
    
    # Test 4: Tool direct
    results["tool_direct"] = test_shopify_tool_directly()
    
    # Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES TESTS")
    print("=" * 80)
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    # Sauvegarder les résultats
    output_file = Path("output/shopify_test_results.json")
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "test_results": results,
            "mock_data_used": MOCK_PRODUCT_DATA,
            "timestamp": str(datetime.now())
        }, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n📄 Résultats sauvegardés dans: {output_file}")


if __name__ == "__main__":
    from datetime import datetime
    main()
