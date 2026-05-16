# export_openapi.py
import requests
import json
import urllib3

# Ignorer les warnings de version (sans danger ici)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Utiliser localhost pour une meilleure compatibilité Windows IPv4/IPv6
API_URL = "http://localhost:8000/openapi.json"

try:
    print(f"📡 Connexion au serveur Ministère sur {API_URL}...")
    resp = requests.get(API_URL, timeout=10)
    
    if resp.status_code == 200:
        with open("ministry-api-contract.json", "w", encoding="utf-8") as f:
            json.dump(resp.json(), f, indent=2, ensure_ascii=False)
        print("✅ Fichier ministry-api-contract.json généré !")
        print(f"📦 Taille: {len(resp.content)} octets")
    else:
        print(f"⚠️ Le serveur a répondu avec le code {resp.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Impossible de joindre le serveur.")
    print("💡 Vérifiez que uvicorn tourne avec --host 0.0.0.0")
except Exception as e:
    print(f"❌ Erreur inattendue : {e}")