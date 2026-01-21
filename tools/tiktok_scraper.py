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
    ALWAYS call this tool with a SINGLE JSON object, not a list.

    Expected arguments:
    - keywords: array of strings (keywords to search on TikTok)
    - max_videos: integer (max videos to analyze, default 3)

    Example of valid call:
    {
      "keywords": ["home gadgets", "beauty products"],
      "max_videos": 3
    }

    Do NOT wrap this in a list. Just pass one object.

    The tool returns a list of dictionaries with:
    - platform
    - url
    - engagement
    - likes
    - shares
    - keyword
    - title

    Use this to identify viral products on TikTok.
    """
    args_schema: Type[BaseModel] = TikTokScraperInput
    
    def _run(self, keywords: List[str], max_videos: int = 3) -> List[Dict[str, Any]]:
        """Search TikTok for trending products"""
        results: List[Dict[str, Any]] = []
        
        for keyword in keywords[:3]:  # Limit to 3 keywords
            try:
                # Using RapidAPI TikTok Scraper
                url = "https://tiktok-scraper7.p.rapidapi.com/search/keyword"
                
                headers = {
                    "X-RapidAPI-Key": settings.RAPID_API_KEY,
                    "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
                }
                
                params = {
                    "keyword": keyword,
                    "count": str(max_videos)
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    for video in data.get("data", {}).get("videos", [])[:max_videos]:
                        results.append({
                            "platform": "TikTok",
                            "url": f"https://tiktok.com/@{video.get('author', {}).get('uniqueId', '')}/video/{video.get('id', '')}",
                            "engagement": video.get("stats", {}).get("playCount", 0),
                            "likes": video.get("stats", {}).get("diggCount", 0),
                            "shares": video.get("stats", {}).get("shareCount", 0),
                            "keyword": keyword,
                            "title": video.get("desc", ""),
                        })
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error scraping TikTok for '{keyword}': {e}")
                continue
        
        return results if results else [{"error": "No TikTok data found"}]
