# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        End Users                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ HTTP/HTTPS
                     ▼
        ┌────────────────────────────┐
        │  React Frontend (Port 3000) │
        │  ├─ Login/Register Pages   │
        │  ├─ Dashboard              │
        │  ├─ Team Management        │
        │  └─ DNS Management         │
        └────────────┬───────────────┘
                     │
                     │ REST API
                     ▼
        ┌────────────────────────────┐
        │  FastAPI Backend (Port 8000)│
        │  ├─ Auth Endpoints         │
        │  ├─ Team Endpoints         │
        │  └─ DNS Endpoints          │
        └────────────┬───────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │  JWT   │  │  Vault  │  │ name.com │
    │ Auth   │  │  Vault  │  │   API    │
    └────────┘  └─────────┘  └──────────┘
```

## Component Diagram

### Frontend Architecture

```
Frontend/
├── Pages/
│   ├── Login.tsx        → User authentication
│   ├── Register.tsx     → Account creation
│   └── Dashboard.tsx    → Main application
│
├── Components/
│   ├── Navbar.tsx       → Navigation
│   ├── ProtectedRoute   → Route guards
│   └── Forms/Tables     → UI elements
│
├── Services/
│   └── api.ts          → API client with interceptors
│
└── Styles/
    ├── index.css       → Global styles
    ├── common.css      → Component styles
    ├── auth.css        → Auth page styles
    └── dashboard.css   → Dashboard styles
```

### Backend Architecture

```
Backend/
├── app/
│   ├── api/
│   │   ├── auth.py     → Auth endpoints
│   │   ├── teams.py    → Team management
│   │   └── domains.py  → DNS management
│   │
│   ├── auth/
│   │   ├── jwt.py      → Token generation
│   │   ├── vault.py    → Vault client
│   │   └── dependencies.py → Auth middleware
│   │
│   ├── services/
│   │   ├── namecom.py  → name.com API client
│   │   ├── domain.py   → Domain logic
│   │   ├── dns.py      → DNS logic
│   │   ├── team.py     → Team logic
│   │   └── user.py     → User logic
│   │
│   ├── models/
│   │   ├── user.py     → User schemas
│   │   ├── team.py     → Team schemas
│   │   └── domain.py   → Domain schemas
│   │
│   └── config.py       → Configuration
│
└── main.py             → FastAPI app
```

## Data Flow

### Authentication Flow

```
User Input (Username/Password)
         │
         ▼
    Login Endpoint
         │
         ▼
    Validate Credentials
         │
         ├─ Password Check
         ├─ User Exists
         └─ User Active
         │
         ▼
    Generate JWT Token
         │
         ├─ Create Payload
         ├─ Sign with Secret Key
         └─ Set Expiration
         │
         ▼
    Return Token to Client
         │
         ▼
    Store Token in localStorage
         │
         ▼
    Include in API Requests
```

### DNS Record Management Flow

```
User Action (Create/Update/Delete)
         │
         ▼
    Frontend Form Submission
         │
         ▼
    Validate Input
         │
         ▼
    API Request with Token
         │
         ▼
    Backend Receives Request
         │
         ▼
    Verify JWT Token
         │
         ├─ Token Valid?
         ├─ User Authorized?
         └─ Team Owner?
         │
         ▼
    Call name.com API
         │
         ├─ Create Record
         ├─ Update Record
         └─ Delete Record
         │
         ▼
    Update Local Database
         │
         ▼
    Return Response
         │
         ▼
    Update Frontend State
         │
         ▼
    Refresh Dashboard
```

## Integration Points

### name.com API Integration

```
┌──────────────────────────┐
│   NamecomService         │
│  (namecom.py)            │
├──────────────────────────┤
│ Methods:                 │
│ • get_domains()          │
│ • get_domain_records()   │
│ • create_dns_record()    │
│ • update_dns_record()    │
│ • delete_dns_record()    │
└────────────┬─────────────┘
             │
             │ HTTPS (REST)
             ▼
    ┌─────────────────────┐
    │  name.com API       │
    │  https://api.name.com/v4
    └─────────────────────┘
             │
             ├─ GET /domains
             ├─ GET /records
             ├─ POST /records
             ├─ PUT /records
             └─ DELETE /records
