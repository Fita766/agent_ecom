import sqlite3
import json
from pathlib import Path

db_path = "output/products.db"

if not Path(db_path).exists():
    print(f"[ERREUR] Base de donnees non trouvee: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Compter les produits
cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]
print(f"\n[INFO] Nombre de produits dans la base: {count}\n")

if count == 0:
    print("La base de donnees est vide.")
    conn.close()
    exit(0)

# Afficher tous les produits
cursor.execute("""
    SELECT name, category, overall_score, is_approved, created_at, data 
    FROM products 
    ORDER BY overall_score DESC
""")

print("=" * 80)
print("PRODUITS TROUVES")
print("=" * 80)

for row in cursor.fetchall():
    name, category, score, approved, created, data_json = row
    
    print(f"\nNom: {name}")
    print(f"Categorie: {category}")
    print(f"Score: {score:.1f}/100" if score else "Score: N/A")
    print(f"Approuve: {'Oui' if approved else 'Non'}")
    print(f"Cree le: {created}")
    
    # Afficher quelques détails du JSON
    try:
        data = json.loads(data_json)
        if 'description' in data:
            desc = data['description'][:100] + "..." if len(data.get('description', '')) > 100 else data.get('description', '')
            print(f"Description: {desc}")
        if 'source' in data and 'url' in data['source']:
            print(f"Source: {data['source']['url']}")
    except:
        pass
    
    print("-" * 80)

conn.close()
print("\n[OK] Affichage termine!")
