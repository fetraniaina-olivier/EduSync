// src/pages/Home.jsx
import { useNavigate } from 'react-router-dom';

export default function Home() {
  const navigate = useNavigate();

  // Données simulées pour le design
  const stats = [
    { label: 'Établissements', value: '28', icon: '🏫', trend: '+2 ce mois' },
    { label: 'Étudiants', value: '48.7k', icon: '👨🎓', trend: '+1.2%' },
    { label: 'Enseignants', value: '3.4k', icon: '‍🏫', trend: 'Stable' },
    { label: 'Diplômes', value: '8.4k', icon: '🎓', trend: '+5.3%' },
  ];

  const features = [
    { title: 'Établissements', desc: 'Gérer les écoles et synchronisation', icon: '🏫', route: '/institutions' },
    { title: 'Étudiants', desc: 'Base nationale des étudiants', icon: '👨‍🎓', route: '/students' },
    { title: 'Enseignants', desc: 'Gestion du corps enseignant', icon: '👨‍🏫', route: '/teachers' },
    { title: 'Diplômes', desc: 'Validation et délivrance', icon: '🎓', route: '/diplomas' },
  ];

  return (
    <div className="p-8 space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Bonjour, Admin 👋</h1>
        <p className="text-gray-400 mt-1">Voici l'état global du système de synchronisation.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-slate-800/50 backdrop-blur border border-slate-700 p-6 rounded-2xl hover:border-indigo-500/50 transition-all cursor-default">
            <div className="flex justify-between items-start mb-4">
              <span className="text-3xl">{stat.icon}</span>
              <span className="text-xs font-medium text-green-400 bg-green-400/10 px-2 py-1 rounded-full">{stat.trend}</span>
            </div>
            <h3 className="text-3xl font-bold text-white">{stat.value}</h3>
            <p className="text-sm text-gray-400 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Navigation Rapide (Cards) */}
      <div>
        <h2 className="text-xl font-bold text-white mb-4">Accès Rapide</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((item, idx) => (
            <button
              key={idx}
              onClick={() => navigate(item.route)}
              className="group flex items-center gap-4 p-6 bg-slate-800/50 backdrop-blur border border-slate-700 rounded-2xl hover:bg-slate-800 hover:border-indigo-500 hover:scale-[1.02] transition-all text-left"
            >
              <div className="text-4xl p-3 bg-slate-700 rounded-xl group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                {item.icon}
              </div>
              <div>
                <h3 className="text-lg font-bold text-white group-hover:text-indigo-400 transition-colors">{item.title}</h3>
                <p className="text-sm text-gray-400">{item.desc}</p>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}