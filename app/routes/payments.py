import uuid
from datetime import datetime, timezone
from app.services.payment_processor import process_payment
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
import logging,time
from app.database import get_db
from app.models import Payment
from app.schemas import PaymentCreate, PaymentResponse
import json
from app.redis_client import redis_client
from app.metrics import (
    payments_total,
    payment_processing_duration,
    cache_hits_total,
    cache_misses_total,

)
from sqlalchemy.exc import IntegrityError







logger = logging.getLogger("payflow")

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)


def create_payment(
    payment: PaymentCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    simulation: str = Header("SUCCESS", alias="X-Payment-Simulation"),
    db: Session = Depends(get_db),
):
    start_time = time.perf_counter()
    existing_payment = (
        db.query(Payment)
        .filter(Payment.idempotency_key == idempotency_key)
        .first()
    )

    if existing_payment:
        return PaymentResponse(
            transaction_id=existing_payment.transaction_id,
            order_id=existing_payment.order_id,
            amount=existing_payment.amount,
            currency=existing_payment.currency,
            payment_method=existing_payment.payment_method,
            payment_channel=existing_payment.payment_channel,
            payer_vpa=existing_payment.payer_vpa,
            payee_vpa=existing_payment.payee_vpa,
            bank_name=existing_payment.bank_name,
            terminal_id=existing_payment.terminal_id,
            status=existing_payment.status,
            payment_time=(
                existing_payment.payment_time.isoformat()
                if existing_payment.payment_time
                else None
            ),
        )

    transaction_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"

    payment_time = datetime.now(timezone.utc)

    payment_result = process_payment(simulation)

    new_payment = Payment(
      transaction_id=transaction_id,
      order_id=payment.order_id,
      amount=payment.amount,
      currency=payment.currency.upper(),
      payment_method=payment.payment_method,
      payment_channel=payment.payment_channel,
      payer_vpa=payment.payer_vpa,
      payee_vpa=payment.payee_vpa,
      bank_name=payment.bank_name,
      terminal_id=payment.terminal_id,
      status=payment_result.value,
      idempotency_key=idempotency_key,
      payment_time=payment_time,
)

    db.add(new_payment)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        existing_payment = (
            db.query(Payment)
            .filter(Payment.idempotency_key == idempotency_key)
            .first()
        )

        if existing_payment:
            return PaymentResponse(
                transaction_id=existing_payment.transaction_id,
                order_id=existing_payment.order_id,
                amount=existing_payment.amount,
                currency=existing_payment.currency,
                payment_method=existing_payment.payment_method,
                payment_channel=existing_payment.payment_channel,
                payer_vpa=existing_payment.payer_vpa,
                payee_vpa=existing_payment.payee_vpa,
                bank_name=existing_payment.bank_name,
                terminal_id=existing_payment.terminal_id,
                status=existing_payment.status,
                payment_time=(
                    existing_payment.payment_time.isoformat()
                    if existing_payment.payment_time
                    else None
                ),
            )

        raise
    duration_seconds = time.perf_counter() - start_time
    duration_ms = duration_seconds * 1000
    payments_total.labels(
    payment_channel=new_payment.payment_channel,
    status=new_payment.status,
    ).inc()

    payment_processing_duration.labels(
        payment_channel=new_payment.payment_channel,
    ).observe(duration_seconds)

    db.refresh(new_payment)
    logger.info(
        "Payment created successfully",
        extra={
            "event": "payment_created",
            "transaction_id": new_payment.transaction_id,
            "order_id": new_payment.order_id,
            "payment_channel": new_payment.payment_channel,
            "amount": str(new_payment.amount),
            "status": new_payment.status,
            "duration_ms": round(duration_ms, 2),
        },
    )

    return PaymentResponse(
        transaction_id=new_payment.transaction_id,
        order_id=new_payment.order_id,
        amount=new_payment.amount,
        currency=new_payment.currency,
        payment_method=new_payment.payment_method,
        payment_channel=new_payment.payment_channel,
        payer_vpa=new_payment.payer_vpa,
        payee_vpa=new_payment.payee_vpa,
        bank_name=new_payment.bank_name,
        terminal_id=new_payment.terminal_id,
        status=new_payment.status,
        payment_time=new_payment.payment_time.isoformat(),
    )

@router.get("/{transaction_id}", response_model=PaymentResponse)
def get_payment(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    cache_key = f"payment:{transaction_id}"


    cached_payment = redis_client.get(cache_key)

    if cached_payment:
        cache_hits_total.inc()

        logger.info(
            "Payment cache hit",
            extra={
                "event": "payment_cache_hit",
                "transaction_id": transaction_id,
            },
        )

        return PaymentResponse(**json.loads(cached_payment))

   
    cache_misses_total.inc()

    logger.info(
        "Payment cache miss",
        extra={
            "event": "payment_cache_miss",
            "transaction_id": transaction_id,
        },
    )

    payment = (
        db.query(Payment)
        .filter(Payment.transaction_id == transaction_id)
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    response = PaymentResponse(
        transaction_id=payment.transaction_id,
        order_id=payment.order_id,
        amount=payment.amount,
        currency=payment.currency,
        payment_method=payment.payment_method,
        payment_channel=payment.payment_channel,
        payer_vpa=payment.payer_vpa,
        payee_vpa=payment.payee_vpa,
        bank_name=payment.bank_name,
        terminal_id=payment.terminal_id,
        status=payment.status,
        payment_time=(
            payment.payment_time.isoformat()
            if payment.payment_time
            else None
        ),
    )

  
    redis_client.set(
        cache_key,
        response.model_dump_json(),
        ex=300,
    )

    return response