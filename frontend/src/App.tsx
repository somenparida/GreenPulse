import { useState, useEffect } from 'react'
import axios, { AxiosError } from 'axios'
import './index.css'

interface SensorReading {
  id: number
  plot_id: string
  moisture: number
  temperature: number
  ph: number
  timestamp: string
}

interface ApiError {
  message: string
  code?: string
}

function App() {
  const [readings, setReadings] = useState<SensorReading[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [retryCount, setRetryCount] = useState(0)

  useEffect(() => {
    fetchReadings()
    const interval = setInterval(fetchReadings, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchReadings = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.get<SensorReading[]>(
        `${apiUrl}/api/v1/readings?limit=100`
      )
      setReadings(response.data)
      setLoading(false)
      setError(null)
      setRetryCount(0)
    } catch (err) {
      const errorMessage =
        err instanceof AxiosError
          ? err.response?.data?.message || err.message
          : 'Failed to fetch sensor readings'
      setError(errorMessage)
      setLoading(false)
      setRetryCount((prev) => prev + 1)
    }
  }

  const handleRetry = () => {
    setLoading(true)
    setError(null)
    fetchReadings()
  }

  return (
    <div className="container">
      <header className="header">
        <h1>🌱 GreenPulse</h1>
        <p>Real-time Agricultural Analytics Dashboard</p>
      </header>

      <main className="main">
        {loading && <div className="loading">Loading sensor data...</div>}
        {error && (
          <div className="error-container">
            <div className="error">{error}</div>
            <button onClick={handleRetry} className="retry-btn">
              Retry (Attempt {retryCount + 1})
            </button>
          </div>
        )}

        <div className="readings-grid">
          {readings.length > 0 ? (
            readings.map((reading) => (
              <div key={reading.id} className="reading-card">
                <h2>Plot: {reading.plot_id}</h2>
                <div className="metric">
                  <span className="label">Moisture:</span>
                  <span className="value">{reading.moisture}%</span>
                </div>
                <div className="metric">
                  <span className="label">Temperature:</span>
                  <span className="value">{reading.temperature}°C</span>
                </div>
                <div className="metric">
                  <span className="label">pH Level:</span>
                  <span className="value">{reading.ph.toFixed(2)}</span>
                </div>
                <div className="timestamp">{new Date(reading.timestamp).toLocaleString()}</div>
              </div>
            ))
          ) : !loading ? (
            <p className="no-data">No sensor data available</p>
          ) : null}
        </div>
      </main>

      <footer className="footer">
        <p>Connected to Backend at {import.meta.env.VITE_API_URL || 'http://localhost:8000'}</p>
      </footer>
    </div>
  )
}

export default App
