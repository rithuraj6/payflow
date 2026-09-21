import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.services.payment_processor import PaymentResult, process_payment

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def unique_idempotency_key():
    return f"test-{uuid.uuid4()}"


def test_create_qr_payment():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": unique_idempotency_key(),
        },
        json={
            "order_id": "TEST-QR-001",
            "amount": 500.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "QR",
            "payee_vpa": "merchant@payflow",
            "bank_name": "HDFC Bank",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["order_id"] == "TEST-QR-001"
    assert data["amount"] == "500.00"
    assert data["payment_method"] == "UPI"
    assert data["payment_channel"] == "QR"
    assert data["payee_vpa"] == "merchant@payflow"
    assert data["status"] == "SUCCESS"


def test_qr_payment_requires_payee_vpa():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": unique_idempotency_key(),
        },
        json={
            "order_id": "TEST-QR-INVALID",
            "amount": 500.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "QR",
            "bank_name": "HDFC Bank",
        },
    )

    assert response.status_code == 422

    assert "payee_vpa is required for QR payments" in response.text


def test_create_vpa_payment():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": unique_idempotency_key(),
        },
        json={
            "order_id": "TEST-VPA-001",
            "amount": 750.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "VPA",
            "payer_vpa": "customer@payflow",
            "payee_vpa": "merchant@payflow",
            "bank_name": "ICICI Bank",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["payment_channel"] == "VPA"
    assert data["payer_vpa"] == "customer@payflow"
    assert data["payee_vpa"] == "merchant@payflow"


def test_create_pos_payment():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": unique_idempotency_key(),
        },
        json={
            "order_id": "TEST-POS-001",
            "amount": 1200.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "POS",
            "terminal_id": "POS-001",
            "bank_name": "SBI",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["payment_channel"] == "POS"
    assert data["terminal_id"] == "POS-001"


def test_idempotency_returns_same_transaction():
    idempotency_key = unique_idempotency_key()

    payment_data = {
        "order_id": "TEST-IDEMPOTENCY-001",
        "amount": 1500.00,
        "currency": "INR",
        "payment_method": "UPI",
        "payment_channel": "QR",
        "payee_vpa": "merchant@payflow",
        "bank_name": "HDFC Bank",
    }

    first_response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": idempotency_key,
        },
        json=payment_data,
    )

    second_response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": idempotency_key,
        },
        json=payment_data,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_data = first_response.json()
    second_data = second_response.json()

    assert (
        first_data["transaction_id"]
        == second_data["transaction_id"]
    )

def test_get_payment():
    idempotency_key = unique_idempotency_key()

    create_response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": idempotency_key,
        },
        json={
            "order_id": "TEST-GET-001",
            "amount": 1000.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "QR",
            "payee_vpa": "merchant@payflow",
            "bank_name": "HDFC Bank",
        },
    )

    assert create_response.status_code == 201

    transaction_id = create_response.json()["transaction_id"]

    get_response = client.get(
        f"/payments/{transaction_id}"
    )

    assert get_response.status_code == 200

    data = get_response.json()

    assert data["transaction_id"] == transaction_id
    assert data["order_id"] == "TEST-GET-001"
    assert data["amount"] == "1000.00"
    assert data["status"] == "SUCCESS"


def test_get_payment_not_found():
    response = client.get(
        "/payments/PAY-DOES-NOT-EXIST"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Payment not found"

def test_vpa_payment_requires_payer_vpa():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": unique_idempotency_key(),
        },
        json={
            "order_id": "TEST-VPA-INVALID",
            "amount": 750.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "VPA",
            "payee_vpa": "merchant@payflow",
        },
    )

    assert response.status_code == 422
    assert "payer_vpa is required for VPA payments" in response.text


def test_pos_payment_requires_terminal_id():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": unique_idempotency_key(),
        },
        json={
            "order_id": "TEST-POS-INVALID",
            "amount": 1200.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "POS",
        },
    )

    assert response.status_code == 422
    assert "terminal_id is required for POS payments" in response.text


def test_payment_processor_success():
    result = process_payment("SUCCESS")
    assert result == PaymentResult.SUCCESS


def test_payment_processor_failed():
    result = process_payment("FAILED")
    assert result == PaymentResult.FAILED


def test_payment_processor_timeout():
    result = process_payment("TIMEOUT")
    assert result == PaymentResult.TIMEOUT




def test_create_payment_failed():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": "api-failed-001",
            "X-Payment-Simulation": "FAILED",
        },
        json={
            "order_id": "ORD-API-FAILED-001",
            "amount": 500.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "QR",
            "payee_vpa": "merchant@upi",
            "bank_name": "Demo Bank",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "FAILED"


def test_create_payment_timeout():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": "api-timeout-001",
            "X-Payment-Simulation": "TIMEOUT",
        },
        json={
            "order_id": "ORD-API-TIMEOUT-001",
            "amount": 500.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "QR",
            "payee_vpa": "merchant@upi",
            "bank_name": "Demo Bank",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "TIMEOUT"


def test_create_payment_success_by_default():
    response = client.post(
        "/payments",
        headers={
            "Idempotency-Key": "api-success-default-001",
        },
        json={
            "order_id": "ORD-API-SUCCESS-001",
            "amount": 500.00,
            "currency": "INR",
            "payment_method": "UPI",
            "payment_channel": "QR",
            "payee_vpa": "merchant@upi",
            "bank_name": "Demo Bank",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "SUCCESS"