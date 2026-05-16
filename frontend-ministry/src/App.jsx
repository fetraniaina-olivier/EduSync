// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import SchoolStudents from './pages/SchoolStudents';
import { AuthProvider, useAuth } from './context/AuthContext';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Home from './pages/Home';
import Institutions from './pages/Institutions';

// ─────────────────────────────────────────────
// 🔐 Composant de protection des routes
// ─────────────────────────────────────────────
function ProtectedRoute({ children }) {
  const { token } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

// ─────────────────────────────────────────────
// 📐 Layout partagé (Sidebar + Contenu)
// ─────────────────────────────────────────────
function DashboardLayout() {
  return (
    <div className="flex bg-slate-900 min-h-screen font-sans">
      <Sidebar /> {/* ✅ Sidebar maintenant DANS le contexte AuthProvider */}
      <main className="flex-1 overflow-y-auto h-screen">
        <Outlet /> {/* Affiche la page active (Home, Institutions, etc.) */}
      </main>
    </div>
  );
}

// ─────────────────────────────────────────────
// 🎯 Application principale
// ─────────────────────────────────────────────
function App() {
  return (
    <BrowserRouter>
      {/* ✅ AuthProvider enveloppe TOUTES les routes */}
      <AuthProvider>
        <Routes>
          {/* Route publique */}
          <Route path="/login" element={<Login />} />

          {/* Routes protégées avec Layout partagé */}
          <Route element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }>
            <Route path="/" element={<Home />} />
            <Route path="/institutions" element={<Institutions />} />
            <Route path="/students" element={<div className="p-8 text-white">🚧 Module Étudiants</div>} />
            <Route path="/teachers" element={<div className="p-8 text-white">🚧 Module Enseignants</div>} />
            <Route path="/diplomas" element={<div className="p-8 text-white">🚧 Module Diplômes</div>} />
          </Route>

          <Route path="/institutions" element={<Institutions />} />
          <Route path="/institutions/:schoolId/students" element={<SchoolStudents />} /> {/* ← Ajoutez cette ligne */}

          {/* Redirection par défaut */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;