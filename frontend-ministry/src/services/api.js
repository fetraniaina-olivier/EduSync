// src/services/api.js
const API_BASE = 'http://localhost:8000/api/v1';

function getHeaders() {
  const token = localStorage.getItem('ministry_token');
  return token ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } : {};
}

export const api = {
  // Récupérer les stats du dashboard
  async getStats() {
    const res = await fetch(`${API_BASE}/sync/stats`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erreur lors du chargement des stats');
    return res.json();
  },

  // Récupérer la liste des écoles
  async getSchools() {
    const res = await fetch(`${API_BASE}/sync/schools`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erreur lors du chargement des écoles');
    return res.json();
  },

  // Récupérer les activités récentes
  async getActivities() {
    const res = await fetch(`${API_BASE}/sync/activities`, { headers: getHeaders() });
    if (!res.ok) throw new Error('Erreur lors du chargement des activités');
    return res.json();
  }
};