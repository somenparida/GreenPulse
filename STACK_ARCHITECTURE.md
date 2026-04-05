# GreenPulse - Complete Stack Architecture

## Project Overview

GreenPulse is a full-stack IoT agricultural analytics platform with:
- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI + Python + SQLAlchemy
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose

## Directory Structure

```
GreenPulse/
├── frontend/                    # React.js Web Application
│   ├── src/
│   │   ├── App.tsx             # Main React component
│   │   ├── main.tsx            # React entry point
│   │   ├── index.css           # Styling
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile              # Frontend container
│   ├── .env.example
│   └── tsconfig.json
│
├── backend/                     # FastAPI Python API
│   ├── main.py                 # Application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database models & connection
│   ├── schemas.py              # Pydantic data models
│   ├── routes.py               # API endpoints
│   ├── health.py               # Health check endpoints
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend container
│   ├── .env.example
│   └── __pycache__
│
├── docker-compose.full.yml     # Complete stack (DB + Backend + Frontend + pgAdmin)
├── init-db.sql                 # Database initialization script
├── .env.example.full           # Environment variables template
│
├── docs/
│   └── CONTRIBUTING.md         # Contribution guidelines
│
├── infrastructure/             # Existing K8s & Terraform configs
│
├── DOCKER_COMPOSE_GUIDE.md     # Docker Compose documentation
├── LICENSE
├── SECURITY.md
├── README.md
└── .gitignore
```

## Quick Start (Docker Compose)

### 1. Clone Repository
```bash
git clone https://github.com/somenparida/GreenPulse.git
cd GreenPulse
```

### 2. Setup Environment
```bash
cp .env.example.full .env
```

### 3. Start All Services
```bash
docker-compose -f docker-compose.full.yml up --build
```

### 4. Access Applications

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | - |
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| pgAdmin | http://localhost:5050 | admin@example.com / admin |
| Database | localhost:5432 | greenpulse / greenpulse_password |

### 5. Insert Sample Data
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

### 6. View Dashboard
Open http://localhost:3000 in your browser

## Project Components

### Frontend (`/frontend`)

**Technology Stack:**
- React 18+ with TypeScript
- Vite (Fast build tool)
- Axios (HTTP client)
- Chart.js (Data visualization)

**Key Files:**
- `src/App.tsx` - Main dashboard component
- `src/index.css` - Styling
- `vite.config.ts` - Vite configuration
- `Dockerfile` - Multi-stage build for production

**Features:**
- Real-time sensor data display
- Responsive card-based layout
- Auto-refresh (5s interval)
- Dark theme UI
- Error handling

### Backend (`/backend`)

**Technology Stack:**
- FastAPI (Modern Python web framework)
- SQLAlchemy (ORM)
- Pydantic (Data validation)
- PostgreSQL (Database)

**Key Files:**
- `main.py` - Application factory & routes
- `database.py` - Database models & connection
- `schemas.py` - Request/response validation
- `routes.py` - API endpoints
- `health.py` - Health check endpoints
- `config.py` - Configuration management

**API Endpoints:**

```
POST   /api/v1/telemetry           - Ingest sensor data
GET    /api/v1/readings            - Get all readings
GET    /api/v1/readings/{id}       - Get specific reading
GET    /api/v1/readings/plot/{id}  - Get plot readings
GET    /api/v1/stats               - Get aggregated stats
GET    /health                     - Health check
GET    /health/live                - Liveness probe
GET    /health/ready               - Readiness probe
GET    /docs                       - Swagger UI documentation
```

### Database (`PostgreSQL`)

**Tables:**
- `sensor_readings` - Telemetry data storage

**Schema:**
```sql
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    plot_id VARCHAR(100),
    moisture FLOAT,
    temperature FLOAT,
    ph FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `idx_plot_id` - Fast plot queries
- `idx_timestamp` - Recent data queries
- `idx_plot_timestamp` - Combined queries

## Development Workflow

### Local Development (Without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Database:**
```bash
# Start PostgreSQL locally or use Docker
docker run -d \
  -e POSTGRES_USER=greenpulse \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=greenpulse \
  -p 5432:5432 \
  postgres:16-alpine
```

### With Docker Compose

```bash
docker-compose -f docker-compose.full.yml up --build -d
docker-compose -f docker-compose.full.yml logs -f
```

## Testing

### Backend Tests
```bash
docker-compose -f docker-compose.full.yml exec backend pytest
```

### Frontend Lint
```bash
docker-compose -f docker-compose.full.yml exec frontend npm run lint
```

## Production Deployment

### Kubernetes
See `infrastructure/kubernetes/base/` for K8s manifests

### AWS with Terraform
See `infrastructure/terraform/` for IaC configuration

### Docker Compose (Standalone)
```bash
docker-compose -f docker-compose.full.yml up -d
# Configure reverse proxy (Nginx)
# Setup SSL certificates
# Configure monitoring & logging
```

## Monitoring & Logging

### Health Checks
- Frontend: http://localhost:3000/
- Backend: http://localhost:8000/health
- Database: PostgreSQL connection test

### Logs
```bash
# All services
docker-compose -f docker-compose.full.yml logs -f

# Specific service
docker-compose -f docker-compose.full.yml logs -f backend
```

### Database Access
```bash
# pgAdmin UI
http://localhost:5050

# psql CLI
docker exec -it greenpulse-db psql -U greenpulse -d greenpulse
```

## Environment Variables

### `.env` File
```env
# Database
POSTGRES_USER=greenpulse
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=greenpulse

# Backend
DATABASE_URL=postgresql://greenpulse:password@db:5432/greenpulse
DEBUG=false

# Frontend
VITE_API_URL=http://localhost:8000

# pgAdmin
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=secure_password
```

## Performance Optimization

### Frontend
- Code splitting with Vite
- Lazy loading components
- Caching strategy
- CDN distribution

### Backend
- Database indexes on frequently queried columns
- Connection pooling
- Query optimization
- Rate limiting

### Database
- Regular backups
- Log maintenance
- Query monitoring
- Replication setup

## Security Practices

✅ **Implemented:**
- CORS configuration
- Environment variable secrets
- Data validation (Pydantic)
- SQL injection prevention (SQLAlchemy ORM)
- HTTPS support ready

⚠️ **Recommended for Production:**
- API authentication (JWT)
- Rate limiting
- HTTPS/SSL certificates
- WAF (Web Application Firewall)
- Database encryption
- Regular security audits

## Troubleshooting

### Services won't start
```bash
docker-compose -f docker-compose.full.yml down -v
docker-compose -f docker-compose.full.yml up --build
```

### Database connection issues
```bash
docker-compose -f docker-compose.full.yml logs db
```

### Frontend can't reach backend
Check `frontend/.env` and `VITE_API_URL` setting

### Port already in use
```bash
# Change ports in docker-compose.full.yml
# Or kill existing process
lsof -i :3000  # Find process
kill -9 <PID>  # Kill it
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](./DOCKER_COMPOSE_GUIDE.md)

## Support

For issues, questions, or contributions:
1. Check [CONTRIBUTING.md](docs/CONTRIBUTING.md)
2. Review [SECURITY.md](SECURITY.md)
3. Open a GitHub issue
4. Create a pull request

## License

MIT License - See [LICENSE](LICENSE)
