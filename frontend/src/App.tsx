import { useState, useEffect, useCallback } from 'react';
import axios, { AxiosError } from 'axios';
import './index.css';

interface SensorReading {
  id: number;
  plot_id: string;
  moisture: number;
  temperature: number;
  ph: number;
  timestamp: string;
}

export default function App() {
  const [readings, setReadings] = useState<SensorReading[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  const fetchReadings = useCallback(async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.get<SensorReading[]>(`${apiUrl}/api/v1/readings?limit=100`);
      setReadings(response.data);
      setError(null);
      setLoading(false);
    } catch (err) {
      let msg = 'Failed to fetch data';
      if (err instanceof AxiosError) msg = err.response?.data?.message || err.message;
      setError(msg);
      setLoading(false);
      setRetryCount(prev => prev + 1);
    }
  }, []);

  useEffect(() => {
    fetchReadings();
    const interval = setInterval(fetchReadings, 5000);
    return () => clearInterval(interval);
  }, [fetchReadings]);

  return (
    <div className="container">
      <header className="header">
        <h1>🌱 GreenPulse</h1>
        <p>Real-time Agricultural Analytics</p>
      </header>

      <main className="main">
        {loading && readings.length === 0 && <div className="loading">Loading...</div>}
        
        {error && (
          <div className="error-container">
            <div className="error">{error}</div>
            <button onClick={() => { setLoading(true); void fetchReadings(); }} className="retry-btn">
              Retry (Attempt {retryCount + 1})
            </button>
          </div>
        )}

        <div className="readings-grid">
          {readings.map((reading) => (
            <div key={reading.id} className="reading-card">
              <h2>Plot: {reading.plot_id}</h2>
              <div className="metric">
                <span className="label">Moisture:</span>
                <span className="value">{reading.moisture}%</span>
              </div>
              <div className="metric">
                <span className="label">Temp:</span>
                <span className="value">{reading.temperature}°C</span>
              </div>
              <div className="metric">
                <span className="label">pH:</span>
                <span className="value">{reading.ph.toFixed(2)}</span>
              </div>
              <div className="timestamp">
                {new Date(reading.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
          {!loading && readings.length === 0 && !error && <p>No data found.</p>}
        </div>
      </main>
    </div>
  );
}