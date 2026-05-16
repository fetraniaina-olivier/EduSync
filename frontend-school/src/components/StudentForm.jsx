import { useState } from 'react';

export default function StudentForm({ onAdd }) {
  const [form, setForm] = useState({
    id: '', first_name: '', last_name: '', birth_date: '', enrollment_date: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onAdd(form);
      setForm({ id: '', first_name: '', last_name: '', birth_date: '', enrollment_date: '' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-slate-800 p-5 rounded-xl border border-slate-700 space-y-4">
      <h2 className="text-lg font-semibold text-white mb-2">➕ Ajouter un étudiant</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input placeholder="ID unique (ex: stu-001)" required className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-emerald-500 outline-none" value={form.id} onChange={e => setForm({...form, id: e.target.value})} />
        <input placeholder="Prénom" required className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-emerald-500 outline-none" value={form.first_name} onChange={e => setForm({...form, first_name: e.target.value})} />
        <input placeholder="Nom" required className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-emerald-500 outline-none" value={form.last_name} onChange={e => setForm({...form, last_name: e.target.value})} />
        <input type="date" required className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-emerald-500 outline-none" value={form.birth_date} onChange={e => setForm({...form, birth_date: e.target.value})} />
        <input type="date" required className="bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-emerald-500 outline-none" value={form.enrollment_date} onChange={e => setForm({...form, enrollment_date: e.target.value})} />
      </div>
      <button type="submit" disabled={loading} className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-2 rounded-lg transition disabled:opacity-50">
        {loading ? 'Enregistrement...' : 'Enregistrer l\'étudiant'}
      </button>
    </form>
  );
}