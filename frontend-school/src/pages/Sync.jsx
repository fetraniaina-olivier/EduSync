import { useState } from 'react';
import { api } from '../services/api';

export default function Sync() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSync = async () => {
    setLoading(true);
    setStatus('⏳ Synchronisation en cours...');
    try {
      const res = await api.triggerSync();
      setStatus(`✅ Succès ! ${res.accepted} élément(s) synchronisé(s)`);
    } catch (err) {
      setStatus('❌ Échec de la synchronisation');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-white">Synchronisation</h2>
        <p className="text-slate-400">Envoyez les données vers le Ministère.</p>
      </div>

      <div className="bg-slate-800 rounded-xl border border-slate-700 p-8">
        <button
          onClick={handleSync}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white py-4 rounded-lg font-bold text-lg transition flex items-center justify-center gap-3"
        >
          🔄 {loading ? 'Synchronisation...' : 'Synchroniser maintenant'}
        </button>

        {status && (
          <div className={`mt-6 p-4 rounded-lg text-center font-medium ${
            status.includes('Succès') ? 'bg-emerald-500/20 text-emerald-300' :
            status.includes('Échec') ? 'bg-red-500/20 text-red-300' :
            'bg-amber-500/20 text-amber-300'
          }`}>
            {status}
          </div>
        )}
      </div>
    </div>
  );
}