# 🚀 CrewAI Product Research & Shopify Automation

Système multi-agents intelligent pour la recherche de produits gagnants et l'automatisation Shopify, utilisant CrewAI et Ollama.

## 📋 Description

Ce projet automatise complètement le processus de recherche de produits rentables pour le dropshipping, de la découverte de tendances sur les réseaux sociaux jusqu'à la création automatique de pages Shopify. Le système utilise **17 agents spécialisés** qui travaillent en séquence pour analyser, valider et publier des produits.

## ✨ Fonctionnalités

### 🔍 Phase 1 : Research & Discovery
- **Trend Scout** : Découverte de produits viraux sur TikTok et Pinterest
- **Market Analyzer** : Analyse approfondie du marché (taille, compétition, géographie)
- **Competitor Intel** : Intelligence concurrentielle et opportunités

### 💰 Phase 2 : Price & Supplier Intelligence
- **AliExpress Scraper** : Recherche de fournisseurs avec prix, ratings, shipping
- **Amazon Scraper** : Analyse des prix concurrents
- **Pricing Strategist** : Calcul des marges optimales (min 30%)

### ✅ Phase 3 : Quality & Validation
- **Review Analyzer** : Analyse sentiment des avis clients
- **Trend Validator** : Validation via Google Trends et réseaux sociaux
- **Duplicate Checker** : Détection de doublons dans la base de données

### 🎯 Phase 4 : Decision & Scoring
- **Scoring Engine** : Calcul de score global (0-100) sur 6 dimensions
- **Decision Maker** : Validation finale GO/NO-GO

### 🛍️ Phase 5 : Shopify Automation
- **Theme Builder** : Sélection et configuration du thème
- **Product Page Creator** : Création de fiches produits optimisées
- **Landing Page Builder** : Pages de vente haute conversion
- **SEO Optimizer** : Optimisation pour les moteurs de recherche

### 📊 Phase 6 : Management & Reporting
- **Project Manager** : Orchestration globale du workflow
- **Report Generator** : Rapport final détaillé

## 🏗️ Architecture

```
agents/          # 17 agents spécialisés
├── research_agents.py      # Trend Scout, Market Analyzer, Competitor Intel
├── scraper_agents.py       # AliExpress, Amazon, Pricing Strategist
├── validation_agents.py    # Review Analyzer, Trend Validator, Duplicate Checker
├── decision_agents.py      # Scoring Engine, Decision Maker
├── shopify_agents.py       # Theme Builder, Product Page, Landing Page, SEO
└── management_agents.py    # Project Manager, Report Generator

tasks/           # 16 tasks orchestrées
├── research_tasks.py
├── scraping_tasks.py
├── validation_tasks.py
├── decision_tasks.py
├── shopify_tasks.py
└── reporting_tasks.py

tools/           # Outils de scraping et intégration
├── tiktok_scraper.py
├── pinterest_scraper.py
├── aliexpress_scraper.py
├── amazon_scraper.py
├── google_trends.py
├── shopify_tool.py
└── duplicate_checker_tool.py

models/          # Modèles Pydantic
└── product_models.py

utils/           # Configuration et utilitaires
├── config.py    # Configuration centralisée
├── database.py  # Gestion SQLite
└── llm.py       # Intégration Ollama
```

## 🛠️ Installation

### Prérequis

- **Python 3.10+**
- **Ollama** installé et configuré
- **Modèle DeepSeek** : `deepseek-r1:8b`

### Étapes

1. **Cloner le repository**
```bash
git clone https://github.com/TON_USERNAME/TON_REPO.git
cd TON_REPO
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Installer et configurer Ollama**
```bash
# Télécharger Ollama depuis https://ollama.com
# Puis télécharger le modèle DeepSeek
ollama pull deepseek-r1:8b
```

4. **Configurer les variables d'environnement**
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer .env et remplir tes clés API
```

## ⚙️ Configuration

### Fichier `.env`

Crée un fichier `.env` à la racine du projet :

