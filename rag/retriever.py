"""
Retriever RAG pour rechercher dans les vector stores
et enrichir le contexte des agents
"""

import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class ProductRAGRetriever:
    """Récupère contexte historique pour enrichir agents"""
    
    def __init__(self, embeddings_dir='rag/embeddings'):
        self.embeddings_dir = Path(embeddings_dir)
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        
        # Charger embeddings pré-calculés
        self.amazon_data = self._load_embeddings('amazon_embeddings.pkl')
        self.tiktok_data = self._load_embeddings('tiktok_embeddings.pkl')
        
        print("✅ RAG Retriever initialisé")
    
    def _load_embeddings(self, filename: str) -> Optional[Dict]:
        """Charge embeddings depuis pickle"""
        path = self.embeddings_dir / filename
        
        if not path.exists():
            print(f"⚠️  Embeddings non trouvés: {path}")
            print(f"   Exécuter: python scripts/create_embeddings.py")
            return None
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        print(f"✅ Chargé: {filename} ({data['embeddings'].shape[0]} items)")
        return data
    
    def search_similar_products(
        self,
        query: str,
        source: str = 'amazon',
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Recherche produits similaires dans base historique
        
        Args:
            query: Texte recherche (ex: "wireless earbuds")
            source: 'amazon' ou 'tiktok'
            top_k: Nombre résultats
        
        Returns:
            Liste de produits similaires avec métadonnées
        """
        # Sélectionner source
        data = self.amazon_data if source == 'amazon' else self.tiktok_data
        
        if data is None:
            return []
        
        # Créer embedding requête
        query_embedding = self.model.encode([query])[0]
        
        # Calculer similarités
        similarities = cosine_similarity(
            [query_embedding],
            data['embeddings']
        )[0]
        
        # Top K indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Construire résultats
        results = []
        for idx in top_indices:
            result = {
                **data['metadatas'][idx],
                'similarity_score': float(similarities[idx]),
                'matched_text': data['texts'][idx]
            }
            results.append(result)
        
        return results
    
    def get_market_insights(
        self,
        product_name: str,
        category: str
    ) -> Dict[str, Any]:
        """
        Génère insights marché à partir données historiques
        
        Returns:
            {
                'avg_price': 29.99,
                'avg_rating': 4.3,
                'total_similar_products': 156,
                'demand_level': 'high',
                'competition_level': 'medium',
                'historical_trend': 'rising'
            }
        """
        # Rechercher produits similaires
        similar = self.search_similar_products(
            f"{product_name} {category}",
            source='amazon',
            top_k=50
        )
        
        if not similar:
            return {
                'error': 'No historical data found',
                'recommendation': 'New niche - high risk, high reward'
            }
        
        # Calculer statistiques
        prices = [p['price'] for p in similar if p.get('price', 0) > 0]
        ratings = [p['rating'] for p in similar if p.get('rating', 0) > 0]
        review_counts = [p['reviews_count'] for p in similar if p.get('reviews_count', 0) > 0]
        
        insights = {
            'total_similar_products': len(similar),
            'avg_price': np.mean(prices) if prices else 0,
            'price_range_min': np.min(prices) if prices else 0,
            'price_range_max': np.max(prices) if prices else 0,
            'avg_rating': np.mean(ratings) if ratings else 0,
            'avg_reviews': np.mean(review_counts) if review_counts else 0,
            
            # Déterminer niveaux
            'demand_level': self._calculate_demand_level(review_counts),
            'competition_level': self._calculate_competition_level(len(similar)),
            'quality_benchmark': np.mean(ratings) if ratings else 0,
            
            # Top 3 produits
            'top_performing_products': similar[:3]
        }
        
        return insights
    
    def get_viral_patterns(self, product_keywords: str) -> Dict[str, Any]:
        """Analyse patterns de viralité TikTok"""
        if self.tiktok_data is None:
            return {'error': 'TikTok data not loaded'}
        
        # Rechercher vidéos similaires
        similar_videos = self.search_similar_products(
            product_keywords,
            source='tiktok',
            top_k=20
        )
        
        if not similar_videos:
            return {'virality_potential': 'unknown'}
        
        # Analyser engagement
        total_likes = sum(v['likes'] for v in similar_videos)
        total_shares = sum(v['shares'] for v in similar_videos)
        total_views = sum(v['views'] for v in similar_videos)
        
        avg_engagement = np.mean([v['engagement_rate'] for v in similar_videos])
        
        # Extraire hashtags populaires
        all_hashtags = []
        for v in similar_videos:
            hashtags = v.get('hashtags', '').split()
            all_hashtags.extend(hashtags)
        
        from collections import Counter
        top_hashtags = Counter(all_hashtags).most_common(5)
        
        return {
            'viral_potential_score': self._calculate_viral_score(avg_engagement),
            'avg_likes': total_likes / len(similar_videos),
            'avg_shares': total_shares / len(similar_videos),
            'avg_views': total_views / len(similar_videos),
            'avg_engagement_rate': avg_engagement,
            'recommended_hashtags': [h[0] for h in top_hashtags],
            'trend_status': 'hot' if avg_engagement > 0.15 else 'warm' if avg_engagement > 0.08 else 'cold'
        }
    
    def enrich_agent_context(
        self,
        product_name: str,
        category: str,
        product_keywords: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fonction principale: enrichit contexte agent avec RAG
        
        À utiliser dans chaque agent pour ajouter données historiques
        """
        context = {
            'rag_enabled': True,
            'market_insights': self.get_market_insights(product_name, category)
        }
        
        # Ajouter patterns viraux si keywords fournis
        if product_keywords:
            context['viral_patterns'] = self.get_viral_patterns(product_keywords)
        
        # Ajouter produits similaires
        context['similar_products_amazon'] = self.search_similar_products(
            f"{product_name} {category}",
            source='amazon',
            top_k=5
        )
        
        return context
    
    # Helper methods
    def _calculate_demand_level(self, review_counts: List[int]) -> str:
        if not review_counts:
            return 'unknown'
        avg = np.mean(review_counts)
        if avg > 5000:
            return 'very_high'
        elif avg > 1000:
            return 'high'
        elif avg > 200:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_competition_level(self, num_products: int) -> str:
        if num_products > 100:
            return 'very_high'
        elif num_products > 50:
            return 'high'
        elif num_products > 20:
            return 'medium'
        else:
            return 'low'
    
    def _calculate_viral_score(self, engagement_rate: float) -> float:
        """Score 0-100 basé sur engagement"""
        # Engagement >20% = très viral
        return min(100, engagement_rate * 500)


if __name__ == "__main__":
    # Test retriever
    retriever = ProductRAGRetriever()
    
    # Test recherche
    results = retriever.search_similar_products("wireless earbuds", top_k=3)
    print("\n📊 Produits similaires:")
    for r in results:
        print(f"  - {r['product_name']} (score: {r['similarity_score']:.3f})")
    
    # Test insights
    insights = retriever.get_market_insights("bluetooth speaker", "electronics")
    print(f"\n💡 Market Insights: {insights}")
