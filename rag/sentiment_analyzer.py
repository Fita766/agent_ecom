"""
Analyseur de sentiment utilisant modèles HuggingFace pré-entraînés
spécialisés pour avis produits e-commerce
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import List, Dict, Any
from pathlib import Path


class SentimentAnalyzer:
    """Analyse sentiment avec DistilBERT fine-tuned sur Amazon reviews"""
    
    def __init__(self, model_name="sohan-ai/sentiment-analysis-model-amazon-reviews"):
        """
        Args:
            model_name: Modèle HuggingFace
                - sohan-ai/sentiment-analysis-model-amazon-reviews (EN, 95% accuracy)
                - tabularisai/multilingual-sentiment-analysis (FR/ES/IT/DE/NL/EN)
        """
        print(f"🔄 Chargement modèle sentiment: {model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            cache_dir="models/sentiment"
        )
        self.model.eval()  # Mode évaluation
        
        print("✅ Modèle sentiment chargé")
        
    def analyze_single_review(self, review_text: str) -> Dict[str, Any]:
        """
        Analyse un seul avis
        
        Returns:
            {
                'sentiment': 'positive' | 'negative',
                'confidence': 0.95,
                'score': 0.95  # -1 (négatif) à +1 (positif)
            }
        """
        # Tokenize
        inputs = self.tokenizer(
            review_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Prédiction
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(probs, dim=1).item()
            confidence = probs[0][predicted_class].item()
        
        # Mapping: 0 = négatif, 1 = positif
        sentiment = "positive" if predicted_class == 1 else "negative"
        
        # Score normalisé -1 à +1
        score = (probs[0][1].item() - probs[0][0].item())
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'score': score,
            'raw_probabilities': {
                'negative': probs[0][0].item(),
                'positive': probs[0][1].item()
            }
        }
    
    def analyze_batch(self, reviews: List[str]) -> List[Dict[str, Any]]:
        """Analyse plusieurs avis (plus rapide que boucle)"""
        results = []
        
        # Process par batch de 32 pour mémoire
        batch_size = 32
        for i in range(0, len(reviews), batch_size):
            batch = reviews[i:i+batch_size]
            
            inputs = self.tokenizer(
                batch,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)
            
            for j in range(len(batch)):
                predicted_class = torch.argmax(probs[j]).item()
                sentiment = "positive" if predicted_class == 1 else "negative"
                confidence = probs[j][predicted_class].item()
                score = probs[j][1].item() - probs[j][0].item()
                
                results.append({
                    'text': batch[j],
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'score': score
                })
        
        return results
    
    def get_aggregate_analysis(
        self,
        reviews: List[str],
        extract_topics: bool = False
    ) -> Dict[str, Any]:
        """
        Analyse agrégée de tous les avis
        
        Returns:
            {
                'total_reviews': 150,
                'positive_count': 120,
                'negative_count': 30,
                'positive_rate': 0.80,
                'avg_sentiment_score': 0.65,
                'confidence_avg': 0.92,
                'sentiment_distribution': {...}
            }
        """
        # Analyser batch
        results = self.analyze_batch(reviews)
        
        # Statistiques
        positive_count = sum(1 for r in results if r['sentiment'] == 'positive')
        negative_count = len(results) - positive_count
        
        avg_score = sum(r['score'] for r in results) / len(results)
        avg_confidence = sum(r['confidence'] for r in results) / len(results)
        
        analysis = {
            'total_reviews': len(reviews),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'positive_rate': positive_count / len(results) if results else 0,
            'avg_sentiment_score': avg_score,
            'avg_confidence': avg_confidence,
            
            # Distribution détaillée
            'sentiment_distribution': {
                'very_positive': sum(1 for r in results if r['score'] > 0.7),
                'positive': sum(1 for r in results if 0.2 < r['score'] <= 0.7),
                'neutral': sum(1 for r in results if -0.2 <= r['score'] <= 0.2),
                'negative': sum(1 for r in results if -0.7 <= r['score'] < -0.2),
                'very_negative': sum(1 for r in results if r['score'] < -0.7)
            },
            
            # Avis avec score extrême (potentiels red flags ou praise)
            'extreme_positives': [r for r in results if r['score'] > 0.8][:5],
            'extreme_negatives': [r for r in results if r['score'] < -0.8][:5]
        }
        
        # Topic extraction (optionnel, plus lent)
        if extract_topics:
            analysis['topics'] = self._extract_common_topics(reviews)
        
        return analysis
    
    def _extract_common_topics(self, reviews: List[str]) -> Dict[str, int]:
        """Extrait mots-clés fréquents (simple version)"""
        from collections import Counter
        import re
        
        # Mots à ignorer
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'is', 'was', 'it', 'this', 'that', 'very', 'really'}
        
        all_words = []
        for review in reviews:
            # Nettoyer et tokenize simple
            words = re.findall(r'\b[a-z]{3,}\b', review.lower())
            all_words.extend([w for w in words if w not in stop_words])
        
        # Top 10 mots
        return dict(Counter(all_words).most_common(10))


class MultilingualSentimentAnalyzer(SentimentAnalyzer):
    """Version multilingue pour FR, ES, IT, DE, NL, EN"""
    
    def __init__(self):
        model_name = "tabularisai/multilingual-sentiment-analysis"
        print(f"🔄 Chargement modèle multilingue: {model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            cache_dir="models/sentiment"
        )
        self.model.eval()
        
        # Mapping 5-class: Very Negative, Negative, Neutral, Positive, Very Positive
        self.sentiment_map = {
            0: "very_negative",
            1: "negative", 
            2: "neutral",
            3: "positive",
            4: "very_positive"
        }
        
        print("✅ Modèle multilingue chargé")
    
    def analyze_single_review(self, review_text: str, language: str = "en") -> Dict[str, Any]:
        """Supporte FR, ES, IT, DE, NL, EN automatiquement"""
        inputs = self.tokenizer(
            review_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            predicted_class = torch.argmax(probs).item()
            confidence = probs[0][predicted_class].item()
        
        sentiment = self.sentiment_map[predicted_class]
        
        # Normaliser score -1 à +1
        score = (predicted_class - 2) / 2  # 0->-1, 2->0, 4->+1
        
        return {
            'sentiment': sentiment,
            'sentiment_class': predicted_class,
            'confidence': confidence,
            'score': score,
            'language': language
        }


if __name__ == "__main__":
    # Test analyzer
    analyzer = SentimentAnalyzer()
    
    test_reviews = [
        "This product is amazing! Best purchase ever!",
        "Terrible quality, broke after 2 days",
        "It's okay, nothing special"
    ]
    
    print("\n📊 Test Sentiment Analysis:")
    for review in test_reviews:
        result = analyzer.analyze_single_review(review)
        print(f"\n'{review}'")
        print(f"  Sentiment: {result['sentiment']} (confidence: {result['confidence']:.2f})")
        print(f"  Score: {result['score']:.2f}")
    
    # Test batch
    print("\n📊 Analyse Agrégée:")
    aggregate = analyzer.get_aggregate_analysis(test_reviews)
    print(f"  Positive rate: {aggregate['positive_rate']:.1%}")
    print(f"  Avg score: {aggregate['avg_sentiment_score']:.2f}")