```env
# Shopify
SHOPIFY_ADMIN_TOKEN=ton_token_shopify
SHOPIFY_STORE_URL=ton-nom-de-boutique

# APIs
RAPID_API_KEY=ta_cle_rapidapi
APIFY_API_TOKEN=ton_token_apify_optional

# LLM
OLLAMA_MODEL=deepseek-r1:8b
OLLAMA_BASE_URL=http://localhost:11434

# Scraping
MAX_TIKTOK_VIDEOS=3
MAX_PINTEREST_PINS=5

# Scoring Thresholds
MIN_APPROVAL_SCORE=75.0
MAX_PRODUCT_WEIGHT_KG=5.0
MIN_PROFIT_MARGIN_PERCENT=30.0

# Output
OUTPUT_DIR=output
DATABASE_PATH=output/products.db
```

### Clés API requises

#### RapidAPI (TikTok Scraper)
1. Créer un compte sur [RapidAPI](https://rapidapi.com/)
2. Souscrire à l'API "TikTok Scraper" (ex: `tiktok-scraper7`)
3. Copier ta clé API dans `.env`

#### Shopify
1. Créer une app privée dans ton admin Shopify
2. Générer un Admin API access token
3. Ajouter le token dans `.env`

#### Apify (Optionnel)
- Utilisé pour des scrapers plus robustes
- Créer un compte sur [Apify](https://apify.com/)
- Ajouter le token dans `.env` si tu veux utiliser des Actors Apify

## 🚀 Utilisation

### Lancer le workflow complet

```bash
python main.py
```

Le système va :
1. Initialiser la base de données SQLite
2. Créer le crew avec tous les agents et tasks
3. Exécuter le workflow séquentiel
4. Sauvegarder les résultats dans `output/`

### Workflow séquentiel

Les 16 tasks s'exécutent dans cet ordre :

```
1. Trend Discovery (TikTok/Pinterest)
2. Market Analysis
3. Competitor Analysis
4. AliExpress Sourcing
5. Amazon Pricing
6. Review Analysis
7. Trend Validation (Google Trends)
8. Duplicate Check
9. Pricing Strategy
10. Product Scoring
11. Final Decision
12. Shopify Theme Setup
13. Product Page Creation
14. Landing Page Creation
15. SEO Optimization
16. Final Report
```

## 📊 Résultats

Les résultats sont sauvegardés dans :
- **Base de données** : `output/products.db` (SQLite)
- **Fichiers JSON** : `output/` (résultats détaillés par phase)

## 🔧 Technologies utilisées

- **CrewAI** : Framework multi-agents
- **Ollama + DeepSeek** : LLM local (100% gratuit)
- **LangChain** : Intégration LLM
- **Pydantic** : Validation de données
- **SQLite** : Base de données locale
- **BeautifulSoup4** : Web scraping
- **Shopify API** : Automatisation Shopify
- **Google Trends API** : Validation des tendances

## 📁 Structure du projet

```
.
├── agents/              # Agents CrewAI
├── tasks/              # Tasks CrewAI
├── tools/              # Outils personnalisés
├── models/             # Modèles Pydantic
├── utils/              # Utilitaires
├── output/             # Résultats (ignoré par git)
├── main.py             # Point d'entrée
├── requirements.txt    # Dépendances Python
├── .env.example        # Exemple de configuration
├── .gitignore          # Fichiers ignorés
└── README.md           # Ce fichier
```

## ⚠️ Notes importantes

### Limitations actuelles

- **Google Trends** : Peut retourner des erreurs 429 (rate limiting) si trop de requêtes
- **Scraping** : Les scrapers AliExpress/Amazon utilisent des méthodes simplifiées (mock data en fallback)
- **Reviews** : L'analyse d'avis nécessite des données réelles (non implémentée actuellement)

### Améliorations futures

- [ ] Intégration complète avec Apify pour un scraping plus robuste
- [ ] Parser les résultats CrewAI en objets `WinningProduct` structurés
- [ ] Interface web pour visualiser les résultats
- [ ] Export Excel/CSV des produits validés
- [ ] Support de plusieurs modèles LLM (OpenAI, Anthropic, etc.)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à :
- Ouvrir une issue pour signaler un bug
- Proposer des améliorations
- Soumettre une pull request

## 📝 License

Ce projet est open source. Utilise-le librement pour tes projets.

## 🙏 Remerciements

- **CrewAI** pour le framework multi-agents
- **Ollama** pour l'infrastructure LLM locale
- **DeepSeek** pour le modèle de langage

---

**Made with ❤️ using CrewAI and Ollama**
