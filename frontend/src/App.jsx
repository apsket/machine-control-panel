import { useEffect, useState } from "react"
import MotorControl from "./components/MotorControl"
import ValveControl from "./components/ValveControl"
import TemperatureDisplay from "./components/TemperatureDisplay"

function App() {
  const [motorSpeed, setMotorSpeed] = useState(0)
  const [valveOpen, setValveOpen] = useState(false)
  const [temperature, setTemperature] = useState(null)

  // Fetch temperature every 90 seconds
  useEffect(() => {
    const fetchTemperature = () => {
      fetch("http://127.0.0.1:8000/temperature")
        .then((res) => res.json())
        .then((data) => setTemperature(data.temperature))
        .catch((err) => console.error(err))
    }

    fetchTemperature()                     // initial fetch
    const interval = setInterval(fetchTemperature, 120000) // every 120s
    return () => clearInterval(interval)   // cleanup on unmount
  }, [])

  // Poll motor speed and valve state every 200ms (or whatever SCAN_INTERVAL you chose)
  useEffect(() => {
    const fetchMachineState = () => {
      fetch("http://127.0.0.1:8000/motor")
        .then((res) => res.json())
        .then((data) => setMotorSpeed(data.speed))
        .catch(console.error)

      fetch("http://127.0.0.1:8000/valve")
        .then((res) => res.json())
        .then((data) => setValveOpen(data.open))
        .catch(console.error)
    }

    fetchMachineState() // initial fetch
    const interval = setInterval(fetchMachineState, 200)
    return () => clearInterval(interval)
  }, [])

  // Motor control handler
  const handleSetSpeed = (speed) => {
    fetch("http://127.0.0.1:8000/motor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ speed }),
    }).catch((err) => console.error(err))
  }

  // Valve control handler
  const handleToggleValve = (open) => {
    fetch("http://127.0.0.1:8000/valve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ open }),
    }).catch((err) => console.error(err))
  }

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6">Machine Control Panel</h1>
      <div className="grid gap-6 md:grid-cols-3">
        <MotorControl motorSpeed={motorSpeed} onSetSpeed={handleSetSpeed} />
        <ValveControl valveOpen={valveOpen} onToggleValve={handleToggleValve} />
        <TemperatureDisplay temperature={temperature} />
      </div>
    </div>
  )
}

export default App