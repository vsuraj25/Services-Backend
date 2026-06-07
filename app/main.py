from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, customer, worker
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="A worker marketplace backend for electricians, mechanics, plumbers, etc.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(worker.router)


@app.get("/")
async def root():
    return {
        "message": "Worker Marketplace API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}