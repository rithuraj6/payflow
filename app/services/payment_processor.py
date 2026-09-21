from enum import Enum


class PaymentResult(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"


def process_payment(simulation: str = "SUCCESS") -> PaymentResult:
    """
    Simulate communication with an external payment processor.

    Supported outcomes:
    - SUCCESS
    - FAILED
    - TIMEOUT

    By default, payments succeed.
    """

    simulation = simulation.upper()

    if simulation == "FAILED":
        return PaymentResult.FAILED

    if simulation == "TIMEOUT":
        return PaymentResult.TIMEOUT

    return PaymentResult.SUCCESS