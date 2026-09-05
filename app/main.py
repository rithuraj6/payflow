from fastapi import FastAPI

app = FastAPI(
    title="PayFlow Payment Platform",
    description="A production-style payment processing platform",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/")
def root():
    return {
        "service": "payflow-payment-service",
        "version": "1.0.0",
    }