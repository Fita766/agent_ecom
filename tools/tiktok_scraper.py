from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type
from pydantic import BaseModel, Field
import requests
import time
from utils.config import settings


class TikTokScraperInput(BaseModel):
    """Input for TikTok Scraper"""
    keywords: List[str] = Field(description="Keywords to search on TikTok")
    max_videos: int = Field(default=3, description="Max videos to analyze")


class TikTokScraperTool(BaseTool):
    name: str = "TikTok Trend Scraper"
    description: str = """
    Scrape TikTok to find trending products based on keywords.
    
    IMPORTANT: Call this tool with a SINGLE dictionary object containing:
    - keywords: array of strings (e.g., ["home gadgets", "beauty products"])
    - max_videos: integer (default: 3)
    
    Example correct usage:
    {"keywords": ["home gadgets", "beauty products"], "max_videos": 3}
    
    Returns a list of trending videos with engagement metrics.
    Use this to identify viral products on TikTok.
    """
    args_schema: Type[BaseModel] = TikTokScraperInput
    
    def _run(self, keywords: List[str] = None, max_videos: int = 3) -> List[Dict[str, Any]]:
        """Search TikTok for trending products"""
        # Validation
        if not keywords:
            return [{"error": "Keywords are required. Provide a list of keywords to search."}]
        
        if not isinstance(keywords, list):
            keywords = [str(keywords)]
        
        results: List[Dict[str, Any]] = []
        
        for keyword in keywords[:3]:  # Limit to 3 keywords
            try:
                # Using RapidAPI TikTok Scraper
                # Note: L'endpoint peut varier selon l'API RapidAPI utilisée
                # Si 404, vérifiez la documentation de votre API sur RapidAPI
                url = "https://tiktok-scraper7.p.rapidapi.com/search/keyword"
                
                headers = {
                    "X-RapidAPI-Key": settings.RAPID_API_KEY,
                    "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
                }
                
                params = {
                    "keyword": keyword,
                    "count": str(max_videos)
                }
                
                # Si l'endpoint ne fonctionne pas, utiliser des données mock
                # pour permettre au workflow de continuer
                use_mock_data = False
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                # Gestion détaillée des erreurs API
                if response.status_code == 200:
                    data = response.json()
                    videos = data.get("data", {}).get("videos", [])
                    if videos:
                        for video in videos[:max_videos]:
                            results.append({
                                "platform": "TikTok",
                                "url": f"https://tiktok.com/@{video.get('author', {}).get('uniqueId', '')}/video/{video.get('id', '')}",
                                "engagement": video.get("stats", {}).get("playCount", 0),
                                "likes": video.get("stats", {}).get("diggCount", 0),
                                "shares": video.get("stats", {}).get("shareCount", 0),
                                "keyword": keyword,
                                "title": video.get("desc", ""),
                            })
                    else:
                        # Pas de vidéos dans la réponse
                        print(f"[TikTok] No videos found for keyword: {keyword}")
                elif response.status_code == 401:
                    error_msg = f"API Key invalide ou expiree pour RapidAPI. Status: {response.status_code}"
                    print(f"[TikTok ERROR] {error_msg}")
                    return [{"error": error_msg, "suggestion": "Verifiez votre RAPID_API_KEY dans config.py ou .env"}]
                elif response.status_code == 404:
                    error_msg = f"Endpoint API introuvable (404). L'API a peut-etre change."
                    print(f"[TikTok ERROR] {error_msg}")
                    print(f"[TikTok] Solution: Verifiez la documentation de votre API RapidAPI")
                    print(f"[TikTok] Utilisation de donnees mock pour continuer le workflow...")
                    results.append({
                        "platform": "TikTok",
                        "url": f"https://tiktok.com/search?q={keyword}",
                        "engagement": 15000,
                        "likes": 2500,
                        "shares": 500,
                        "keyword": keyword,
                        "title": f"Trending product related to {keyword}",
                        "note": "Mock data - API endpoint not found (404)"
                    })
                elif response.status_code == 429:
                    error_msg = f"Rate limit depasse ou credits epuises. Status: {response.status_code}"
                    print(f"[TikTok ERROR] {error_msg}")
                    print(f"[TikTok] Utilisation de donnees mock pour continuer le workflow...")
                    results.append({
                        "platform": "TikTok",
                        "url": f"https://tiktok.com/search?q={keyword}",
                        "engagement": 15000,
                        "likes": 2500,
                        "shares": 500,
                        "keyword": keyword,
                        "title": f"Trending product related to {keyword}",
                        "note": "Mock data - API credits may be exhausted"
                    })
                else:
                    error_data = response.text[:200] if response.text else "No error details"
                    error_msg = f"Erreur API TikTok: Status {response.status_code} - {error_data}"
                    print(f"[TikTok ERROR] {error_msg}")
                    print(f"[TikTok] Utilisation de donnees mock pour continuer le workflow...")
                    results.append({
                        "platform": "TikTok",
                        "url": f"https://tiktok.com/search?q={keyword}",
                        "engagement": 12000,
                        "likes": 2000,
                        "shares": 400,
                        "keyword": keyword,
                        "title": f"Popular {keyword} product",
                        "note": f"Mock data - API error {response.status_code}"
                    })
                
                time.sleep(1)  # Rate limiting
                
            except requests.exceptions.RequestException as e:
                error_msg = f"Erreur de connexion TikTok pour '{keyword}': {e}"
                print(f"[TikTok ERROR] {error_msg}")
                # Fallback avec données mock
                print(f"[TikTok] Utilisation de donnees mock pour continuer le workflow...")
                results.append({
                    "platform": "TikTok",
                    "url": f"https://tiktok.com/search?q={keyword}",
                    "engagement": 10000,
                    "likes": 1500,
                    "shares": 300,
                    "keyword": keyword,
                    "title": f"Trending {keyword} content",
                    "note": "Mock data - Connection error"
                })
            except Exception as e:
                error_msg = f"Erreur inattendue TikTok pour '{keyword}': {e}"
                print(f"[TikTok ERROR] {error_msg}")
                # Fallback avec données mock
                results.append({
                    "platform": "TikTok",
                    "url": f"https://tiktok.com/search?q={keyword}",
                    "engagement": 8000,
                    "likes": 1200,
                    "shares": 250,
                    "keyword": keyword,
                    "title": f"{keyword} trending product",
                    "note": "Mock data - Unexpected error"
                })
        
        return results if results else [{"error": "No TikTok data found"}]
