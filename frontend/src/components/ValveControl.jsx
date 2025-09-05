export default function ValveControl({ valveOpen, onToggleValve, changing }) {
  return (
    <div className="p-6 rounded-2xl shadow-lg bg-white hover:shadow-xl transition-shadow">
      <h2 className="text-xl font-semibold mb-2">Valve Control</h2>
      <p className="mb-2">
        Valve is: <span className="font-bold">{valveOpen ? "Open" : "Closed"}</span>{" "}
        {changing && <span className="text-blue-500">({valveOpen ? "Opening..." : "Closing..."})</span>}
      </p>
      <button
        onClick={() => onToggleValve(!valveOpen)}
        className={`px-3 py-1 rounded text-white ${
          valveOpen ? "bg-red-500 hover:bg-red-600" : "bg-green-500 hover:bg-green-600"
        } transition`}
        disabled={changing}
      >
        {valveOpen ? "Close Valve" : "Open Valve"}
      </button>
    </div>
  )
}