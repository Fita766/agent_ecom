# 🔑 Informations sur les Clés API Requises

## RAPID_API_KEY

**Où elle est utilisée :**
- **Fichier :** `tools/tiktok_scraper.py` (ligne 37)
- **Agent :** `TrendScout Agent` (`agents/research_agents.py`)
- **Outil :** `TikTokScraperTool`
- **Usage :** Scraping de données TikTok via l'API RapidAPI pour identifier les produits tendance

**Comment l'obtenir :**
1. Créer un compte sur [RapidAPI](https://rapidapi.com/)
2. Souscrire à l'API "TikTok Scraper" (ex: `tiktok-scraper7`)
3. Copier votre clé API depuis le dashboard RapidAPI
4. L'ajouter dans votre fichier `.env` : `RAPID_API_KEY=votre_cle_ici`

**Alternative :** Si tu ne veux pas utiliser RapidAPI, tu peux modifier `TikTokScraperTool` pour utiliser une autre méthode (scraping direct, autre API, etc.)

---

## APIFY_API_TOKEN

**Où elle est définie :**
- **Fichier :** `utils/config.py` (ligne 16)
- **Usage actuel :** **AUCUN** - Cette clé est définie mais **non utilisée** dans le code actuel

**Pourquoi elle est là :**
- Probablement prévue pour utiliser des Actors Apify pour le scraping (alternative plus robuste que le scraping direct)
- Peut être utilisée pour des scrapers Apify pour TikTok, Pinterest, Amazon, AliExpress, etc.

**Si tu veux l'utiliser :**
1. Créer un compte sur [Apify](https://apify.com/)
2. Obtenir ton API token depuis le dashboard Apify
3. L'ajouter dans `.env` : `APIFY_API_TOKEN=votre_token_ici`
4. Modifier les tools de scraping pour utiliser les Actors Apify au lieu du scraping direct

**Note :** Pour l'instant, le système fonctionne sans cette clé car elle n'est pas utilisée.

---

## 📝 Fichier .env à créer

Crée un fichier `.env` à la racine du projet avec :

```env
# Shopify
SHOPIFY_ADMIN_TOKEN=ton_token_shopify
SHOPIFY_STORE_URL=ton_nom_de_boutique

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
