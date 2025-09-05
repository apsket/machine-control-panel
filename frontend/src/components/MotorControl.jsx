import { useState } from "react"

function MotorControl({ motorSpeed, onSetSpeed }) {
  const [inputSpeed, setInputSpeed] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (inputSpeed !== "") {
      onSetSpeed(Number(inputSpeed))
      setInputSpeed("")
    }
  }

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 w-80 flex flex-col items-center text-center">
      <h2 className="text-xl font-semibold text-gray-700 -mb-0">Motor Control</h2>
      <p className="text-gray-600 mb-2">
        Current Speed: <span className="font-bold text-gray-900">{motorSpeed}</span>
      </p>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center space-y-3 w-full"
      >
        <input
          type="number"
          value={inputSpeed}
          onChange={(e) => setInputSpeed(e.target.value)}
          placeholder="Enter new speed"
          className="border border-gray-300 rounded-lg px-4 py-2 text-center w-40 focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white font-medium px-5 py-2 rounded-lg transition"
        >
          Set Speed
        </button>
      </form>
    </div>
  )
}

export default MotorControl