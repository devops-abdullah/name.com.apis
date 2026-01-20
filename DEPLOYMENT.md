# Deployment Guide

## Production Checklist

- [ ] Change JWT_SECRET_KEY in .env
- [ ] Enable HTTPS
- [ ] Set DEBUG=False
- [ ] Configure proper database (not SQLite)
- [ ] Set up environment variables securely
- [ ] Configure CORS for production domain
- [ ] Set up error logging
- [ ] Configure rate limiting
- [ ] Enable security headers
- [ ] Set up monitoring and alerts

## Docker Deployment

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t dns-api-backend .
docker run -p 8000:8000 --env-file .env dns-api-backend
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package.json .
RUN npm install

COPY . .
RUN npm run build

FROM node:18-alpine
RUN npm install -g serve
COPY --from=builder /app/dist /app

EXPOSE 3000
CMD ["serve", "-s", ".", "-l", "3000"]
```

Build and run:
```bash
docker build -t dns-api-frontend .
docker run -p 3000:3000 dns-api-frontend
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - NAMECOM_API_KEY=${NAMECOM_API_KEY}
      - NAMECOM_API_TOKEN=${NAMECOM_API_TOKEN}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DATABASE_URL=postgresql://user:password@db:5432/dns_manager
    depends_on:
      - db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dns_manager
    volumes:
      - postgres_data:/var/lib/postgresql/data

  vault:
    image: vault:latest
    ports:
      - "8200:8200"
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=devtoken
    cap_add:
      - IPC_LOCK

volumes:
  postgres_data:
```

Run with Docker Compose:
```bash
docker-compose up
```

## Cloud Deployment

### AWS EC2

1. Create EC2 instance (Ubuntu 22.04)
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip nodejs npm
   ```
3. Clone repository
4. Follow setup instructions
5. Use systemd for auto-start

### Heroku

Create `Procfile`:
```
web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
```

Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Set environment variables
3. Deploy

### Railway.app

1. Connect GitHub
2. Add database
3. Deploy

## Database Setup

### PostgreSQL

```bash
# Create database
createdb dns_manager

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://user:password@localhost:5432/dns_manager
```

### MySQL

```bash
# Create database
mysql -u root -p
CREATE DATABASE dns_manager;
```

## Security

### HTTPS Setup

```bash
# Generate self-signed certificate (development)
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

### Rate Limiting

Install slowapi:
```bash
pip install slowapi
```

### CORS Configuration

Update `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Monitoring

### Application Performance

Install monitoring tools:
```bash
pip install prometheus-client
```

### Logging

Configure logging in `main.py`:
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Backups

Create backup script:
```bash
#!/bin/bash
pg_dump dns_manager > backup_$(date +%Y%m%d).sql
```

## Scaling

- Use load balancer (nginx, HAProxy)
- Scale horizontally with multiple API instances
- Use CDN for frontend assets
- Cache DNS records with Redis
