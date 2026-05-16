export default function StudentTable({ students }) {
  if (!students.length) return <div className="text-center py-8 text-slate-500">Aucun étudiant enregistré.</div>;

  return (
    <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
      <table className="w-full text-left">
        <thead className="bg-slate-700/50 text-slate-300 text-sm">
          <tr>
            <th className="px-4 py-3">ID</th>
            <th className="px-4 py-3">Nom complet</th>
            <th className="px-4 py-3">Naissance</th>
            <th className="px-4 py-3">Inscription</th>
            <th className="px-4 py-3 text-center">Sync</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-700">
          {students.map(s => (
            <tr key={s.id} className="hover:bg-slate-700/30 transition">
              <td className="px-4 py-3 font-mono text-xs text-slate-400">{s.id}</td>
              <td className="px-4 py-3 font-medium text-white">{s.first_name} {s.last_name}</td>
              <td className="px-4 py-3 text-sm text-slate-400">{s.birth_date}</td>
              <td className="px-4 py-3 text-sm text-slate-400">{s.enrollment_date}</td>
              <td className="px-4 py-3 text-center">
                <span className={`inline-block px-2 py-1 rounded text-xs font-bold ${s.is_synced ? 'bg-emerald-500/20 text-emerald-400' : 'bg-amber-500/20 text-amber-400'}`}>
                  {s.is_synced ? '✅ Sync' : '⏳ En attente'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}