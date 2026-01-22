"""
Module RAG (Retrieval-Augmented Generation) pour enrichir les agents
avec des données historiques et des modèles ML
"""

from .embeddings import create_embeddings, EmbeddingManager
from .retriever import ProductRAGRetriever
from .context_builder import ContextBuilder
from .sentiment_analyzer import SentimentAnalyzer
from .trend_predictor import TrendPredictor

__all__ = [
    'create_embeddings',
    'EmbeddingManager',
    'ProductRAGRetriever',
    'ContextBuilder',
    'SentimentAnalyzer',
    'TrendPredictor'
]
