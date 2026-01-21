from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ProductCategory(str, Enum):
    FASHION = "fashion"
    ELECTRONICS = "electronics"
    HOME_GARDEN = "home_garden"
    BEAUTY = "beauty"
    SPORTS = "sports"
    TOYS = "toys"
    PETS = "pets"
    ACCESSORIES = "accessories"
    OTHER = "other"


class Geography(str, Enum):
    US = "US"
    EU = "EU"
    FR = "FR"
    UK = "UK"
    CA = "CA"
    WORLDWIDE = "WORLDWIDE"


class ProductSource(BaseModel):
    platform: str = Field(description="Source platform (TikTok, Pinterest, etc)")
    url: str = Field(description="Original URL")
    engagement: Optional[int] = Field(default=0, description="Likes/shares/saves")
    date_found: datetime = Field(default_factory=datetime.now)


class SupplierInfo(BaseModel):
    platform: str = Field(description="AliExpress, Amazon, etc")
    product_url: str
    supplier_name: str
    price: float = Field(gt=0, description="Price in USD")
    shipping_cost: float = Field(default=0.0)
    shipping_time_days: int = Field(default=30)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    total_orders: Optional[int] = Field(default=0)
    stock_available: Optional[int] = Field(default=None)
    weight_kg: Optional[float] = Field(default=None, description="Product weight")
    dimensions_cm: Optional[str] = Field(default=None)


class Review(BaseModel):
    text: str
    rating: float = Field(ge=1, le=5)
    date: Optional[datetime] = None
    verified_purchase: bool = False
    sentiment_score: Optional[float] = Field(default=None, ge=-1, le=1)
    

class ReviewAnalysis(BaseModel):
    total_reviews: int = 0
    average_rating: float = Field(default=0.0, ge=0, le=5)
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0
    sentiment_score: float = Field(default=0.0, ge=-1, le=1, description="Overall sentiment")
    main_pros: List[str] = Field(default_factory=list)
    main_cons: List[str] = Field(default_factory=list)
    red_flags: List[str] = Field(default_factory=list)


class MarketAnalysis(BaseModel):
    niche: str
    target_geography: List[Geography]
    market_size_estimate: str = Field(description="Small/Medium/Large/Huge")
    competition_level: str = Field(description="Low/Medium/High/Very High")
    trend_direction: str = Field(description="Rising/Stable/Declining")
    seasonality: Optional[str] = Field(default=None)
    google_trends_score: Optional[int] = Field(default=None, ge=0, le=100)
    tiktok_views: Optional[int] = Field(default=0)
    pinterest_saves: Optional[int] = Field(default=0)
    search_volume_monthly: Optional[int] = Field(default=None)


class PricingStrategy(BaseModel):
    cost_price: float = Field(gt=0, description="Purchase price from supplier")
    shipping_cost: float = Field(default=0.0)
    total_cost: float = Field(gt=0)
    suggested_retail_price: float = Field(gt=0)
    profit_margin_percent: float = Field(ge=0, le=100)
    profit_amount: float
    competitive_price_range_min: Optional[float] = None
    competitive_price_range_max: Optional[float] = None
    recommended_geography_pricing: Dict[str, float] = Field(default_factory=dict)


class ProductScore(BaseModel):
    trend_score: float = Field(ge=0, le=100, description="Trend momentum")
    profit_score: float = Field(ge=0, le=100, description="Profit potential")
    competition_score: float = Field(ge=0, le=100, description="Lower competition is better")
    demand_score: float = Field(ge=0, le=100, description="Market demand")
    quality_score: float = Field(ge=0, le=100, description="Product quality & reviews")
    shipping_score: float = Field(ge=0, le=100, description="Shipping feasibility")
    overall_score: float = Field(ge=0, le=100, description="Weighted average")
    
    reasoning: str = Field(description="Detailed explanation of scoring")


class WinningProduct(BaseModel):
    """Complete product analysis result"""
    id: str = Field(description="Unique product identifier")
    name: str
    description: str
    category: ProductCategory
    
    # Discovery
    source: ProductSource
    discovery_date: datetime = Field(default_factory=datetime.now)
    
    # Suppliers
    suppliers: List[SupplierInfo] = Field(min_length=1)
    best_supplier: Optional[SupplierInfo] = None
    
    # Analysis
    market_analysis: MarketAnalysis
    review_analysis: ReviewAnalysis
    pricing_strategy: PricingStrategy
    
    # Scoring
    score: ProductScore
    is_approved: bool = Field(default=False)
    rejection_reason: Optional[str] = None
    
    # Product Details
    images_urls: List[str] = Field(default_factory=list)
    video_url: Optional[str] = None
    features: List[str] = Field(default_factory=list)
    specifications: Dict[str, Any] = Field(default_factory=dict)
    
    # Shopify
    shopify_product_id: Optional[str] = None
    shopify_url: Optional[str] = None
    landing_page_created: bool = False


class DuplicateCheckResult(BaseModel):
    is_duplicate: bool
    existing_product_id: Optional[str] = None
    similarity_score: float = Field(ge=0, le=1)
    reason: str
