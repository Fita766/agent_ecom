import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional

load_dotenv()


class Settings(BaseSettings):
    # Shopify
    SHOPIFY_ADMIN_TOKEN: str = os.getenv("SHOPIFY_ADMIN_TOKEN", "")
    SHOPIFY_STORE_URL: str = os.getenv("SHOPIFY_STORE_URL", "")
    
    # APIs
    RAPID_API_KEY: str = os.getenv("RAPID_API_KEY", "")
    APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "")
    
    # LLM
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:8b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Scraping
    MAX_TIKTOK_VIDEOS: int = int(os.getenv("MAX_TIKTOK_VIDEOS", "3"))
    MAX_PINTEREST_PINS: int = int(os.getenv("MAX_PINTEREST_PINS", "5"))
    
    # Scoring Thresholds
    MIN_APPROVAL_SCORE: float = 75.0
    MAX_PRODUCT_WEIGHT_KG: float = 5.0
    MIN_PROFIT_MARGIN_PERCENT: float = 30.0
    
    # Output
    OUTPUT_DIR: str = "output"
    DATABASE_PATH: str = "output/products.db"
    
    class Config:
        env_file = ".env"


settings = Settings()