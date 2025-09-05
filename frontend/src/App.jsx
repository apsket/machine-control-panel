import { useEffect, useState } from "react"
import MotorControl from "./components/MotorControl"
import ValveControl from "./components/ValveControl"
import TemperatureDisplay from "./components/TemperatureDisplay"

function App() {
  const [motorSpeed, setMotorSpeed] = useState(0)
  const [valveOpen, setValveOpen] = useState(false)
  const [temperature, setTemperature] = useState(null)

  // Flags to show "in-progress" actions
  const [motorChanging, setMotorChanging] = useState(false)
  const [valveChanging, setValveChanging] = useState(false)

  // ------------------------
  // Polling loop
  // ------------------------
  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://127.0.0.1:8000/motor")
        .then((res) => res.json())
        .then((data) => setMotorSpeed(data.speed))
        .catch(console.error)

      fetch("http://127.0.0.1:8000/valve")
        .then((res) => res.json())
        .then((data) => setValveOpen(data.open))
        .catch(console.error)

      fetch("http://127.0.0.1:8000/temperature")
        .then((res) => res.json())
        .then((data) => setTemperature(data.temperature))
        .catch(console.error)
    }, 500) // poll every 0.5s
    return () => clearInterval(interval)
  }, [])

  // ------------------------
  // Handlers
  // ------------------------
  const handleSetSpeed = async (speed) => {
    setMotorChanging(true)
    try {
      await fetch("http://127.0.0.1:8000/motor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ speed }),
      })
    } catch (err) {
      console.error(err)
    } finally {
      setMotorChanging(false)
    }
  }

  const handleToggleValve = async (open) => {
    setValveChanging(true)
    try {
      await fetch("http://127.0.0.1:8000/valve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ open }),
      })
    } catch (err) {
      console.error(err)
    } finally {
      setValveChanging(false)
    }
  }

  // ------------------------
  // Render
  // ------------------------
  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <h1 className="text-3xl font-bold mb-6">Machine Control Panel</h1>
      <div className="grid gap-6 md:grid-cols-3">
        <MotorControl
          motorSpeed={motorSpeed}
          onSetSpeed={handleSetSpeed}
          changing={motorChanging}
        />
        <ValveControl
          valveOpen={valveOpen}
          onToggleValve={handleToggleValve}
          changing={valveChanging}
        />
        <TemperatureDisplay temperature={temperature} />
      </div>
    </div>
  )
}

export default App