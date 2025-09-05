function TemperatureDisplay({ temperature }) {
  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 w-80 flex flex-col items-center text-center">
      <h2 className="text-xl font-semibold text-gray-700 mb-3">
        Ambient Temperature
      </h2>
      <p className="text-3xl font-bold text-blue-600">
        🌡️ {temperature !== null ? `${temperature}°C` : "Loading..."}
      </p>
    </div>
  )
}

export default TemperatureDisplay