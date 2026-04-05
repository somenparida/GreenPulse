# Docker Compose Documentation

## Quick Start

```bash
# Clone repository
git clone https://github.com/somenparida/GreenPulse.git
cd GreenPulse

# Copy environment file
cp .env.example.full .env

# Start all services
docker-compose -f docker-compose.full.yml up --build
```

## Services

### 1. PostgreSQL Database
- **Port**: 5432
- **User**: `greenpulse`
- **Password**: `greenpulse_password` (change in .env)
- **Database**: `greenpulse`

### 2. Backend API (FastAPI)
- **Port**: 8000
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

### 3. Frontend (React)
- **Port**: 3000
- **URL**: http://localhost:3000

### 4. pgAdmin (Database GUI)
- **Port**: 5050
- **URL**: http://localhost:5050
- **Email**: `admin@example.com`
- **Password**: `admin` (change in .env)

## Common Commands

```bash
# Start services
docker-compose -f docker-compose.full.yml up

# Start in background
docker-compose -f docker-compose.full.yml up -d

# View logs
docker-compose -f docker-compose.full.yml logs -f backend

# Stop services
docker-compose -f docker-compose.full.yml down

# Remove volumes (data)
docker-compose -f docker-compose.full.yml down -v

# Rebuild containers
docker-compose -f docker-compose.full.yml up --build

# Run backend tests
docker-compose -f docker-compose.full.yml exec backend pytest

# Access database shell
docker exec -it greenpulse-db psql -U greenpulse -d greenpulse
```

## Database Access

### Using psql
```bash
docker exec -it greenpulse-db psql -U greenpulse -d greenpulse

# View tables
\dt

# View data
SELECT * FROM sensor_readings;
```

### Using pgAdmin
1. Open http://localhost:5050
2. Login with email: admin@example.com, password: admin
3. Add new server:
   - Name: GreenPulse
   - Host: db
   - Port: 5432
   - Username: greenpulse
   - Password: greenpulse_password

## API Endpoints

### Telemetry (Ingest)
```bash
curl -X POST http://localhost:8000/api/v1/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "plot_id": "plot-001",
    "moisture": 65.5,
    "temperature": 24.3,
    "ph": 6.8
  }'
```

### Get Readings
```bash
# All readings
curl http://localhost:8000/api/v1/readings

# By plot
curl "http://localhost:8000/api/v1/readings/plot/plot-001?hours=24"

# Specific reading
curl http://localhost:8000/api/v1/readings/1
```

### Get Stats
```bash
curl http://localhost:8000/api/v1/stats
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Environment Variables

Create `.env` file based on `.env.example.full`:

```env
# Database
POSTGRES_USER=greenpulse
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=greenpulse

# Backend
DATABASE_URL=postgresql://greenpulse:password@db:5432/greenpulse
DEBUG=false

# Frontend
VITE_API_URL=http://localhost:8000

# pgAdmin
PGADMIN_EMAIL=your_email@example.com
PGADMIN_PASSWORD=your_secure_password
```

## Troubleshooting

### Services fail to start
```bash
# Check logs
docker-compose -f docker-compose.full.yml logs

# Rebuild from scratch
docker-compose -f docker-compose.full.yml down -v
docker-compose -f docker-compose.full.yml up --build
```

### Database connection error
```bash
# Wait for database to be ready
docker-compose -f docker-compose.full.yml exec backend python -c \
  "import time; time.sleep(10)"

# Restart backend
docker-compose -f docker-compose.full.yml restart backend
```

### Cannot connect to frontend
```bash
# Check if port 3000 is in use
lsof -i :3000

# Clear Docker cache
docker system prune -a
```

## Development

### Backend Development
```bash
# SSH into backend
docker-compose -f docker-compose.full.yml exec backend sh

# Install new packages
docker-compose -f docker-compose.full.yml exec backend pip install package_name

# Run tests
docker-compose -f docker-compose.full.yml exec backend pytest -v
```

### Frontend Development
```bash
# SSH into frontend
docker-compose -f docker-compose.full.yml exec frontend sh

# Install new packages
docker-compose -f docker-compose.full.yml exec frontend npm install package_name

# Build
docker-compose -f docker-compose.full.yml exec frontend npm run build
```

## Production Deployment

For production, use the original `docker-compose.yml` with:
- Environment-specific `.env` file
- Reverse proxy (Nginx/Apache)
- HTTPS certificates
- Resource limits
- Restart policies
- Monitoring & logging
