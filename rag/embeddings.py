"""
Gestionnaire d'embeddings pour créer des vector stores
à partir des datasets Kaggle
"""

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from typing import List, Dict, Any, Optional
from tqdm import tqdm


class EmbeddingManager:
    """Crée et gère les embeddings pour RAG"""
    
    def __init__(self, model_name='sentence-transformers/all-mpnet-base-v2'):
        """
        Args:
            model_name: Nom du modèle HuggingFace pour embeddings
                       - all-mpnet-base-v2: Meilleur all-around (768 dim)
                       - all-MiniLM-L6-v2: Plus rapide, moins précis (384 dim)
        """
        print(f"🔄 Chargement modèle embeddings: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        print("✅ Modèle chargé")
    
    def create_amazon_embeddings(self, csv_path: str, output_dir: str):
        """
        Crée embeddings pour dataset Amazon Sales
        
        Args:
            csv_path: Chemin vers CSV Amazon (ex: datasets/amazon_sales/amazon.csv)
            output_dir: Dossier sortie embeddings
        """
        print(f"\n📊 Création embeddings Amazon: {csv_path}")
        
        # Charger CSV
        df = pd.read_csv(csv_path, nrows=100000)  # Limite pour mémoire
        print(f"✅ {len(df)} produits chargés")
        
        # Créer texte pour embedding
        texts = []
        metadatas = []
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Préparation"):
            # Colonnes typiques: product_name, category, price, rating, reviews_count
            try:
                text = f"{row.get('product_name', '')} {row.get('category', '')}"
                texts.append(text)
                
                metadata = {
                    'product_id': str(idx),
                    'product_name': row.get('product_name', ''),
                    'category': row.get('category', ''),
                    'price': float(row.get('actual_price', 0) or row.get('discounted_price', 0) or 0),
                    'rating': float(row.get('rating', 0) or 0),
                    'reviews_count': int(row.get('rating_count', 0) or 0)
                }
                metadatas.append(metadata)
            except Exception as e:
                print(f"⚠️  Skip row {idx}: {e}")
                continue
        
        # Créer embeddings
        print(f"\n🔄 Création {len(texts)} embeddings...")
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32
        )
        
        # Sauvegarder
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        data = {
            'embeddings': embeddings,
            'texts': texts,
            'metadatas': metadatas,
            'model_name': self.model_name
        }
        
        save_path = output_path / 'amazon_embeddings.pkl'
        with open(save_path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"✅ Embeddings sauvegardés: {save_path}")
        print(f"📊 Shape: {embeddings.shape}")
        
        return save_path
    
    def create_tiktok_embeddings(self, csv_path: str, output_dir: str):
        """Crée embeddings pour dataset TikTok Trends"""
        print(f"\n📊 Création embeddings TikTok: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"✅ {len(df)} vidéos chargées")
        
        texts = []
        metadatas = []
        
        for idx, row in tqdm(df.iterrows(), total=len(df), desc="Préparation"):
            try:
                # Colonnes TikTok: video_description, hashtags, likes, shares
                hashtags = row.get('hashtags', '')
                desc = row.get('video_description', '') or row.get('title', '')
                
                text = f"{desc} {hashtags}"
                texts.append(text)
                
                metadata = {
                    'video_id': str(idx),
                    'description': desc,
                    'hashtags': hashtags,
                    'likes': int(row.get('diggCount', 0) or row.get('likes', 0) or 0),
                    'shares': int(row.get('shareCount', 0) or row.get('shares', 0) or 0),
                    'views': int(row.get('playCount', 0) or row.get('views', 0) or 0),
                    'engagement_rate': float(row.get('engagement_rate', 0) or 0)
                }
                metadatas.append(metadata)
            except Exception as e:
                print(f"⚠️  Skip row {idx}: {e}")
                continue
        
        print(f"\n🔄 Création {len(texts)} embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=32)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        data = {
            'embeddings': embeddings,
            'texts': texts,
            'metadatas': metadatas,
            'model_name': self.model_name
        }
        
        save_path = output_path / 'tiktok_embeddings.pkl'
        with open(save_path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"✅ Embeddings sauvegardés: {save_path}")
        return save_path


def create_embeddings(dataset_type: str, csv_path: str, output_dir: str = "rag/embeddings"):
    """
    Fonction helper pour créer embeddings
    
    Args:
        dataset_type: 'amazon' ou 'tiktok'
        csv_path: Chemin vers CSV
        output_dir: Dossier sortie
    
    Example:
        create_embeddings('amazon', 'datasets/amazon_sales/amazon.csv')
    """
    manager = EmbeddingManager()
    
    if dataset_type == 'amazon':
        return manager.create_amazon_embeddings(csv_path, output_dir)
    elif dataset_type == 'tiktok':
        return manager.create_tiktok_embeddings(csv_path, output_dir)
    else:
        raise ValueError(f"Type invalide: {dataset_type}. Utiliser 'amazon' ou 'tiktok'")


if __name__ == "__main__":
    # Test script
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python embeddings.py <type> <csv_path>")
        print("Types: amazon, tiktok")
        sys.exit(1)
    
    dataset_type = sys.argv[1]
    csv_path = sys.argv[2]
    
    create_embeddings(dataset_type, csv_path)
