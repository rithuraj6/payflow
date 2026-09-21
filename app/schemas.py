from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class PaymentCreate(BaseModel):
    order_id: str = Field(min_length=1, max_length=50)

    amount: Decimal = Field(
        gt=0,
        decimal_places=2,
    )

    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
    )

    payment_method: Literal["UPI"] = "UPI"

    payment_channel: Literal["QR", "VPA", "POS"]

    payer_vpa: str | None = None

    payee_vpa: str | None = None

    bank_name: str | None = None

    terminal_id: str | None = None

    @model_validator(mode="after")
    def validate_payment_channel(self):
        if self.payment_channel == "QR":
            if not self.payee_vpa:
                raise ValueError(
                    "payee_vpa is required for QR payments"
                )

            if self.terminal_id:
                raise ValueError(
                    "terminal_id is not allowed for QR payments"
                )

        elif self.payment_channel == "VPA":
            if not self.payer_vpa:
                raise ValueError(
                    "payer_vpa is required for VPA payments"
                )

            if not self.payee_vpa:
                raise ValueError(
                    "payee_vpa is required for VPA payments"
                )

            if self.terminal_id:
                raise ValueError(
                    "terminal_id is not allowed for VPA payments"
                )

        elif self.payment_channel == "POS":
            if not self.terminal_id:
                raise ValueError(
                    "terminal_id is required for POS payments"
                )

            if self.payer_vpa:
                raise ValueError(
                    "payer_vpa is not allowed for POS payments"
                )

        return self

class PaymentResponse(BaseModel):
    transaction_id: str
    order_id: str
    amount: Decimal
    currency: str
    payment_method: str
    payment_channel: str
    payer_vpa: str | None
    payee_vpa: str | None
    bank_name: str | None
    terminal_id: str | None
    status: str
    payment_time: str | None