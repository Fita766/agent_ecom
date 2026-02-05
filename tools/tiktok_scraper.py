from crewai.tools.base_tool import BaseTool
from typing import List, Dict, Any, Type, Optional
from pydantic import BaseModel, Field
import requests
import time
from utils.config import settings


class TikTokScraperInput(BaseModel):
    """Input for TikTok Scraper"""
    keywords: List[str] = Field(description="Keywords/hashtags to search on TikTok (without # symbol)")
    max_videos: int = Field(default=3, description="Max videos to analyze")
    region: str = Field(default="us", description="Region code (e.g., 'us', 'gb', 'fr')")
    publish_time: int = Field(default=0, description="0=ALL, 1=24h, 7=week, 30=month, 90=3months, 180=6months")
    sort_type: int = Field(default=0, description="0=Relevance, 1=Like count, 3=Date posted")


class TikTokScraperTool(BaseTool):
    name: str = "TikTok Trend Scraper"
    description: str = """
    Scrape TikTok to find trending products based on keywords/hashtags.
    
    IMPORTANT: Call this tool with a SINGLE dictionary object containing:
    - keywords: array of strings (e.g., ["tiktokmakemebuyit", "home gadgets"])
      Note: Do NOT include the # symbol in keywords
    - max_videos: integer (default: 3)
    - region: string (default: "us")
    - publish_time: integer (default: 0 for all time)
    - sort_type: integer (default: 0 for relevance)
    
    Example correct usage:
    {"keywords": ["tiktokmakemebuyit", "home gadgets"], "max_videos": 3, "region": "us"}
    
    Returns a list of trending videos with engagement metrics.
    Use this to identify viral products on TikTok.
    """
    args_schema: Type[BaseModel] = TikTokScraperInput
    
    def _run(
        self, 
        keywords: List[str] = None, 
        max_videos: int = 3,
        region: str = "us",
        publish_time: int = 0,
        sort_type: int = 0
    ) -> List[Dict[str, Any]]:
        """Search TikTok for trending products"""
        # Validation
        if not keywords:
            return [{"error": "Keywords are required. Provide a list of keywords/hashtags to search (without # symbol)."}]
        
        if not isinstance(keywords, list):
            keywords = [str(keywords)]
        
        # Remove # symbol if present
        keywords = [kw.strip("#") for kw in keywords]
        
        results: List[Dict[str, Any]] = []
        
        for keyword in keywords[:3]:  # Limit to 3 keywords
            try:
                url = "https://tiktok-scraper7.p.rapidapi.com/feed/search"
                
                headers = {
                    "x-rapidapi-key": settings.RAPID_API_KEY,
                    "x-rapidapi-host": "tiktok-scraper7.p.rapidapi.com"
                }
                
                params = {
                    "keywords": keyword,
                    "region": region,
                    "count": str(max_videos),
                    "cursor": "0",
                    "publish_time": str(publish_time),
                    "sort_type": str(sort_type)
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if API returned success
                    if data.get("code") != 0:
                        error_msg = data.get("msg", "Unknown API error")
                        print(f"[TikTok ERROR] API returned error: {error_msg}")
                        results.append({
                            "error": f"TikTok API error: {error_msg}",
                            "keyword": keyword
                        })
                        continue
                    
                    videos = data.get("data", {}).get("videos", [])
                    
                    if videos:
                        for video in videos[:max_videos]:
                            # Build TikTok URL from video_id or aweme_id
                            video_id = video.get("video_id") or video.get("aweme_id", "")
                            author_id = video.get("author", {}).get("unique_id", "")
                            
                            if author_id and video_id:
                                tiktok_url = f"https://tiktok.com/@{author_id}/video/{video_id}"
                            else:
                                tiktok_url = f"https://tiktok.com/search?q={keyword}"
                            
                            results.append({
                                "platform": "TikTok",
                                "url": tiktok_url,
                                "video_id": video_id,
                                "aweme_id": video.get("aweme_id", ""),
                                "engagement": video.get("play_count", 0),
                                "likes": video.get("digg_count", 0),
                                "shares": video.get("share_count", 0),
                                "comments": video.get("comment_count", 0),
                                "downloads": video.get("download_count", 0),
                                "keyword": keyword,
                                "title": video.get("title", ""),
                                "author": {
                                    "unique_id": author_id,
                                    "nickname": video.get("author", {}).get("nickname", ""),
                                    "id": video.get("author", {}).get("id", "")
                                },
                                "create_time": video.get("create_time", 0),
                                "duration": video.get("duration", 0),
                                "cover": video.get("cover", ""),
                            })
                    else:
                        print(f"[TikTok] No videos found for keyword: {keyword}")
                        results.append({
                            "error": f"No videos found for keyword: {keyword}",
                            "keyword": keyword
                        })
                        
                elif response.status_code == 401:
                    error_msg = f"API Key invalide ou expiree pour RapidAPI. Status: {response.status_code}"
                    print(f"[TikTok ERROR] {error_msg}")
                    return [{"error": error_msg, "suggestion": "Verifiez votre RAPID_API_KEY dans config.py ou .env"}]
                    
                elif response.status_code == 404:
                    error_msg = f"Endpoint API introuvable (404). Verifiez l'URL: {url}"
                    print(f"[TikTok ERROR] {error_msg}")
                    return [{"error": error_msg}]
                    
                elif response.status_code == 429:
                    error_msg = f"Rate limit depasse ou credits epuises. Status: {response.status_code}"
                    print(f"[TikTok ERROR] {error_msg}")
                    return [{"error": error_msg, "suggestion": "Attendez quelques minutes ou verifiez vos credits RapidAPI"}]
                    
                else:
                    error_data = response.text[:200] if response.text else "No error details"
                    error_msg = f"Erreur API TikTok: Status {response.status_code} - {error_data}"
                    print(f"[TikTok ERROR] {error_msg}")
                    results.append({
                        "error": error_msg,
                        "keyword": keyword,
                        "status_code": response.status_code
                    })
                
                time.sleep(1)  # Rate limiting
                
            except requests.exceptions.Timeout:
                error_msg = f"Timeout lors de la requete TikTok pour '{keyword}'. Le serveur n'a pas repondu a temps."
                print(f"[TikTok ERROR] {error_msg}")
                results.append({
                    "error": error_msg,
                    "keyword": keyword
                })
                
            except requests.exceptions.RequestException as e:
                error_msg = f"Erreur de connexion TikTok pour '{keyword}': {e}"
                print(f"[TikTok ERROR] {error_msg}")
                results.append({
                    "error": error_msg,
                    "keyword": keyword
                })
                
            except Exception as e:
                error_msg = f"Erreur inattendue TikTok pour '{keyword}': {e}"
                print(f"[TikTok ERROR] {error_msg}")
                results.append({
                    "error": error_msg,
                    "keyword": keyword
                })
        
        if not results:
            return [{"error": "No TikTok data found. Check your API key and endpoint."}]
        
        # Filter out error-only results if we have successful results
        successful_results = [r for r in results if "error" not in r]
        if successful_results:
            return successful_results
        
        # Return errors if no successful results
        return results
