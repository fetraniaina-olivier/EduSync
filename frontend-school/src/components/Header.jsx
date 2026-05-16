export default function Header() {
  return (
    <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-emerald-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">🏫</div>
        <div>
          <h1 className="text-lg font-bold text-white">EduSync École</h1>
          <p className="text-xs text-slate-400">Gestion & Synchronisation</p>
        </div>
      </div>
      <div className="text-sm text-slate-400 bg-slate-700 px-3 py-1 rounded-full">Portail Interne</div>
    </header>
  );
}