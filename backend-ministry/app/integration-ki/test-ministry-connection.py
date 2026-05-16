# À envoyer à l'équipe 2
import requests
import json

MINISTRY_URL = "http://localhost:8000/api/v1/sync/health"

try:
    resp = requests.get(MINISTRY_URL, timeout=5)
    if resp.status_code == 200:
        print("✅ Connexion Ministère OK !")
        print("📦 Réponse :", resp.json())
    else:
        print(f"⚠️ Le Ministère répond mais avec le code {resp.status_code}")
except requests.exceptions.ConnectionError:
    print("❌ Impossible de joindre le Ministère. Vérifiez que le port 8000 est ouvert.")
except Exception as e:
    print(f"❌ Erreur : {e}")