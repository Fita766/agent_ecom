"""
Outil d'extraction de produits depuis descriptions TikTok
Utilise le LLM local pour identifier le produit réel dans une vidéo/description
"""

from crewai.tools.base_tool import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field
from utils.llm import get_ollama_llm
import re


class ProductExtractorInput(BaseModel):
    video_title: str = Field(description="Titre de la vidéo TikTok")
    video_description: str = Field(default="", description="Description complète")
    hashtags: str = Field(default="", description="Hashtags de la vidéo")


class ProductExtractorTool(BaseTool):
    name: str = "Product Extractor from TikTok"
    description: str = """
    Extrait le nom du produit RÉEL depuis une vidéo TikTok.
    
    Input: Titre vidéo + description + hashtags
    Output: Nom produit structuré, catégorie, description
    
    Exemple:
    Input: "DIY Home Hacks - These LED lights changed my room! 🔥 #tiktokmakemebuyit #ledlights"
    Output: {
        "product_name": "LED Strip Lights",
        "category": "Home & Garden",
        "description": "Color-changing LED strips for room decoration"
    }
    """
    args_schema: Type[BaseModel] = ProductExtractorInput
    
    def _run(
        self,
        video_title: str,
        video_description: str = "",
        hashtags: str = ""
    ) -> Dict[str, Any]:
        """Extrait produit depuis contenu TikTok"""
        
        # Combiner toutes les infos
        full_text = f"{video_title}. {video_description}. {hashtags}"
        
        # Patterns communs de produits
        product_patterns = [
            r"(?:LED|RGB)\s+(?:strip|lights?|bulbs?)",
            r"(?:wireless|bluetooth)\s+(?:earbuds|headphones|speaker)",
            r"(?:portable|mini)\s+(?:blender|fan|humidifier)",
            r"(?:magnetic|suction)\s+(?:phone\s+)?holder",
            r"(?:car|desk|phone)\s+(?:mount|stand|organizer)",
            r"(?:smart|mini|portable)\s+\w+",
        ]
        
        # Essayer regex d'abord
        for pattern in product_patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                product_name = match.group(0).title()
                return self._structure_product(product_name, full_text)
        
        # Fallback: Utiliser LLM pour extraction
        return self._extract_with_llm(full_text)
    
    def _extract_with_llm(self, text: str) -> Dict[str, Any]:
        """Utilise DeepSeek local pour extraire produit"""
        
        llm = get_ollama_llm()
        
        prompt = f"""
Analyze this TikTok video text and extract the ACTUAL PRODUCT being shown/promoted.

Video Text: "{text}"

Return ONLY a JSON object (no markdown, no explanation):
{{
    "product_name": "Exact product name (e.g., 'LED Strip Lights RGB 5M')",
    "category": "Product category (Home & Garden, Beauty, Tech, Fashion, Kitchen, Pet)",
    "description": "Brief product description (1 sentence)",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}

If no clear product is found, return:
{{
    "product_name": "Unknown Product",
    "category": "Other",
    "description": "Video content unclear",
    "keywords": []
}}

JSON:
"""
        
        try:
            response = llm.invoke(prompt)
            
            # Parser réponse LLM
            import json
            
            # Nettoyer réponse (retirer markdown si présent)
            clean_response = response.content if hasattr(response, 'content') else str(response)
            clean_response = clean_response.strip()
            
            # Retirer ```json et ``` si présents
            if clean_response.startswith("```"):
                clean_response = clean_response.split("```")[1]
                if clean_response.startswith("json"):
                    clean_response = clean_response[4:]
            
            clean_response = clean_response.strip()
            
            # Parser JSON
            result = json.loads(clean_response)
            
            # Validation
            if not result.get("product_name") or result["product_name"] == "Unknown Product":
                # Fallback: extraire manuellement
                return self._fallback_extraction(text)
            
            return result
            
        except Exception as e:
            print(f"❌ LLM extraction failed: {e}")
            return self._fallback_extraction(text)
    
    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        """Extraction basique si LLM échoue"""
        
        # Mots-clés produits communs
        product_keywords = {
            'led': ('Home & Garden', 'LED lighting product'),
            'light': ('Home & Garden', 'Lighting product'),
            'phone': ('Tech', 'Phone accessory'),
            'wireless': ('Tech', 'Wireless device'),
            'makeup': ('Beauty', 'Makeup product'),
            'kitchen': ('Kitchen', 'Kitchen gadget'),
            'organizer': ('Home & Garden', 'Organization product'),
            'holder': ('Accessories', 'Holder/stand product'),
        }
        
        text_lower = text.lower()
        
        for keyword, (category, desc) in product_keywords.items():
            if keyword in text_lower:
                # Extraire contexte autour du keyword
                words = text_lower.split()
                try:
                    idx = words.index(keyword)
                    context = ' '.join(words[max(0, idx-2):min(len(words), idx+3)])
                    product_name = context.title()
                except:
                    product_name = f"{keyword.title()} Product"
                
                return {
                    "product_name": product_name,
                    "category": category,
                    "description": desc,
                    "keywords": [keyword]
                }
        
        # Dernier fallback
        return {
            "product_name": "Trending Product",
            "category": "Other",
            "description": "Product from viral TikTok video",
            "keywords": ["viral", "trending"]
        }
    
    def _structure_product(self, product_name: str, full_text: str) -> Dict[str, Any]:
        """Structure le produit extrait"""
        
        # Déterminer catégorie basique
        category_map = {
            'led': 'Home & Garden',
            'light': 'Home & Garden',
            'bluetooth': 'Tech',
            'wireless': 'Tech',
            'phone': 'Tech',
            'makeup': 'Beauty',
            'skincare': 'Beauty',
            'kitchen': 'Kitchen',
            'pet': 'Pet',
            'fashion': 'Fashion',
            'jewelry': 'Fashion'
        }
        
        category = 'Other'
        for keyword, cat in category_map.items():
            if keyword in product_name.lower():
                category = cat
                break
        
        return {
            "product_name": product_name,
            "category": category,
            "description": f"{product_name} as seen on TikTok",
            "keywords": product_name.lower().split()
        }


if __name__ == "__main__":
    # Test
    extractor = ProductExtractorTool()
    
    tests = [
        ("DIY Home Hacks", "These LED strip lights are amazing! Game changer", "#tiktokmakemebuyit #ledlights"),
        ("Must-Have Kitchen Gadget", "This mini blender is perfect for smoothies", "#amazonfinds #kitchen"),
        ("Phone Accessory Haul", "Magnetic car mount holder - best purchase ever!", "#phonehacks")
    ]
    
    for title, desc, tags in tests:
        result = extractor._run(title, desc, tags)
        print(f"\nTest: {title}")
        print(f"Result: {result}")
