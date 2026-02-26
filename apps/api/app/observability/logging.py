import json
import logging
from datetime import UTC, datetime
from typing import Any

_LOGGING_CONFIGURED = False


class JsonLogFormatter(logging.Formatter):
    _extra_fields = (
        "event_name",
        "workspace_id",
        "agent_id",
        "jti",
        "decision",
        "reason_code",
        "audit_event_id",
        "status",
        "checked_count",
        "broken_at_event_id",
        "path",
        "method",
    )

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for field in self._extra_fields:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging() -> None:
    global _LOGGING_CONFIGURED
    if _LOGGING_CONFIGURED:
        return

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonLogFormatter())
    root_logger.handlers = [handler]

    _LOGGING_CONFIGURED = True
