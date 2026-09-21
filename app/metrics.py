from prometheus_client import Counter, Histogram


payments_total = Counter(
    "payflow_payments_total",
    "Total number of payment processing attempts",
    ["payment_channel", "status"],
)


payment_processing_duration = Histogram(
    "payflow_payment_processing_duration_seconds",
    "Payment processing duration in seconds",
    ["payment_channel"],
)


cache_hits_total = Counter(
    "payflow_cache_hits_total",
    "Total number of payment cache hits",
)

cache_misses_total = Counter(
    "payflow_cache_misses_total",
    "Total number of payment cache misses",
)