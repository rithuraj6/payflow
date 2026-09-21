from fastapi import FastAPI

from app.routes.payments import router as payments_router
from app.logging_config import configure_logging
from prometheus_fastapi_instrumentator import Instrumentator


configure_logging()

app = FastAPI(
    title="PayFlow Payment Platform",
    description="A production-style UPI payment processing platform",
    version="1.0.0",
)

app.include_router(payments_router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
def root():
    return {
        "service": "payflow-payment-service",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }