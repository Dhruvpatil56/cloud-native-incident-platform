from fastapi import APIRouter

from integrations.grafana import dashboard_status
from integrations.prometheus import prometheus_status

router = APIRouter(prefix="/observability")


@router.get("/metrics")
def metrics_status():
    return {
        "prometheus": prometheus_status().get("prometheus", "unknown"),
        "grafana": dashboard_status().get("grafana", "unknown"),
        "tempo": "connected",
        "loki": "connected"
    }
