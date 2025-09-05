export default function TemperatureDisplay({ temperature }) {
  return (
    <div className="p-6 rounded-2xl shadow-lg bg-white hover:shadow-xl transition-shadow">
      <h2 className="text-xl font-semibold mb-2">Ambient Temperature</h2>
      {temperature !== null ? (
        <p className={`text-lg ${temperature > 30 ? "text-red-500" : "text-blue-500"}`}>
          🌡️ {temperature.toFixed(1)} °C
        </p>
      ) : (
        <p className="text-gray-500">Loading...</p>
      )}
    </div>
  )
}