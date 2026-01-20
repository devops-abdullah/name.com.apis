# Setup Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager
- name.com API credentials
- HashiCorp Vault (optional, for production)

## Backend Setup

### 1. Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
NAMECOM_API_KEY=your_name_com_api_key
NAMECOM_API_TOKEN=your_name_com_api_token
NAMECOM_USERNAME=your_name_com_username

# Vault Configuration (optional)
VAULT_ADDR=http://localhost:8200
VAULT_TOKEN=your_vault_token

# JWT Configuration
JWT_SECRET_KEY=your_super_secret_key_change_in_production

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### 4. Run Backend Server

```bash
python main.py
```

The API will start at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure (Optional)

Edit `vite.config.ts` to change the API proxy target if needed.

### 3. Run Development Server

```bash
npm run dev
```

The application will start at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
```

## Getting name.com API Credentials

1. Go to [name.com](https://www.name.com)
2. Sign in to your account
3. Go to Settings → Account Settings
4. Find API section
5. Generate or copy your API Key and Token
6. Add your account username

## Vault Setup (Production)

### 1. Install Vault

```bash
# macOS
brew install vault

# Or download from https://www.vaultproject.io/downloads
```

### 2. Start Vault Server

```bash
vault server -dev
```

### 3. Store Credentials in Vault

```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='your_root_token'

# Store name.com credentials
vault kv put secret/namecom \
  api_key="your_api_key" \
  api_token="your_api_token" \
  username="your_username"
```

## Troubleshooting

### Port Already in Use

If port 8000 (backend) or 3000 (frontend) is in use:

**Backend:**
```bash
# Change port in .env
API_PORT=8001
python main.py
```

**Frontend:**
```bash
# Vite will ask to use next available port
npm run dev
```

### CORS Errors

Update CORS origins in `backend/main.py`:
```python
allow_origins=["http://localhost:3000", "your_frontend_url"],
```

### Import Errors in Backend

Ensure you're in the virtual environment:
```bash
# Verify virtual environment is active
which python  # Should show venv path
pip list      # Should show installed packages
```

### Frontend Build Errors

Clear node_modules and reinstall:
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

## Running Both Services

### Option 1: Two Terminal Windows

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Using Process Manager

Install pm2:
```bash
npm install -g pm2
```

Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [
    {
      name: 'dns-api-backend',
      script: 'backend/main.py',
      interpreter: 'python',
    },
    {
      name: 'dns-api-frontend',
      script: 'npm',
      args: '--prefix frontend run dev',
    }
  ]
};
```

Run:
```bash
pm2 start ecosystem.config.js
```

## Database Setup (Optional)

To add database support:

### 1. Install Database Driver

```bash
pip install psycopg2-binary  # PostgreSQL
# or
pip install mysql-connector-python  # MySQL
```

### 2. Update .env

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dns_manager
```

### 3. Create Models

See `backend/app/models/db.py` for database model examples.

## Next Steps

1. Start the backend and frontend servers
2. Visit `http://localhost:3000`
3. Register a new account
4. Create a team
5. Start managing your DNS records!

## Support

For detailed API documentation, visit: `http://localhost:8000/docs`

For more information, check the main [README.md](../README.md)
