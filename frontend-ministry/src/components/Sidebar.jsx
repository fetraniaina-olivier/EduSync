// src/components/Sidebar.jsx
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const menu = [
    { path: '/', label: 'Accueil', icon: '🏠' },
    { path: '/institutions', label: 'Établissements', icon: '🏫' },
    { path: '/students', label: 'Étudiants', icon: '👨‍' },
    { path: '/teachers', label: 'Enseignants', icon: '👨‍🏫' },
    { path: '/diplomas', label: 'Diplômes', icon: '🎓' },
  ];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 p-4 flex flex-col h-screen">
      {/* Logo */}
      <div 
        className="flex items-center gap-3 px-4 py-4 mb-8 cursor-pointer hover:opacity-80 transition-opacity"
        onClick={() => navigate('/')}
      >
        <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
          MIN
        </div>
        <div>
          <h1 className="text-white font-bold leading-tight">MESupReS</h1>
          <p className="text-xs text-gray-500">Ministère</p>
        </div>
      </div>

      {/* Menu Navigation */}
      <nav className="flex-1 space-y-2">
        {menu.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                isActive 
                  ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-500/20' 
                  : 'text-gray-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* User Profile & Logout */}
      <div className="mt-auto pt-4 border-t border-slate-800">
        <div className="flex items-center gap-3 px-4 py-3 mb-2">
          <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs text-white font-bold">
            AD
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">Admin</p>
            <p className="text-xs text-gray-500 truncate">admin@mesupres.gov</p>
          </div>
        </div>
        
        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-400 hover:bg-red-500/10 rounded-lg transition-colors text-left mt-2"
        >
          <span>🚪</span>
          <span className="font-medium">Se déconnecter</span>
        </button>
      </div>
    </div>
  );
}