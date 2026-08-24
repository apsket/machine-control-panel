import { useEffect, useState } from "react"
import MotorControl from "./components/MotorControl"
import ValveControl from "./components/ValveControl"
import TemperatureDisplay from "./components/TemperatureDisplay"

function App() {
  const [motorSpeed, setMotorSpeed] = useState(0)
  const [motorMin, setMotorMin] = useState(0)
  const [motorMax, setMotorMax] = useState(100)
  const [valveOpen, setValveOpen] = useState(false)
  const [temperature, setTemperature] = useState(null)
  const [temperatureTs, setTemperatureTs] = useState(null)
  const [tempFetchCount, setTempFetchCount] = useState(0)

  // Flags and targets
  const [motorChanging, setMotorChanging] = useState(false)
  const [motorTarget, setMotorTarget] = useState(null)

  const [valveChanging, setValveChanging] = useState(false)
  const [valveTarget, setValveTarget] = useState(null)

  // ------------------------
  // Polling loops
  // ------------------------
  useEffect(() => {
    const fetchTemperature = () => {
      // Add a cache-busting query param and request no-store to avoid browser cache
      const url = `http://127.0.0.1:8000/temperature?_=${Date.now()}`
      console.debug('Fetching temperature from', url)
      fetch(url, { cache: 'no-store' })
        .then((res) => {
          console.debug('Temperature response status:', res.status)
          return res.json()
        })
        .then((data) => {
          // data: { temperature: number|null, timestamp: ISO string|null }
          console.debug('Temperature payload:', data)
          const raw = data.temperature
          const rounded = raw !== null && raw !== undefined ? Number(Number(raw).toFixed(1)) : null
          setTemperature(rounded)
          setTemperatureTs(data.timestamp)
          // increment a counter to force a render even if numeric value didn't change
          setTempFetchCount((c) => c + 1)
        })
        .catch((err) => {
          console.error('Error fetching temperature:', err)
        })
    }

    fetchTemperature()
    const interval = setInterval(fetchTemperature, 30000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const fetchMachineState = () => {
      fetch("http://127.0.0.1:8000/motor")
        .then((res) => res.json())
        .then((data) => {
          // data: { speed, target?, min?, max? }
          setMotorSpeed(data.speed)
          if (typeof data.min === 'number') setMotorMin(data.min)
          if (typeof data.max === 'number') setMotorMax(data.max)
        })
        .catch(console.error)

      fetch("http://127.0.0.1:8000/valve")
        .then((res) => res.json())
        .then((data) => setValveOpen(data.open))
        .catch(console.error)
    }

    fetchMachineState()
    const interval = setInterval(fetchMachineState, 200)
    return () => clearInterval(interval)
  }, [])

  // ------------------------
  // Handlers
  // ------------------------
  const handleSetSpeed = async (speed) => {
    setMotorTarget(speed)
    setMotorChanging(true)
    try {
      await fetch("http://127.0.0.1:8000/motor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ speed }),
      })
    } catch (err) {
      console.error(err)
    }
  }

  const handleToggleValve = async (open) => {
    setValveTarget(open)
    setValveChanging(true)
    try {
      await fetch("http://127.0.0.1:8000/valve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ open }),
      })
    } catch (err) {
      console.error(err)
    }
  }

  // ------------------------
  // Sync motorChanging and valveChanging with actual state
  // ------------------------
  useEffect(() => {
    if (motorTarget !== null && motorSpeed === motorTarget) {
      setMotorChanging(false)
      setMotorTarget(null)
    }
  }, [motorSpeed, motorTarget])

  useEffect(() => {
    if (valveTarget !== null && valveOpen === valveTarget) {
      setValveChanging(false)
      setValveTarget(null)
    }
  }, [valveOpen, valveTarget])

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
          targetSpeed={motorTarget}
          min={motorMin}
          max={motorMax}
        />
        <ValveControl
          valveOpen={valveOpen}
          onToggleValve={handleToggleValve}
          changing={valveChanging}
          target={valveTarget}
        />
        <TemperatureDisplay temperature={temperature} timestamp={temperatureTs} />
      </div>
    </div>
  )
}

export default App