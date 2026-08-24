import { useEffect, useState } from "react"
import { Line } from "react-chartjs-2"
import client from "../api/client"
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

function fmtTime(ts) {
  const d = new Date(ts)
  return d.toLocaleTimeString()
}

export default function TelemetryChart({ metrics = ["temperature"], title, windowMs: propWindowMs, limit = 10000, chartHeight = 320 }) {
  const [data, setData] = useState(null)
  const [windowMs, setWindowMs] = useState(propWindowMs || null)

  useEffect(() => {
    let mounted = true
    async function load() {
      // If we don't yet have a window from props or config, fetch /config once
      if (!windowMs) {
        try {
          const cfg = await client.get('/config')
          if (!mounted) return
          setWindowMs(cfg.data.telemetry_window_ms)
        } catch (e) {
          // fallback to prop or default 5 minutes
          setWindowMs(propWindowMs || 5 * 60 * 1000)
        }
        // continue; next invocation will fetch history with windowMs set
      }
      if (!windowMs) return
      const end = Date.now()
      const start = end - windowMs
      try {
        const resp = await client.get('/history', { params: { start, end, limit } })
        if (!mounted) return
        const rows = resp.data || []
        const labels = rows.map(r => fmtTime(r.ts))
        const datasets = metrics.map((m, idx) => {
          const values = rows.map(r => {
            if (m === 'motor_actual') return r.motor_actual
            if (m === 'motor_target') return r.motor_target
            if (m === 'valve_open') return r.valve_open ? 1 : 0
            if (m === 'temperature') return r.temperature
            return null
          })
          const color = idx === 0 ? 'rgba(59,130,246,1)' : 'rgba(16,185,129,1)'
          const isValve = m === 'valve_open'
          return {
            label: (Array.isArray(title) ? title[idx] : (title || m)),
            data: values,
            borderColor: color,
            backgroundColor: color.replace('1)', '0.0)'),
            tension: isValve ? 0 : 0.05,
            stepped: isValve,
            borderWidth: 1.5,
            pointRadius: isValve ? 2 : 0,
            pointHoverRadius: 6,
            fill: false,
          }
        })
        setData({ labels, datasets })
      } catch (e) {
        // ignore for now
      }
    }
    load()
    // Refresh charts frequently for UI responsiveness (5s). Do not tie
    // refresh cadence directly to the window length which previously caused
    // very long and seemingly random update intervals for large windows.
    const iv = setInterval(load, 5000)
    return () => { mounted = false; clearInterval(iv) }
  }, [metrics, windowMs, limit, title])

  if (!data) return <div className="mt-3 text-sm text-gray-500">Loading chart...</div>

  return (
    <div className="mt-3" style={{ height: chartHeight }}>
      <Line
        data={data}
        height={chartHeight}
        options={{
          maintainAspectRatio: false,
          responsive: true,
          plugins: { legend: { display: data.datasets.length > 1 }, title: { display: !!title, text: title } },
          scales: { x: { display: true }, y: { beginAtZero: metrics.length === 1 && metrics[0] === 'valve_open' } },
        }}
      />
    </div>
  )
}
