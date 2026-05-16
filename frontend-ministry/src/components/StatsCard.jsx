export default function StatsCard({ title, value, subtitle, icon, trend }) {
  return (
    <div className="bg-card rounded-xl p-6 border border-border">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm text-gray-400 uppercase tracking-wide">{title}</p>
          <h3 className="text-3xl font-bold text-white mt-2">{value}</h3>
          {subtitle && <p className="text-sm text-gray-400 mt-1">{subtitle}</p>}
          {trend !== undefined && (
            <p className={`text-sm mt-2 flex items-center gap-1 ${
              trend >= 0 ? 'text-success' : 'text-red-400'
            }`}>
              {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}% ce mois
            </p>
          )}
        </div>
        <div className="text-4xl opacity-80">{icon}</div>
      </div>
    </div>
  );
}