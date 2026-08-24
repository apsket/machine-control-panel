import { useState } from "react"
import TelemetryChart from "./TelemetryChart"

export default function MotorControl({ motorSpeed, onSetSpeed, targetSpeed, min = 0, max = 100 }) {
  const [inputValue, setInputValue] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue !== "") {
      const parsed = Number(inputValue)
      if (!Number.isInteger(parsed)) {
        // rely on browser validation too; avoid sending non-integers
        return
      }
      const intVal = Math.max(min, Math.min(max, Math.round(parsed)))
      onSetSpeed(intVal)
      setInputValue("") // clear input after submitting
    }
  }

  return (
    <div className="p-6 rounded-2xl shadow-lg bg-white hover:shadow-xl transition-shadow w-full">
      <h2 className="text-xl font-semibold mb-1">Motor Control</h2>
      <p className="mb-1">
        Current Speed: <span className="font-bold">{motorSpeed}</span>{" "}
        {targetSpeed !== null && motorSpeed !== targetSpeed && (
          <span className="text-blue-500">(Changing to {targetSpeed}...)</span>
        )}
      </p>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="number"
          className="border border-gray-300 rounded px-2 py-1 w-24 focus:outline-none focus:ring-2 focus:ring-blue-400"
          style={{ width: '6rem' }}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onInput={(e) => e.currentTarget.setCustomValidity("")}
          onInvalid={(e) => e.currentTarget.setCustomValidity(`Please enter an integer between ${min} and ${max}`)}
          placeholder="Enter new speed"
          step={1}
          min={min}
          max={max}
        />
        <button
          type="submit"
          className="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600 transition"
        >
          Set
        </button>
      </form>
      <TelemetryChart metrics={["motor_actual","motor_target"]} title={["Motor Actual","Motor Target"]} chartHeight={260} />
    </div>
  )
}