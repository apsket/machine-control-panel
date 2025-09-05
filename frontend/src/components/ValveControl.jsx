function ValveControl({ valveOpen, onToggleValve }) {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 w-80 flex flex-col items-center text-center">
      <h2 className="text-xl font-semibold text-gray-700 mb-3">Valve Control</h2>
      <p className="text-gray-600 mb-4">
        Valve is currently:{" "}
        <span className={`font-bold ${valveOpen ? "text-green-600" : "text-red-600"}`}>
          {valveOpen ? "Open" : "Closed"}
        </span>
      </p>
      <button
        onClick={() => onToggleValve(!valveOpen)}
        className={`px-5 py-2 rounded-lg font-medium shadow transition ${
          valveOpen ? "bg-red-500 hover:bg-red-600 text-white" : "bg-green-500 hover:bg-green-600 text-white"
        }`}
      >
        {valveOpen ? "Close Valve" : "Open Valve"}
      </button>
    </div>
  )
}

export default ValveControl