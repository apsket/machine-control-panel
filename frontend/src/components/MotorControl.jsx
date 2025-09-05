import { useState } from "react"

export default function MotorControl({ motorSpeed, onSetSpeed, changing }) {
  const [inputValue, setInputValue] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputValue !== "") {
      onSetSpeed(Number(inputValue))
      setInputValue("") // clear input after submitting
    }
  }

  return (
    <div className="p-6 rounded-2xl shadow-lg bg-white hover:shadow-xl transition-shadow">
      <h2 className="text-xl font-semibold mb-2">Motor Control</h2>
      <p className="mb-2">
        Current Speed: <span className="font-bold">{motorSpeed}</span>{" "}
        {changing && <span className="text-blue-500">(Changing...)</span>}
      </p>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="number"
          className="border border-gray-300 rounded px-2 py-1 w-24 focus:outline-none focus:ring-2 focus:ring-blue-400"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Enter new speed"
          disabled={changing}
        />
        <button
          type="submit"
          className="px-3 py-1 rounded bg-blue-500 text-white hover:bg-blue-600 transition"
          disabled={changing}
        >
          Set
        </button>
      </form>
    </div>
  )
}