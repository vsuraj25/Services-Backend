# API Examples

This document contains example requests and responses for the Worker Marketplace API.

## Authentication Flow

### 1. Send OTP

**Request:**
```bash
POST /auth/send-otp
Content-Type: application/json

{
    "phone": "+1234567890"
}
```

**Response:**
```json
{
    "success": true,
    "message": "OTP sent successfully",
    "otp": "123456"
}
```

### 2. Verify OTP (New User Registration)

**Request:**
```bash
POST /auth/verify-otp
Content-Type: application/json

{
    "phone": "+1234567890",
    "otp": "123456",
    "role": "customer"
}
```

**Response:**
```json
{
    "success": true,
    "message": "User registered successfully",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "phone": "+1234567890",
            "role": "customer"
        }
    }
}
```

### 3. Verify OTP (Existing User Login)

**Request:**
```bash
POST /auth/verify-otp
Content-Type: application/json

{
    "phone": "+1234567890",
    "otp": "123456",
    "role": "worker"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "user": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "phone": "+1234567890",
            "role": "worker"
        }
    }
}
```

### 4. Get Current User Profile

**Request:**
```bash
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Customer):**
```json
{
    "success": true,
    "message": "User profile retrieved successfully",
    "data": {
        "user": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "phone": "+1234567890",
            "role": "customer",
            "is_active": true,
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        },
        "profile": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "John Doe",
            "email": "john@example.com",
            "default_address": "123 Main St, City, State",
            "lat": 40.7128,
            "lng": -74.0060
        }
    }
}
```

**Response (Worker):**
```json
{
    "success": true,
    "message": "User profile retrieved successfully",
    "data": {
        "user": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "phone": "+1234567890",
            "role": "worker",
            "is_active": true,
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        },
        "profile": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Jane Smith",
            "bio": "Experienced electrician with 10+ years of experience",
            "experience_years": 10,
            "is_verified": true,
            "rating": 4.5,
            "total_jobs": 150,
            "is_online": true,
            "current_lat": 40.7128,
            "current_lng": -74.0060,
            "last_active": "2024-01-01T15:30:00"
        },
        "skills": [
            {
                "id": "456e7890-e89b-12d3-a456-426614174001",
                "skill_name": "Electrical Wiring",
                "experience_level": "expert"
            },
            {
                "id": "789e0123-e89b-12d3-a456-426614174002",
                "skill_name": "Circuit Breaker Installation",
                "experience_level": "advanced"
            }
        ]
    }
}
```

## Customer APIs

### 1. Get Customer Profile

**Request:**
```bash
GET /customer/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "success": true,
    "message": "Customer profile retrieved successfully",
    "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "John Doe",
        "email": "john@example.com",
        "default_address": "123 Main St, City, State",
        "lat": 40.7128,
        "lng": -74.0060
    }
}
```

### 2. Update Customer Profile

**Request:**
```bash
PUT /customer/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "default_address": "456 Oak Ave, New City, State",
    "lat": 40.7580,
    "lng": -73.9855
}
```

**Response:**
```json
{
    "success": true,
    "message": "Customer profile updated successfully",
    "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "default_address": "456 Oak Ave, New City, State",
        "lat": 40.7580,
        "lng": -73.9855
    }
}
```

## Worker APIs

### 1. Get Worker Profile

**Request:**
```bash
GET /worker/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "success": true,
    "message": "Worker profile retrieved successfully",
    "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Jane Smith",
        "bio": "Experienced electrician with 10+ years of experience",
        "experience_years": 10,
        "is_verified": true,
        "rating": 4.5,
        "total_jobs": 150,
        "is_online": true,
        "current_lat": 40.7128,
        "current_lng": -74.0060,
        "last_active": "2024-01-01T15:30:00"
    }
}
```

### 2. Update Worker Profile

**Request:**
```bash
PUT /worker/profile
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "name": "Jane Smith",
    "bio": "Master electrician specializing in residential and commercial wiring",
    "experience_years": 12
}
```

**Response:**
```json
{
    "success": true,
    "message": "Worker profile updated successfully",
    "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Jane Smith",
        "bio": "Master electrician specializing in residential and commercial wiring",
        "experience_years": 12,
        "is_verified": true,
        "rating": 4.5,
        "total_jobs": 150,
        "is_online": true,
        "current_lat": 40.7128,
        "current_lng": -74.0060,
        "last_active": "2024-01-01T15:30:00"
    }
}
```

### 3. Update Worker Status

**Request:**
```bash
PUT /worker/status
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "is_online": true,
    "current_lat": 40.7580,
    "current_lng": -73.9855
}
```

**Response:**
```json
{
    "success": true,
    "message": "Worker status updated successfully",
    "data": {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Jane Smith",
        "bio": "Master electrician specializing in residential and commercial wiring",
        "experience_years": 12,
        "is_verified": true,
        "rating": 4.5,
        "total_jobs": 150,
        "is_online": true,
        "current_lat": 40.7580,
        "current_lng": -73.9855,
        "last_active": "2024-01-01T16:00:00"
    }
}
```

### 4. Add Worker Skill

**Request:**
```bash
POST /worker/skills
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "skill_name": "Electrical Panel Installation",
    "experience_level": "expert"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Skill added successfully",
    "data": [
        {
            "id": "012f3456-e89b-12d3-a456-426614174003",
            "skill_name": "Electrical Panel Installation",
            "experience_level": "expert"
        }
    ]
}
```

### 5. Get Worker Skills

**Request:**
```bash
GET /worker/skills
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
    "success": true,
    "message": "Skills retrieved successfully",
    "data": [
        {
            "id": "456e7890-e89b-12d3-a456-426614174001",
            "skill_name": "Electrical Wiring",
            "experience_level": "expert"
        },
        {
            "id": "789e0123-e89b-12d3-a456-426614174002",
            "skill_name": "Circuit Breaker Installation",
            "experience_level": "advanced"
        },
        {
            "id": "012f3456-e89b-12d3-a456-426614174003",
            "skill_name": "Electrical Panel Installation",
            "experience_level": "expert"
        }
    ]
}
```

## Error Responses

### Invalid OTP
```json
{
    "detail": "Invalid OTP"
}
```

### Unauthorized Access
```json
{
    "detail": "Could not validate credentials"
}
```

### Insufficient Permissions
```json
{
    "detail": "Not enough permissions"
}
```

### Profile Not Found
```json
{
    "detail": "Worker profile not found"
}
```

### Validation Error
```json
{
    "detail": [
        {
            "loc": ["body", "phone"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

## Testing with curl

### Complete Flow Example

```bash
# 1. Send OTP
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

# 2. Verify OTP and get token (note the OTP from console)
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "otp": "123456", "role": "customer"}'

# 3. Extract token from response and use it
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 4. Get user profile
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 5. Update profile
curl -X PUT "http://localhost:8000/customer/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```
