from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

VERIFY_TOTAL = Counter(
    "kya_verify_total",
    "Total number of verify decisions",
    labelnames=("decision", "reason_code"),
)
VERIFY_LATENCY_SECONDS = Histogram(
    "kya_verify_latency_seconds",
    "Latency of verify endpoint in seconds",
)
AUDIT_INTEGRITY_TOTAL = Counter(
    "kya_audit_integrity_total",
    "Total number of audit integrity checks",
    labelnames=("status",),
)


def observe_verify(decision: str, reason_code: str | None, latency_seconds: float) -> None:
    VERIFY_TOTAL.labels(decision=decision, reason_code=reason_code or "NONE").inc()
    VERIFY_LATENCY_SECONDS.observe(latency_seconds)


def observe_audit_integrity(status: str) -> None:
    AUDIT_INTEGRITY_TOTAL.labels(status=status).inc()


def export_metrics_text() -> str:
    payload = generate_latest()
    return payload.decode("utf-8")


METRICS_CONTENT_TYPE = CONTENT_TYPE_LATEST
