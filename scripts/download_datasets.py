"""
Script automatisé pour télécharger tous les datasets Kaggle nécessaires
"""
import os
import subprocess
from pathlib import Path
import zipfile

class DatasetDownloader:
    def __init__(self, base_dir="datasets"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        self.datasets = {
            'amazon_sales': {
                'kaggle_id': 'karkavelrajaj/amazon-sales-dataset',
                'size': '~1.2GB',
                'description': 'Amazon sales historical data for demand prediction'
            },
            'amazon_products_2023': {
                'kaggle_id': 'lokeshparab/amazon-products-dataset',
                'size': '~500MB',
                'description': 'Amazon products 2023 with reviews and ratings'
            },
            'tiktok_trends': {
                'kaggle_id': 'lykin22/tiktok-trending-data',
                'size': '~200MB',
                'description': 'TikTok viral videos and engagement metrics'
            },
            'ecommerce_behavior': {
                'kaggle_id': 'uom190346a/e-commerce-customer-behavior-dataset',
                'size': '~500MB',
                'description': 'Customer behavior and conversion patterns'
            },
            'sentiment_data': {
                'kaggle_id': 'abhi8923shriv/sentiment-analysis-dataset',
                'size': '~100MB',
                'description': 'Pre-labeled sentiment analysis training data'
            },
            'retailrocket': {
                'kaggle_id': 'retailrocket/ecommerce-dataset',
                'size': '~300MB',
                'description': 'E-commerce user behavior and conversion data'
            }
        }
    
    def check_kaggle_setup(self):
        """Vérifie que Kaggle CLI est configuré"""
        kaggle_json = Path.home() / '.kaggle' / 'kaggle.json'
        
        if not kaggle_json.exists():
            print("❌ Kaggle API non configuré!")
            print("\n📋 Étapes:")
            print("1. Aller sur https://www.kaggle.com/account")
            print("2. Cliquer 'Create New API Token'")
            print("3. Placer kaggle.json dans:", kaggle_json.parent)
            return False
        
        print("✅ Kaggle API configuré")
        return True
    
    def download_dataset(self, name, info):
        """Télécharge et extrait un dataset"""
        dataset_dir = self.base_dir / name
        dataset_dir.mkdir(exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"📦 Téléchargement: {name}")
        print(f"📊 Dataset: {info['kaggle_id']}")
        print(f"💾 Taille: {info['size']}")
        print(f"📝 Description: {info['description']}")
        print(f"{'='*60}")
        
        # Vérifier si déjà téléchargé
        if list(dataset_dir.glob('*.csv')) or list(dataset_dir.glob('*.json')):
            print(f"⚠️  Dataset déjà présent dans {dataset_dir}")
            response = input("Télécharger à nouveau? (y/N): ")
            if response.lower() != 'y':
                print("⏭️  Ignoré")
                return True
        
        try:
            # Télécharger
            subprocess.run([
                'kaggle', 'datasets', 'download',
                info['kaggle_id'],
                '-p', str(dataset_dir)
            ], check=True)
            
            # Extraire ZIP si présent
            zip_files = list(dataset_dir.glob('*.zip'))
            for zip_path in zip_files:
                print(f"📂 Extraction: {zip_path.name}")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(dataset_dir)
                zip_path.unlink()  # Supprimer ZIP après extraction
            
            print(f"✅ Téléchargé: {name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur téléchargement {name}: {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
    
    def download_all(self, skip_large=False):
        """Télécharge tous les datasets"""
        if not self.check_kaggle_setup():
            return
        
        print(f"\n🚀 Début téléchargement de {len(self.datasets)} datasets...")
        
        results = {}
        for name, info in self.datasets.items():
            # Option pour skip datasets lourds
            if skip_large and '1.2GB' in info['size']:
                print(f"\n⏭️  Skip {name} (trop lourd)")
                continue
            
            success = self.download_dataset(name, info)
            results[name] = success
        
        # Résumé
        print(f"\n{'='*60}")
        print("📊 RÉSUMÉ")
        print(f"{'='*60}")
        
        for name, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {name}")
        
        total = len(results)
        successful = sum(results.values())
        print(f"\n✅ {successful}/{total} datasets téléchargés")


if __name__ == "__main__":
    downloader = DatasetDownloader()
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   🤖 TÉLÉCHARGEMENT DATASETS KAGGLE - RAG E-COMMERCE      ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    print("\nOptions:")
    print("1. Télécharger TOUS les datasets (~3GB)")
    print("2. Télécharger SANS les gros datasets (~1.5GB)")
    print("3. Télécharger UN SEUL dataset")
    print("4. Quitter")
    
    choice = input("\nChoix (1-4): ")
    
    if choice == "1":
        downloader.download_all(skip_large=False)
    elif choice == "2":
        downloader.download_all(skip_large=True)
    elif choice == "3":
        print("\nDatasets disponibles:")
        for i, (name, info) in enumerate(downloader.datasets.items(), 1):
            print(f"{i}. {name} ({info['size']}) - {info['description']}")
        
        idx = int(input("\nChoisir numéro: ")) - 1
        name = list(downloader.datasets.keys())[idx]
        info = downloader.datasets[name]
        downloader.download_dataset(name, info)
    else:
        print("❌ Annulé")
