import json
import logging
import sys


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        if hasattr(record, "event"):
            log_data["event"] = record.event

        if hasattr(record, "transaction_id"):
            log_data["transaction_id"] = record.transaction_id

        if hasattr(record, "order_id"):
            log_data["order_id"] = record.order_id

        if hasattr(record, "payment_channel"):
            log_data["payment_channel"] = record.payment_channel

        if hasattr(record, "amount"):
            log_data["amount"] = record.amount

        if hasattr(record, "status"):
            log_data["status"] = record.status

        return json.dumps(log_data)


def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logger = logging.getLogger("payflow")
    logger.setLevel(logging.INFO)

    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
