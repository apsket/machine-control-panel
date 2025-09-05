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
    fetchTemperature()
    const interval = setInterval(fetchTemperature, 90000)
    return () => clearInterval(interval)
  }, [])

  // Poll machine state
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
    fetchMachineState()
    const interval = setInterval(fetchMachineState, 500)
    return () => clearInterval(interval)
  }, [])

  const handleSetSpeed = (speed) => {
    fetch("http://127.0.0.1:8000/motor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ speed }),
    }).catch((err) => console.error(err))
  }

  const handleToggleValve = (open) => {
    fetch("http://127.0.0.1:8000/valve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ open }),
    }).catch((err) => console.error(err))
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl">
        <h1 className="text-4xl font-bold mb-12 text-gray-800 text-center">
          Machine Control Panel
        </h1>
        
        <div className="w-full h-px bg-gray-300 border-0 flex-shrink-0">
          <MotorControl motorSpeed={motorSpeed} onSetSpeed={handleSetSpeed} />
          
          <div className="w-full max-w-2xl my-8">
            <hr className="w-full h-px bg-gray-300 border-0" />
          </div>
          
          <ValveControl valveOpen={valveOpen} onToggleValve={handleToggleValve} />
          
          <div className="w-full max-w-2xl my-8">
            <hr className="w-full h-px bg-gray-300 border-0" />
          </div>
          
          <TemperatureDisplay temperature={temperature} />
        </div>
      </div>
    </div>
  )
}

export default App
