"""Script pour tester si la clé RapidAPI fonctionne"""
import requests
from utils.config import settings

def test_rapidapi_key():
    """Teste la clé RapidAPI pour TikTok"""
    print("=" * 80)
    print("TEST DE LA CLE RAPIDAPI")
    print("=" * 80)
    
    api_key = settings.RAPID_API_KEY
    if not api_key:
        print("[ERREUR] RAPID_API_KEY non configuree dans config.py")
        return
    
    print(f"\nCle API trouvee: {api_key[:20]}...{api_key[-10:]}")
    print("\nTest de l'API TikTok Scraper...")
    
    url = "https://tiktok-scraper7.p.rapidapi.com/search/keyword"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
    }
    params = {
        "keyword": "home gadgets",
        "count": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("[OK] API fonctionne correctement!")
            print(f"Reponse: {str(data)[:200]}...")
        elif response.status_code == 401:
            print("[ERREUR] Cle API invalide ou expiree")
            print("Solution: Verifiez votre cle sur https://rapidapi.com/developer/billing")
        elif response.status_code == 429:
            print("[ERREUR] Rate limit depasse ou credits epuises")
            print("Solution: Attendez ou rechargez vos credits sur RapidAPI")
        elif response.status_code == 403:
            print("[ERREUR] Acces refuse - peut-etre que l'API n'est plus disponible")
            print("Solution: Verifiez sur RapidAPI si l'API 'tiktok-scraper7' existe toujours")
        else:
            print(f"[ERREUR] Status code inattendu: {response.status_code}")
            print(f"Reponse: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR] Erreur de connexion: {e}")
    except Exception as e:
        print(f"[ERREUR] Erreur inattendue: {e}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_rapidapi_key()
