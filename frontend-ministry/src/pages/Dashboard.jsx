import StatsCard from '../components/StatsCard';
import InstitutionTable from '../components/InstitutionTable';

// Données mockées (à remplacer par appels API)
const stats = {
  institutions: 28,
  students: 48750,
  teachers: 3420,
  diplomas: 8420,
};

const institutions = [
  {
    id: 1,
    code: 'ENI-FNR',
    name: 'ENI Fianarantsoa',
    type: 'École Nationale d\'Ingénieurs',
    region: 'Haute Matsiatra',
    students: 1842,
    status: 'actif',
    lastSync: 'il y a 3 min',
  },
  {
    id: 2,
    code: 'ESP-ANT',
    name: 'ESPA Antananarivo',
    type: 'École Supérieure',
    region: 'Analamanga',
    students: 4250,
    status: 'actif',
    lastSync: 'il y a 12 min',
  },
  {
    id: 3,
    code: 'ENI-ANT',
    name: 'ENI Antananarivo',
    type: 'École Nationale d\'Ingénieurs',
    region: 'Analamanga',
    students: 2100,
    status: 'actif',
    lastSync: 'il y a 1h',
  },
  {
    id: 4,
    code: 'EST-TLM',
    name: 'EST Toamasina',
    type: 'École Supérieure de Technologie',
    region: 'Atsinanana',
    students: 1560,
    status: 'attente',
    lastSync: 'il y a 3j',
  },
];

export default function Dashboard() {
  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Vue consolidée nationale</h1>
        <p className="text-gray-400 mt-1">Données agrégées de l'ensemble des établissements connectés.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Établissements"
          value={stats.institutions}
          icon="🏫"
          trend={2.5}
        />
        <StatsCard
          title="Étudiants"
          value={stats.students.toLocaleString()}
          icon="👨‍🎓"
          trend={1.2}
        />
        <StatsCard
          title="Enseignants"
          value={stats.teachers.toLocaleString()}
          icon="👨‍🏫"
          trend={-0.3}
        />
        <StatsCard
          title="Diplômes Validés"
          value={stats.diplomas.toLocaleString()}
          icon="🎓"
        />
      </div>

      {/* Institutions Table */}
      <InstitutionTable institutions={institutions} />
    </div>
  );
}