```

### Vault Integration

```
┌──────────────────────────┐
│   VaultService           │
│  (vault.py)              │
├──────────────────────────┤
│ Methods:                 │
│ • get_namecom_creds()    │
│ • store_user_token()     │
│ • get_user_token()       │
│ • revoke_user_token()    │
└────────────┬─────────────┘
             │
             │ HTTPS (REST)
             ▼
    ┌─────────────────────┐
    │  HashiCorp Vault    │
    │  http://localhost:8200
    └─────────────────────┘
             │
             ├─ POST /v1/auth/token
             ├─ GET /v1/secret/data/*
             ├─ POST /v1/secret/data/*
             └─ DELETE /v1/secret/data/*
```

## Request/Response Cycle

```
Frontend                          Backend                    External
  │                                 │                         │
  │ 1. Send Request                 │                         │
  │─────────────────────────────────>│                         │
  │ POST /api/auth/login             │                         │
  │ Content-Type: application/json   │                         │
  │                                 │                         │
  │                          2. Validate Input                │
  │                                 │                         │
  │                          3. Check Vault                   │
  │                                 │────────────────────────>│
  │                                 │ GET secret/data/namecom │
  │                                 │<────────────────────────│
  │                                 │ Credentials             │
  │                                 │                         │
  │                          4. Generate Token                │
  │                                 │                         │
  │ 5. Send Response                │                         │
  │<─────────────────────────────────│                         │
  │ {                               │                         │
  │   "access_token": "...",        │                         │
  │   "token_type": "bearer"        │                         │
  │ }                               │                         │
  │                                 │                         │
  │ 6. Store Token                  │                         │
  │ (localStorage)                  │                         │
  │                                 │                         │
  │ 7. API Request with Token       │                         │
  │─────────────────────────────────>│                         │
  │ GET /api/domains                │                         │
  │ Authorization: Bearer <token>   │                         │
  │                                 │                         │
  │                          8. Verify Token                  │
  │                                 │                         │
  │                          9. Fetch from name.com           │
  │                                 │────────────────────────>│
  │                                 │ GET /domains            │
  │                                 │<────────────────────────│
  │                                 │ Domain List             │
  │                                 │                         │
  │ 10. Send Response               │                         │
  │<─────────────────────────────────│                         │
  │ [domains...]                    │                         │
  │                                 │                         │
  │ 11. Update UI                   │                         │
  └                                 └                         ┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│              Production Environment                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │        Load Balancer (nginx/HAProxy)        │  │
│  └────────────┬─────────────────────────────────┘  │
│               │                                    │
│     ┌─────────┴─────────┐                         │
│     │                   │                         │
│  ┌──▼────┐          ┌──▼────┐                    │
│  │Backend│          │Backend│  (Scale up)       │
│  │API #1 │          │API #2 │                    │
│  │:8000  │          │:8001  │                    │
│  └──┬────┘          └──┬────┘                    │
│     └────────┬────────┘                          │
│              │                                   │
│         ┌────▼──────────┐                        │
│         │  PostgreSQL   │                        │
│         │   Database    │                        │
│         └───────────────┘                        │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │     Frontend (React Static Files)         │  │
│  │     Served via CDN/Nginx                  │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │        HashiCorp Vault                    │  │
│  │    (Secrets Management)                   │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
└─────────────────────────────────────────────────┘
             │
             │ HTTPS
             ▼
        ┌─────────────────┐
        │  End Users      │
        └─────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│           DNS Management Platform       │
├─────────────────────────────────────────┤
│                                         │
│  Frontend Layer:                        │
│  • React 18.x (UI Library)              │
│  • TypeScript (Type Safety)             │
│  • Vite (Build Tool)                    │
│  • React Router (Routing)               │
│  • Axios (HTTP Client)                  │
│  • CSS3 (Styling)                       │
│                                         │
│  Backend Layer:                         │
│  • FastAPI (Web Framework)              │
│  • Uvicorn (ASGI Server)                │
│  • Pydantic (Data Validation)           │
│  • PyJWT (Authentication)               │
│  • SQLAlchemy (ORM)                     │
│  • HVAC (Vault Client)                  │
│  • Requests (HTTP Client)               │
│                                         │
│  Infrastructure:                        │
│  • PostgreSQL (Database)                │
│  • Docker (Containerization)            │
│  • name.com API (DNS Provider)          │
│  • HashiCorp Vault (Secrets)            │
│  • nginx (Reverse Proxy)                │
│                                         │
└─────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────┐
│           Security Layers                   │
├─────────────────────────────────────────────┤
│                                             │
│  1. HTTPS/TLS                              │
│     └─ Encrypts data in transit             │
│                                             │
│  2. JWT Authentication                     │
│     └─ Stateless, token-based auth         │
│                                             │
│  3. Vault Integration                      │
│     └─ Secure credential storage            │
│                                             │
│  4. CORS Protection                        │
│     └─ Controls cross-origin requests      │
│                                             │
│  5. Rate Limiting                          │
│     └─ Prevents abuse                      │
│                                             │
│  6. Input Validation                       │
│     └─ Pydantic models validate data       │
│                                             │
│  7. Role-Based Access Control              │
│     └─ Admin, Manager, Member roles        │
│                                             │
│  8. Secure Password Hashing                │
│     └─ SHA-256 hashing                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

This architecture ensures scalability, security, and maintainability across all components.
