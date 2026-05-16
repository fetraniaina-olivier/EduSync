import { useState } from 'react';
import StudentForm from '../components/StudentForm';
import StudentTable from '../components/StudentTable';
import { api } from '../services/api';

export default function Students() {
  const [view, setView] = useState('list'); // 'list' ou 'add'
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchStudents = async () => {
    try {
      const data = await api.getStudents();
      setStudents(data);
    } finally {
      setLoading(false);
    }
  };

  useState(() => { fetchStudents(); }, []);

  const handleAdd = async (data) => {
    await api.addStudent(data);
    fetchStudents();
    setView('list');
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white">Étudiants</h2>
          <p className="text-slate-400">Gestion des inscriptions et synchronisation.</p>
        </div>
        {view === 'list' && (
          <button 
            onClick={() => setView('add')}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg font-medium transition"
          >
            ➕ Ajouter un étudiant
          </button>
        )}
      </div>

      {view === 'add' ? (
        <StudentForm onAdd={handleAdd} onCancel={() => setView('list')} />
      ) : (
        <StudentTable students={students} onRefresh={fetchStudents} />
      )}
    </div>
  );
}