# API Documentation

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except `/register` and `/login`) require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Response Format

All endpoints return JSON responses with consistent structure:

```json
{
  "data": {},
  "error": null,
  "message": "Success"
}
```

## Endpoints

### Authentication

#### Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "message": "User registered successfully"
}
```

#### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Get Current User

```http
GET /api/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-20T10:00:00"
}
```

### Teams

#### List Teams

```http
GET /api/teams
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "My Team",
    "description": "Team description",
    "owner_id": 1,
    "created_at": "2024-01-20T10:00:00"
  }
]
```

#### Create Team

```http
POST /api/teams
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Team",
  "description": "Team description"
}
```

#### Get Team Details

```http
GET /api/teams/{team_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "name": "My Team",
  "description": "Team description",
  "owner_id": 1,
  "created_at": "2024-01-20T10:00:00",
  "members": [
    {
      "user_id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "role": "admin",
      "joined_at": "2024-01-20T10:00:00"
    }
  ],
  "member_count": 1
}
```

#### Update Team

```http
PUT /api/teams/{team_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Team Name",
  "description": "Updated description"
}
```

#### Delete Team

```http
DELETE /api/teams/{team_id}
Authorization: Bearer <token>
```

#### Add Team Member

```http
POST /api/teams/{team_id}/members/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "role": "member"
}
```

#### Remove Team Member

```http
DELETE /api/teams/{team_id}/members/{user_id}
Authorization: Bearer <token>
```

### Domains & DNS Records

#### List Domains

```http
GET /api/domains
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "name": "example.com",
    "namecom_id": "12345"
  }
]
```

#### Get Domain Details

```http
GET /api/domains/{domain_name}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "name": "example.com",
  "namecom_id": "12345",
  "team_id": 1,
  "records": [
    {
      "id": 1,
      "domain": "example.com",
      "name": "@",
      "type": "A",
      "content": "192.0.2.1",
      "ttl": 3600,
      "priority": null,
      "created_at": "2024-01-20T10:00:00"
    }
  ]
}
```

#### List DNS Records

```http
GET /api/domains/{domain_name}/records
Authorization: Bearer <token>
```

#### Create DNS Record

```http
POST /api/domains/{domain_name}/records
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "www",
  "type": "A",
  "content": "192.0.2.1",
  "ttl": 3600,
  "priority": null
}
```

**Supported Record Types:**
- A (IPv4 address)
- AAAA (IPv6 address)
- CNAME (Canonical name)
- MX (Mail exchange)
- TXT (Text record)
- NS (Name server)
- SRV (Service)
- SOA (Start of authority)

#### Update DNS Record

```http
PUT /api/domains/{domain_name}/records/{record_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "192.0.2.2",
  "ttl": 7200,
  "priority": null
}
```

#### Delete DNS Record

```http
DELETE /api/domains/{domain_name}/records/{record_id}
Authorization: Bearer <token>
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized

```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden

```json
{
  "detail": "You don't have permission to perform this action"
}
```

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

API endpoints are rate limited to:
- 100 requests per minute per IP
- 1000 requests per hour per user

## Pagination

List endpoints support pagination:

```http
GET /api/teams?page=1&limit=10
```

## Filtering

Some endpoints support filtering:

```http
GET /api/domains?team_id=1
```

## Sorting

Results can be sorted:

```http
GET /api/teams?sort=-created_at
```

Use `-` prefix for descending order.

## Interactive Documentation

Access Swagger UI at: `http://localhost:8000/docs`

Access ReDoc at: `http://localhost:8000/redoc`
