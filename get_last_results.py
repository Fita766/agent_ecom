"""Récupère et affiche les résultats du dernier run du workflow"""
import json
from pathlib import Path
from datetime import datetime

output_dir = Path("output")

print("=" * 80)
print("RECUPERATION DES RESULTATS DU DERNIER RUN")
print("=" * 80)

# 1. Chercher le fichier last_results.txt (le plus récent)
last_file = output_dir / "last_results.txt"
if last_file.exists():
    print(f"\n[FICHIER] {last_file}")
    print("-" * 80)
    with open(last_file, "r", encoding="utf-8") as f:
        content = f.read()
    print(content)
    print("-" * 80)
else:
    print("\n[INFO] Fichier last_results.txt non trouve.")

# 2. Chercher tous les fichiers de résultats JSON
json_files = sorted(output_dir.glob("results_*.json"), reverse=True)
if json_files:
    print(f"\n[FICHIERS JSON DISPONIBLES] {len(json_files)} fichiers trouves")
    print("\nLes 3 plus recents:")
    for i, json_file in enumerate(json_files[:3], 1):
        print(f"  {i}. {json_file.name}")
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            timestamp = data.get("timestamp", "Unknown")
            print(f"     Timestamp: {timestamp}")
        except:
            pass
    
    # Afficher le plus récent en détail
    if json_files:
        print(f"\n[CONTENU DU PLUS RECENT] {json_files[0].name}")
        print("-" * 80)
        try:
            with open(json_files[0], "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "results" in data:
                results = data["results"]
                if isinstance(results, dict):
                    print(json.dumps(results, indent=2, ensure_ascii=False))
                else:
                    print(results)
            else:
                print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Erreur lecture JSON: {e}")
        print("-" * 80)

# 3. Chercher dans la base de données
db_path = output_dir / "products.db"
if db_path.exists():
    import sqlite3
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, created_at, data 
            FROM products 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            name, created, data_json = row
            print(f"\n[DERNIER ENREGISTREMENT BASE DE DONNEES]")
            print(f"Nom: {name}")
            print(f"Cree le: {created}")
            print("-" * 80)
            try:
                data = json.loads(data_json)
                if "raw_results" in data:
                    print(data["raw_results"][:1000])
                    if len(data["raw_results"]) > 1000:
                        print(f"\n... (tronque, {len(data['raw_results'])} caracteres au total)")
                else:
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
            except:
                print(data_json[:500])
            print("-" * 80)
        conn.close()
    except Exception as e:
        print(f"\n[ERREUR] Impossible de lire la base de donnees: {e}")

print("\n" + "=" * 80)
print("[ASTUCE] Pour voir tous les resultats:")
print(f"  - Fichier texte: {output_dir}/last_results.txt")
print(f"  - Fichiers JSON: {output_dir}/results_*.json")
print(f"  - Base de donnees: {output_dir}/products.db")
print("=" * 80)
