from crewai.tools.base_tool import BaseTool
from typing import Dict, Any, Type
from pydantic import BaseModel, Field
from utils.database import ProductDatabase
from utils.config import settings
from difflib import SequenceMatcher


class DuplicateCheckerInput(BaseModel):
    """Input for Duplicate Checker"""
    product_name: str = Field(description="Product name to check")
    threshold: float = Field(default=0.8, description="Similarity threshold (0-1)")


class DuplicateCheckerTool(BaseTool):
    name: str = "Duplicate Product Checker"
    description: str = """
    Check if a product already exists in the database.
    Uses fuzzy matching to detect similar product names.
    Returns duplicate check result with similarity score.
    """
    args_schema: Type[BaseModel] = DuplicateCheckerInput
    
    def _run(self, product_name: str, threshold: float = 0.8) -> Dict[str, Any]:
        """Check for duplicate products in database"""
        try:
            db = ProductDatabase(settings.DATABASE_PATH)
            existing_product = db.check_duplicate_by_name(product_name, threshold)

            if existing_product:
                similarity = SequenceMatcher(
                    None, product_name.lower(), existing_product.name.lower()
                ).ratio()

                return {
                    "is_duplicate": True,
                    "existing_product_id": existing_product.id,
                    "similarity_score": similarity,
                    "reason": f"Product '{product_name}' is similar to existing product '{existing_product.name}' (similarity: {similarity:.2%})",
                }
            else:
                return {
                    "is_duplicate": False,
                    "existing_product_id": None,
                    "similarity_score": 0.0,
                    "reason": f"No duplicate found for '{product_name}'",
                }

        except Exception as e:
            return {
                "is_duplicate": False,
                "error": str(e),
                "reason": f"Error checking duplicates: {e}",
            }
