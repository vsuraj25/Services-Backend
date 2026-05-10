# Worker Marketplace Backend

A FastAPI backend for a worker marketplace application similar to Rapido/Uber but for electricians, mechanics, plumbers, etc.

## Features

- **OTP-based Authentication**: Mobile number login with 6-digit OTP
- **JWT Token Management**: Secure token-based authentication
- **Role-based System**: Customer, Worker, and Admin roles
- **Profile Management**: Complete profile management for customers and workers
- **Worker Skills**: Add and manage worker skills and experience levels
- **Online Status**: Track worker availability and location
- **Clean Architecture**: Modular, scalable, and beginner-friendly code structure

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Reliable relational database
- **SQLAlchemy ORM**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Alembic**: Database migration tool

## Project Structure

```
app/
├── main.py                 # FastAPI app entry point
├── database.py             # Database connection setup
├── config.py               # Configuration settings
├── models/
│   ├── __init__.py
│   ├── user.py            # User, Customer, Worker models
│   └── skill.py           # WorkerSkill model
├── schemas/
│   ├── __init__.py
│   ├── auth.py            # Auth request/response schemas
│   ├── user.py            # User schemas
│   ├── customer.py        # Customer schemas
│   ├── worker.py          # Worker schemas
│   └── skill.py           # Skill schemas
├── routes/
│   ├── __init__.py
│   ├── auth.py            # Auth endpoints
│   ├── customer.py        # Customer endpoints
│   └── worker.py          # Worker endpoints
├── services/
│   ├── __init__.py
│   ├── auth.py            # Auth business logic
│   ├── user.py            # User management
│   └── otp.py             # OTP handling
└── utils/
    ├── __init__.py
    ├── jwt.py             # JWT token utilities
    └── security.py        # Security helpers
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Update the `.env` file with your database credentials:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Worker Marketplace
DEBUG=True
```

### 3. Database Setup

Create a PostgreSQL database and update the `DATABASE_URL` in your `.env` file.

### 4. Run Database Migrations

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/send-otp` - Send OTP to phone number
- `POST /auth/verify-otp` - Verify OTP and get access token
- `GET /auth/me` - Get current user information

### Customer

- `GET /customer/profile` - Get customer profile
- `PUT /customer/profile` - Update customer profile

### Worker

- `GET /worker/profile` - Get worker profile
- `PUT /worker/profile` - Update worker profile
- `PUT /worker/status` - Update worker online status and location
- `POST /worker/skills` - Add skill to worker profile
- `GET /worker/skills` - Get all worker skills

## Example API Usage

### 1. Send OTP

```bash
curl -X POST "http://localhost:8000/auth/send-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

### 2. Verify OTP and Login

```bash
curl -X POST "http://localhost:8000/auth/verify-otp" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "otp": "123456", "role": "customer"}'
```

### 3. Get User Profile

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Update Customer Profile

```bash
curl -X PUT "http://localhost:8000/customer/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
```

### 5. Add Worker Skill

```bash
curl -X POST "http://localhost:8000/worker/skills" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"skill_name": "Electrical Wiring", "experience_level": "expert"}'
```

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `phone` (String, Unique)
- `role` (String: customer/worker/admin)
- `is_active` (Boolean)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Customers Table
- `id` (UUID, Foreign Key to users)
- `name` (String)
- `email` (String)
- `default_address` (Text)
- `lat` (Double)
- `lng` (Double)

### Workers Table
- `id` (UUID, Foreign Key to users)
- `name` (String)
- `bio` (Text)
- `experience_years` (Integer)
- `is_verified` (Boolean)
- `rating` (Float)
- `total_jobs` (Integer)
- `is_online` (Boolean)
- `current_lat` (Double)
- `current_lng` (Double)
- `last_active` (Timestamp)

### Worker Skills Table
- `id` (UUID, Primary Key)
- `worker_id` (UUID, Foreign Key)
- `skill_name` (String)
- `experience_level` (String)

## Security Features

- JWT token-based authentication
- Role-based access control
- OTP verification with expiry
- Protected routes with role validation
- Token expiry management

## Development Notes

- OTP is printed to console for testing (in production, use SMS service)
- Simple in-memory OTP storage (use Redis for production)
- Clean error handling and response format
- Comprehensive API documentation
- Database migrations with Alembic

## Future Enhancements

- Redis for OTP storage
- Real-time notifications with WebSockets
- File upload for worker documents
- Rating and review system
- Job posting and matching
- Payment integration
- Geolocation-based worker search
