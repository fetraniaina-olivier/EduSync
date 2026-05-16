const API_URL = 'http://localhost:8001/api/v1';

export const api = {
  async getStudents() {
    const res = await fetch(`${API_URL}/students/`);
    if (!res.ok) throw new Error('Erreur récupération étudiants');
    return res.json();
  },

  async addStudent(data) {
    const res = await fetch(`${API_URL}/students/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error('Erreur ajout étudiant');
    return res.json();
  },

  async triggerSync() {
    const res = await fetch(`${API_URL}/sync/trigger`, { method: 'POST' });
    if (!res.ok) throw new Error('Erreur synchronisation');
    return res.json();
  }
};