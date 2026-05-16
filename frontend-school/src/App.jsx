// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Students from './pages/Students';
import Teachers from './pages/Teachers';
import Programs from './pages/Programs';
import Diplomas from './pages/Diplomas';
import Sync from './pages/Sync';

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-900">
        <Sidebar />
        <main className="flex-1 p-8 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/students" element={<Students />} />
            <Route path="/teachers" element={<Teachers />} />
            <Route path="/programs" element={<Programs />} />
            <Route path="/diplomas" element={<Diplomas />} />
            <Route path="/sync" element={<Sync />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;