# ️ Système de synchronisation de données entre institutions

Plateforme sécurisée de centralisation et de synchronisation des données scolaires entre les établissements et le Ministère de l'Enseignement.  
Architecture découplée, authentification JWT, dashboard analytique et traçabilité complète des opérations.

---

## Description

Ce projet implémente une solution complète de gestion et de synchronisation de données éducatives. Il permet aux institutions de gérer leurs inscriptions localement (SQLite) et de pousser automatiquement les données vers une base centralisée (PostgreSQL) au niveau du Ministère. Le système garantit l'intégrité, la sécurité et la disponibilité des informations tout en offrant une visibilité temps réel via des dashboards dédiés.

---

## Fonctionnalités

- **Authentification sécurisée** : JWT multi-rôles (École, Ministère, Super Admin)
- **Synchronisation intelligente** : Push bidirectionnel avec gestion des conflits et traçabilité (`is_synced`, `last_sync_at`)
- **Dashboards analytiques** : Statistiques en temps réel, historique des sync, suivi des établissements
- **Gestion académique** : Étudiants, Enseignants, Programmes, Diplômes, Inscriptions
- **Sécurité renforcée** : CORS strict, validation Pydantic, tokens expirables, isolation des bases
-  **Architecture hybride** : SQLite (local/école) ↔ PostgreSQL (central/ministère)

---

## Stack Technique

| Couche | Technologies |
|--------|--------------|
| **Backend** | FastAPI, Python 3.13, SQLAlchemy (Async), Pydantic, HTTPX, Uvicorn |
| **Frontend** | React 18, Vite, TailwindCSS, React Router, Fetch API |
| **Base de données** | SQLite (École), PostgreSQL (Ministère) |
| **Sécurité** | JWT (Bearer), CORS, Hashage bcrypt, Validation stricte |
| **Outils** | Docker, Git, PowerShell, Swagger UI (OpenAPI) |

---

##  Prérequis

- Python `3.13+`
- Node.js `18+` & npm/yarn
- PostgreSQL (Docker recommandé : `docker run --name ministry-db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=ministry_db -p 5432:5432 -d postgres`)
- Git

---

##  Installation & Démarrage

### 1. Cloner le dépôt
```powershell
git clone https://github.com/fetraniaina-olivier/edu-sync.git
cd edu-sync

cd backend-ministry
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configurer les variables
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

cd ../backend-school
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Configurer les variables
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

# Frontend Ministère
cd ../frontend-ministry
npm install
npm run dev  # http://localhost:5173

# Frontend École
cd ../frontend-school
npm install
npm run dev  # http://localhost:5174

Flux de Synchronisation
Création locale : L'école ajoute un étudiant → is_synced = false dans school.db
Déclenchement : L'utilisateur clique sur Synchroniser
Authentification : Le backend école récupère un token JWT via /auth/login/school
Push sécurisé : Envoi des opérations via POST /api/v1/sync/push avec header Authorization: Bearer <token>
Validation Ministère : Contrôle d'identité, intégrité des données et gestion des conflits
Confirmation : Mise à jour is_synced = true côté école + affichage instantané sur le dashboard Ministère

###########Sécurité & Bonnes Pratiques############
✅ Tokens JWT avec expiration configurable
✅ Validation stricte des payloads via Pydantic
✅ CORS restreint aux origines autorisées
✅ Isolation des bases de données (locale vs centrale)
✅ Hashage des secrets/mots de passe (bcrypt)
✅ Aucun fichier sensible dans le dépôt Git
✅ Logs structurés pour audit et debugging