from crewai.tools.base_tool import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field
from pytrends.request import TrendReq


class GoogleTrendsInput(BaseModel):
    """Input for Google Trends"""
    keyword: str = Field(description="Keyword to analyze")
    timeframe: str = Field(default="today 3-m", description="Time frame")
    geo: str = Field(default="", description="Geography code (US, FR, etc)")


class GoogleTrendsTool(BaseTool):
    name: str = "Google Trends Analyzer"
    description: str = """
    Analyze keyword trends on Google Trends.
    Returns trend score, related queries, rising trends.
    Use this to validate product demand and trend direction.
    """
    args_schema: Type[BaseModel] = GoogleTrendsInput
    
    def _run(self, keyword: str, timeframe: str = "today 3-m", geo: str = "") -> Dict[str, Any]:
        """Analyze Google Trends for keyword"""
        try:
            pytrends = TrendReq(hl="en-US", tz=360)
            pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo)

            interest_df = pytrends.interest_over_time()

            avg_interest = 0
            trend_direction = "Stable"

            if not interest_df.empty and keyword in interest_df.columns:
                avg_interest = int(interest_df[keyword].mean())

                recent = interest_df[keyword].iloc[-4:].mean()
                older = interest_df[keyword].iloc[:4].mean()

                if recent > older * 1.2:
                    trend_direction = "Rising"
                elif recent < older * 0.8:
                    trend_direction = "Declining"

            related = pytrends.related_queries()
            rising_queries = []

            if keyword in related and related[keyword]["rising"] is not None:
                rising_queries = related[keyword]["rising"]["query"].head(5).tolist()

            return {
                "keyword": keyword,
                "average_interest": avg_interest,
                "trend_direction": trend_direction,
                "rising_queries": rising_queries,
                "timeframe": timeframe,
                "geo": geo or "Worldwide",
            }

        except Exception as e:
            return {"error": str(e), "keyword": keyword}
