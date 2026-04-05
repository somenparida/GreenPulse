-- Create extensions
CREATE EXTENSION IF NOT EXISTS uuid-ossp;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create tables
CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    plot_id VARCHAR(100) NOT NULL,
    moisture FLOAT NOT NULL,
    temperature FLOAT NOT NULL,
    ph FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_plot_id ON sensor_readings(plot_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_plot_timestamp ON sensor_readings(plot_id, timestamp DESC);

-- Insert sample data
INSERT INTO sensor_readings (plot_id, moisture, temperature, ph) VALUES
    ('plot-001', 65.5, 24.3, 6.8),
    ('plot-002', 72.1, 26.1, 7.2),
    ('plot-003', 58.9, 22.5, 6.5),
    ('plot-001', 68.2, 25.1, 6.9),
    ('plot-002', 71.5, 26.8, 7.1);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO greenpulse;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO greenpulse;
