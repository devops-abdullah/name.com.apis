# Quick Start Guide

## 30-Second Setup

### For Windows Users

Double-click `setup.bat` and follow the prompts.

### For Mac/Linux Users

```bash
bash setup.sh
```

## Manual Setup (2 minutes)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Mac/Linux
# or
venv\Scripts\activate             # Windows

pip install -r requirements.txt
cp .env.example .env

# Edit .env with your name.com API credentials
python main.py
```

### Frontend (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

## What You Get

✅ Beautiful DNS Management Dashboard
✅ Real-time DNS Record CRUD Operations
✅ Team Collaboration Features
✅ Secure JWT Authentication
✅ Vault Integration Ready
✅ Production-ready Code
✅ Full API Documentation

## Directory Structure

```
📦 name.com.apis
├── 📂 backend/          Python FastAPI backend
├── 📂 frontend/         React TypeScript frontend
├── 📄 setup.sh          Mac/Linux setup
├── 📄 setup.bat         Windows setup
├── 📄 SETUP.md          Detailed setup guide
├── 📄 API_DOCS.md       API documentation
├── 📄 DEPLOYMENT.md     Deployment guide
└── 📄 README.md         Project overview
```

## First Steps

1. **Register**: Create your account at `http://localhost:3000`
2. **Login**: Use your credentials
3. **Create Team**: Start a new team for your organization
4. **View Domains**: See all domains from your name.com account
5. **Manage DNS**: Create, edit, delete DNS records

## Key Files to Know

### Backend
- `backend/main.py` - Start the API server
- `backend/app/config.py` - Configuration
- `backend/app/services/namecom.py` - name.com API integration
- `backend/.env` - Your credentials (⚠️ Keep secure!)

### Frontend
- `frontend/src/App.tsx` - Main React app
- `frontend/src/pages/` - Page components
- `frontend/src/services/api.ts` - API client
- `frontend/vite.config.ts` - Build configuration

## Important: Environment Setup

Create `backend/.env` with:
```
NAMECOM_API_KEY=your_key
NAMECOM_API_TOKEN=your_token
NAMECOM_USERNAME=your_username
JWT_SECRET_KEY=your_secret_key_here
```

Get these from [name.com API Settings](https://www.name.com/account/settings/api)

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change `API_PORT=8001` in `.env` |
| Port 3000 in use | Vite will prompt for alternate port |
| Module not found | Ensure virtual env is activated |
| CORS errors | Check API_URL in frontend config |
| 401 Unauthorized | Token may have expired, login again |

## Available Commands

### Backend
```bash
# Development server
python main.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# Run with Docker
docker build -t dns-api .
docker run -p 8000:8000 dns-api
```

### Frontend
```bash
# Development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Getting Help

1. **API Docs**: `http://localhost:8000/docs`
2. **Setup Issues**: See [SETUP.md](SETUP.md)
3. **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
4. **API Details**: See [API_DOCS.md](API_DOCS.md)

## Next Steps

- [ ] Complete the setup
- [ ] Create an account
- [ ] Create a team
- [ ] Add team members
- [ ] Manage your first DNS record
- [ ] Read [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- [ ] Customize the UI in `frontend/src/styles/`
- [ ] Add additional features as needed

## Features Overview

### 🔐 Authentication
- User registration and login
- JWT token-based auth
- Vault integration for secrets
- Secure password hashing

### 👥 Teams
- Create and manage teams
- Add/remove team members
- Role-based access (admin, manager, member)
- Team-specific domain management

### 🌐 DNS Management
- List all domains
- View DNS records
- Create new records (A, AAAA, CNAME, MX, TXT, etc.)
- Update existing records
- Delete records
- Real-time synchronization

### 🎨 Beautiful UI
- Modern gradient design
- Responsive layout
- Smooth animations
- Dark mode ready
- Mobile friendly

## System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.8+ |
| Node.js | 16+ |
| npm | 7+ |
| RAM | 2GB minimum |
| Disk Space | 500MB |
| Browser | Chrome, Firefox, Safari, Edge |

## Production Checklist

Before deploying to production:

- [ ] Change JWT_SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up proper CORS
- [ ] Configure rate limiting
- [ ] Set up monitoring
- [ ] Enable security headers
- [ ] Use environment variables
- [ ] Set up backups

See [DEPLOYMENT.md](DEPLOYMENT.md) for details.

## Support & Resources

- 📚 [Full README](README.md)
- 🚀 [Setup Guide](SETUP.md)  
- 📖 [API Documentation](API_DOCS.md)
- 🐳 [Deployment Guide](DEPLOYMENT.md)
- 🔗 [name.com Documentation](https://www.name.com/api-docs)

---

**Ready to get started?** Run the setup script now! 🎉
