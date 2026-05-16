export default function InstitutionTable({ institutions }) {
  return (
    <div className="bg-card rounded-xl border border-border overflow-hidden">
      {/* Header */}
      <div className="p-6 border-b border-border flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-white">Établissements connectés</h3>
          <p className="text-sm text-gray-400">État des liaisons de synchronisation</p>
        </div>
        <button className="px-4 py-2 bg-primary hover:bg-indigo-600 text-white text-sm rounded-lg transition">
          + Ajouter
        </button>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-900">
            <tr>
              <th className="text-left px-6 py-4 text-sm text-gray-400 font-medium">CODE</th>
              <th className="text-left px-6 py-4 text-sm text-gray-400 font-medium">ÉTABLISSEMENT</th>
              <th className="text-left px-6 py-4 text-sm text-gray-400 font-medium">RÉGION</th>
              <th className="text-left px-6 py-4 text-sm text-gray-400 font-medium">ÉTUDIANTS</th>
              <th className="text-left px-6 py-4 text-sm text-gray-400 font-medium">STATUT</th>
              <th className="text-left px-6 py-4 text-sm text-gray-400 font-medium">DERNIÈRE SYNC</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {institutions.map((inst) => (
              <tr key={inst.id} className="hover:bg-slate-750 transition">
                <td className="px-6 py-4 text-sm text-gray-300 font-mono">{inst.code}</td>
                <td className="px-6 py-4">
                  <div>
                    <p className="text-sm font-medium text-white">{inst.name}</p>
                    <p className="text-xs text-gray-500">{inst.type}</p>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-gray-300">{inst.region}</td>
                <td className="px-6 py-4 text-sm text-gray-300">{inst.students?.toLocaleString()}</td>
                <td className="px-6 py-4">
                  <span className={`px-3 py-1 text-xs rounded-full font-medium ${
                    inst.status === 'actif' 
                      ? 'bg-success/20 text-success' 
                      : 'bg-warning/20 text-warning'
                  }`}>
                    {inst.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-400">{inst.lastSync}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}