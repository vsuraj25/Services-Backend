from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routes import auth, customer, worker
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="A worker marketplace backend for electricians, mechanics, plumbers, etc.",
    version="1.0.0"
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
