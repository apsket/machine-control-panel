export default function TemperatureDisplay({ temperature }) {
  return (
    <div className="p-4 rounded-2xl shadow bg-white">
      <h2 className="text-xl font-semibold mb-2">Ambient Temperature</h2>
      {temperature !== null ? (
        <p className="text-lg">{temperature.toFixed(1)} °C</p>
      ) : (
        <p className="text-gray-500">Loading...</p>
      )}
    </div>
  )
}