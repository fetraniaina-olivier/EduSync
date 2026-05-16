import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  const menuItems = [
    { path: '/', label: 'Tableau de bord', icon: '📊' },
    { path: '/students', label: 'Étudiants', icon: '👥' },
    { path: '/teachers', label: 'Enseignants', icon: '👨‍🏫' },
    { path: '/programs', label: 'Programmes', icon: '📚' },
    { path: '/diplomas', label: 'Diplômes', icon: '🎓' },
    { path: '/sync', label: 'Synchronisation', icon: '🔄' },
  ];

  return (
    <aside className="w-64 bg-slate-800 border-r border-slate-700 min-h-screen flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">🏫</div>
          <div>
            <h1 className="text-white font-bold text-sm">ENI</h1>
            <p className="text-slate-400 text-xs">École Nationale d'Informatique</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                isActive
                  ? 'bg-emerald-600 text-white'
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
              }`
            }
          >
            <span className="text-xl">{item.icon}</span>
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* User Info */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center gap-3 px-4 py-3">
          <div className="w-8 h-8 rounded-full bg-emerald-600 flex items-center justify-center text-white text-sm font-bold">
            AD
          </div>
          <div>
            <p className="text-white text-sm font-medium">Administrateur</p>
            <p className="text-slate-400 text-xs">admin@eni.mg</p>
          </div>
        </div>
      </div>
    </aside>
  );
}