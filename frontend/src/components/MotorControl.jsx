import { useState } from "react"

export default function MotorControl({ motorSpeed, onSetSpeed }) {
  const [inputValue, setInputValue] = useState(motorSpeed)

  const handleSubmit = (e) => {
    e.preventDefault()
    onSetSpeed(Number(inputValue))
  }

  return (
    <div className="p-4 rounded-2xl shadow bg-white">
      <h2 className="text-xl font-semibold mb-2">Motor Control</h2>
      <p className="mb-2">
        Current Speed: <span className="font-bold">{motorSpeed}</span>
      </p>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="number"
          className="border rounded px-2 py-1 w-24"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />
        <button
          type="submit"
          className="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600"
        >
          Set
        </button>
      </form>
    </div>
  )
}