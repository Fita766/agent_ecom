import sqlite3
from typing import List, Optional
from models.product_models import WinningProduct
import json
from datetime import datetime


class ProductDatabase:
    def __init__(self, db_path: str = "output/products.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                data JSON NOT NULL,
                overall_score REAL,
                is_approved INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_score ON products(overall_score DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_approved ON products(is_approved)
        """)
        
        conn.commit()
        conn.close()
    
    def save_product(self, product: WinningProduct):
        """Save or update product"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO products 
            (id, name, category, data, overall_score, is_approved, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product.id,
            product.name,
            product.category.value,
            json.dumps(product.model_dump(), default=str),
            product.score.overall_score,
            1 if product.is_approved else 0,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_all_products(self) -> List[WinningProduct]:
        """Retrieve all products"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM products ORDER BY overall_score DESC")
        
        products = []
        for row in cursor.fetchall():
            data = json.loads(row[0])
            products.append(WinningProduct(**data))
        
        conn.close()
        return products
    
    def check_duplicate_by_name(self, name: str, threshold: float = 0.8) -> Optional[WinningProduct]:
        """Check if similar product exists"""
        from difflib import SequenceMatcher
        
        all_products = self.get_all_products()
        for product in all_products:
            similarity = SequenceMatcher(None, name.lower(), product.name.lower()).ratio()
            if similarity >= threshold:
                return product
        return None
