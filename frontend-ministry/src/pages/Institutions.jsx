import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Institutions() {
  const [schools, setSchools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSchools = async () => {
      try {
        setLoading(true);
        
        // ✅ UTILISER LA BONNE CLÉ : 'ministry_token'
        const token = localStorage.getItem('ministry_token');
        
        console.log('🔑 Token récupéré:', token ? 'OUI ✅' : 'NON ❌');
        
        if (!token) {
          throw new Error('Token manquant. Veuillez vous reconnecter.');
        }

        const res = await fetch('http://localhost:8000/api/v1/sync/schools', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Accept': 'application/json'
          }
        });

        if (!res.ok) {
          const errData = await res.json().catch(() => ({}));
          throw new Error(errData.detail || `Erreur HTTP ${res.status}`);
        }

        const data = await res.json();
        console.log('✅ Données reçues:', data);
        setSchools(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error('❌ Erreur:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSchools();
  }, []);

  if (loading) return <div className="p-10 text-center text-slate-400">⏳ Chargement des établissements...</div>;
  if (error) return <div className="p-10 text-center text-red-400">⚠️ {error}</div>;
  if (schools.length === 0) return <div className="p-10 text-center text-slate-500">Aucune école enregistrée.</div>;

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-700 bg-slate-800">
      <table className="w-full text-left">
        <thead className="bg-slate-700 text-slate-300 text-sm uppercase tracking-wider">
          <tr>
            <th className="p-4 font-semibold">Code</th>
            <th className="p-4 font-semibold">Établissement</th>
            <th className="p-4 font-semibold">Région</th>
            <th className="p-4 font-semibold text-center">Étudiants</th>
            <th className="p-4 font-semibold">Dernière Sync</th>
            <th className="p-4 font-semibold text-center">Statut</th>
          </tr>
        </thead>
       <tbody className="divide-y divide-slate-700">
  {schools.map((s) => (
    <tr 
      key={s.id} 
      className="hover:bg-slate-700/40 transition-colors cursor-pointer"  // ← Ajouté
      onClick={() => navigate(`/institutions/${s.id}/students`)}           // ← Ajouté
    >
      <td className="p-4 font-mono text-sm text-emerald-400">{s.code}</td>
      <td className="p-4 font-medium text-white">{s.name}</td>
      <td className="p-4 text-slate-400">{s.region || 'N/A'}</td>
      <td className="p-4 text-center">
        <span className="bg-slate-700 text-white px-3 py-1 rounded-full text-sm font-bold">{s.students}</span>
      </td>
      <td className="p-4 text-slate-400 font-mono">{s.last_sync || 'Jamais'}</td>
      <td className="p-4 text-center">
        <span className={`px-2 py-1 rounded text-xs font-semibold ${s.status === 'actif' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
          {s.status}
        </span>
      </td>
    </tr>
  ))}
</tbody>
      </table>
    </div>
  );
}