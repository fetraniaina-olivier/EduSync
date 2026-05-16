import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function Dashboard() {
  const [stats, setStats] = useState({
    students: 0,
    teachers: 0,
    programs: 0,
    diplomas: 0
  });
  const [syncs, setSyncs] = useState([]);

  useEffect(() => {
    // Charger les stats
    api.getStudents().then(data => {
      setStats(prev => ({ ...prev, students: data.length }));
    });
    
    // Simuler des syncs récentes
    setSyncs([
      { entity: 'Étudiants', count: 142, time: 'Il y a 2 heures' },
      { entity: 'Notes', count: 568, time: 'Il y a 5 heures' },
      { entity: 'Programmes', count: 12, time: 'Hier' },
    ]);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Tableau de bord ENI</h2>
        <p className="text-slate-400">Vue d'ensemble de l'établissement et de ses synchronisations.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard title="ÉTUDIANTS" value={stats.students} icon="👥" trend="+42 ce mois" />
        <StatCard title="ENSEIGNANTS" value={stats.teachers || 87} icon="👨‍" />
        <StatCard title="PROGRAMMES" value={stats.programs || 64} icon="📚" />
        <StatCard title="DIPLÔMES ÉMIS" value={stats.diplomas || 312} icon="🎓" trend="+24 cette session" />
      </div>

      {/* Sync Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Dernières synchronisations</h3>
          <div className="space-y-3">
            {syncs.map((sync, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full"></div>
                  <div>
                    <p className="text-white font-medium">{sync.entity}</p>
                    <p className="text-slate-400 text-sm">ENI → Ministère • {sync.count} enregistrements</p>
                  </div>
                </div>
                <span className="text-slate-400 text-sm">{sync.time}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
          <h3 className="text-lg font-semibold text-white mb-4">État de connexion</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse"></div>
                <span className="text-emerald-400 font-medium">Connecté au Ministère</span>
              </div>
              <span className="text-emerald-400 text-sm">OK</span>
            </div>
            <button 
              onClick={() => window.location.href = '/sync'}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium transition"
            >
              Synchroniser maintenant
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon, trend }) {
  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-slate-400 text-sm mb-1">{title}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
      {trend && <p className="text-emerald-400 text-sm">{trend}</p>}
    </div>
  );
}