# GreenPulse - Quick Start Guide

## 🚀 5-Minute Setup

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### Step 1: Clone & Setup
```bash
git clone https://github.com/somenparida/GreenPulse.git
cd GreenPulse
cp .env.example.full .env
```

### Step 2: Start Everything
```bash
docker-compose -f docker-compose.full.yml up --build
```

Wait for all services to be healthy (2-3 minutes)

### Step 3: Access the Application

| What | URL |
|------|-----|
| 🌐 Dashboard | http://localhost:3000 |
| 📊 API Docs | http://localhost:8000/docs |
| 🗄️ Database GUI | http://localhost:5050 |

### Step 4: Send Some Data
```bash
curl -X POST http://localhost:8000/api/v1/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "plot_id": "field-1",
    "moisture": 65.5,
    "temperature": 24.3,
    "ph": 6.8
  }'
```

### Step 5: Watch the Dashboard
Refresh http://localhost:3000 and see your data appear!

---

## 📁 Project Structure

```
├── frontend/          ← React web app (Port 3000)
├── backend/           ← FastAPI REST API (Port 8000)
├── docker-compose.full.yml
├── init-db.sql        ← Database setup
└── .env.example.full  ← Configuration
```

---

## 🐳 Docker Commands

```bash
# Start services (foreground)
docker-compose -f docker-compose.full.yml up

# Start services (background)
docker-compose -f docker-compose.full.yml up -d

# View logs
docker-compose -f docker-compose.full.yml logs -f backend

# Stop everything
docker-compose -f docker-compose.full.yml down

# Remove all data
docker-compose -f docker-compose.full.yml down -v

# Restart a service
docker-compose -f docker-compose.full.yml restart backend
```

---

## 💾 Service Details

### Frontend (React @ Port 3000)
- Modern React dashboard
- Real-time sensor data
- Dark theme UI
- Auto-refresh every 5 seconds

### Backend (FastAPI @ Port 8000)
- REST API for sensor data
- Automatic Swagger/OpenAPI docs
- Health checks included
- Database queries optimized

### Database (PostgreSQL @ Port 5432)
- User: `greenpulse`
- Password: `greenpulse_password`
- Database: `greenpulse`
- 3 sample plots included

### pgAdmin (Port 5050)
- Email: `admin@example.com`
- Password: `admin`
- Visual database manager

---

## 🔗 API Examples

### Get all readings
```bash
curl http://localhost:8000/api/v1/readings
```

### Get readings for a specific plot (last 24 hours)
```bash
curl "http://localhost:8000/api/v1/readings/plot/plot-001?hours=24"
```

### Get statistics
```bash
curl http://localhost:8000/api/v1/stats
```

### Health check
```bash
curl http://localhost:8000/health
```

---

## 📊 Database Access

### Via pgAdmin GUI
1. Open http://localhost:5050
2. Login with `admin@example.com` / `admin`
3. Add server: Host=`db`, Port=`5432`, User=`greenpulse`, Password=`greenpulse_password`

### Via Command Line
```bash
docker exec -it greenpulse-db psql -U greenpulse -d greenpulse

# View tables
\dt

# View data
SELECT * FROM sensor_readings;

# Exit
\q
```

---

## ⚙️ Configuration

Edit `.env` file to customize:

```env
# Database credentials
POSTGRES_USER=greenpulse
POSTGRES_PASSWORD=your_password_here
POSTGRES_DB=greenpulse

# Frontend API URL
VITE_API_URL=http://localhost:8000

# pgAdmin credentials
PGADMIN_EMAIL=your_email@example.com
PGADMIN_PASSWORD=your_password_here
```

---

## 🚨 Troubleshooting

### "Connection refused" errors
```bash
# Wait longer for database to start
docker-compose -f docker-compose.full.yml down
docker-compose -f docker-compose.full.yml up
```

### Port already in use
```bash
# Find what's using the port (3000 example)
lsof -i :3000

# Kill the process
kill -9 <PID>
```

### Rebuild everything from scratch
```bash
docker-compose -f docker-compose.full.yml down -v --remove-orphans
docker system prune -a
docker-compose -f docker-compose.full.yml up --build
```

---

## 📚 Documentation

- **Detailed Setup**: See [DOCKER_COMPOSE_GUIDE.md](DOCKER_COMPOSE_GUIDE.md)
- **Architecture**: See [STACK_ARCHITECTURE.md](STACK_ARCHITECTURE.md)
- **Kubernetes**: See [infrastructure/kubernetes/](infrastructure/kubernetes/)
- **Terraform (AWS)**: See [infrastructure/terraform/](infrastructure/terraform/)

---

## 🔒 Security Notes

⚠️ **This is a development setup. For production:**
- Change all default passwords
- Enable HTTPS/SSL
- Setup authentication (JWT)
- Enable CORS restrictions
- Add rate limiting
- Setup backups
- Enable database encryption

---

## 📝 Next Steps

1. ✅ Start the stack
2. ✅ Send test data
3. ✅ View on dashboard
4. 🔄 Integrate your own IoT devices
5. 🚀 Deploy to production (see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md))

---

## 🆘 Need Help?

- Check logs: `docker-compose -f docker-compose.full.yml logs -f`
- Read [CONTRIBUTING.md](docs/CONTRIBUTING.md)
- Review [SECURITY.md](SECURITY.md)
- Open GitHub issue

---

**Happy farming! 🌱**
