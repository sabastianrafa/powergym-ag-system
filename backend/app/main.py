from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, protected, customers, plans, subscriptions, payments, attendances, biometrics

app = FastAPI(
    title="PowerGym Management System",
    description="API for managing gym customers, subscriptions, payments, and attendances",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(protected.router, prefix="/api")
app.include_router(customers.router, prefix="/api")
app.include_router(plans.router, prefix="/api")
app.include_router(subscriptions.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(attendances.router, prefix="/api")
app.include_router(biometrics.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "PowerGym Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
