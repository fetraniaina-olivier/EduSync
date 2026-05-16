import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export default function SchoolStudents() {
  const { schoolId } = useParams();
  const navigate = useNavigate();
  const [students, setStudents] = useState([]);
  const [school, setSchool] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('ministry_token');
        
        if (!token) {
          setError('Token manquant. Veuillez vous reconnecter.');
          setLoading(false);
          return;
        }

        console.log('🔑 Token:', token ? 'OK ✅' : 'MANQUANT');
        console.log('🎯 School ID:', schoolId);

        // 1. Récupérer les infos de l'école
        const schoolsRes = await fetch('http://localhost:8000/api/v1/sync/schools', {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });

        if (!schoolsRes.ok) {
          if (schoolsRes.status === 401) {
            throw new Error('Session expirée. Veuillez vous reconnecter.');
          }
          throw new Error(`Erreur écoles: ${schoolsRes.status}`);
        }

        const schools = await schoolsRes.json();
        console.log('📦 Écoles reçues:', schools);
        
        const currentSchool = schools.find(s => s.id === schoolId);
        console.log('🏫 École trouvée:', currentSchool);
        setSchool(currentSchool);

        // 2. Récupérer les étudiants
        const studentsUrl = `http://localhost:8000/api/v1/sync/schools/${schoolId}/students`;
        console.log('📡 URL étudiants:', studentsUrl);
        
        const studentsRes = await fetch(studentsUrl, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });

        console.log('📊 Status réponse étudiants:', studentsRes.status);

        if (!studentsRes.ok) {
          if (studentsRes.status === 401) {
            throw new Error('Non authentifié. Reconnectez-vous.');
          } else if (studentsRes.status === 403) {
            throw new Error('Accès refusé. Token invalide.');
          }
          const errText = await studentsRes.text();
          throw new Error(`Erreur API: ${studentsRes.status} - ${errText}`);
        }
        
        const data = await studentsRes.json();
        console.log('✅ Étudiants reçus:', data);
        console.log('🔢 Nombre:', data.length);
        
        setStudents(data);
      } catch (err) {
        console.error('❌ Erreur complète:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [schoolId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="text-slate-400 text-xl">⏳ Chargement...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 p-8">
        <div className="bg-red-500/20 border border-red-500/50 text-red-400 px-6 py-4 rounded-xl max-w-md">
          <h3 className="font-bold text-lg mb-2">❌ Erreur</h3>
          <p className="mb-4">{error}</p>
          <button 
            onClick={() => navigate('/login')}
            className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
          >
            Se reconnecter
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 space-y-6">
      <button onClick={() => navigate('/institutions')} className="text-slate-400 hover:text-white flex items-center gap-2">
        ← Retour aux établissements
      </button>
      
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-white">{school?.name}</h1>
          <p className="text-slate-400">{school?.code} • {school?.region} • Sync: {school?.last_sync}</p>
        </div>
        <div className="bg-slate-800 px-6 py-3 rounded-xl border border-slate-700">
          <span className="text-2xl font-bold text-emerald-400">{students.length}</span> étudiants
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-700 bg-slate-800">
        {students.length === 0 ? (
          <div className="p-10 text-center text-slate-500">
            Aucun étudiant dans cette école
          </div>
        ) : (
          <table className="w-full text-left">
            <thead className="bg-slate-700 text-slate-300 text-sm">
              <tr>
                <th className="p-4">ID</th>
                <th className="p-4">Nom complet</th>
                <th className="p-4">Naissance</th>
                <th className="p-4">Inscription</th>
                <th className="p-4 text-center">Statut</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {students.map(s => (
                <tr key={s.id} className="hover:bg-slate-700/40">
                  <td className="p-4 font-mono text-sm text-slate-400">{s.id}</td>
                  <td className="p-4 text-white font-medium">{s.first_name} {s.last_name}</td>
                  <td className="p-4 text-slate-400">{s.birth_date || 'N/A'}</td>
                  <td className="p-4 text-slate-400">{s.enrollment_date || 'N/A'}</td>
                  <td className="p-4 text-center">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${s.is_synced ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                      ✅ bien reçu

                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}