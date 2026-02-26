from fastapi import APIRouter, Response

from app.observability.metrics import METRICS_CONTENT_TYPE, export_metrics_text

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
def metrics_endpoint() -> Response:
    return Response(content=export_metrics_text(), media_type=METRICS_CONTENT_TYPE)
