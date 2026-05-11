from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging

router = APIRouter(prefix="/webhook", tags=["webhook"])
logger = logging.getLogger(__name__)


class AlertLabel(BaseModel):
    alertname: Optional[str] = None
    severity: Optional[str] = "warning"
    service: Optional[str] = None


class AlertAnnotation(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None


class Alert(BaseModel):
    status: str
    labels: AlertLabel
    annotations: AlertAnnotation


class AlertmanagerPayload(BaseModel):
    alerts: List[Alert]


def map_severity(severity: str) -> str:
    mapping = {
        "critical": "critical",
        "warning": "high",
        "info": "low",
    }
    return mapping.get(severity.lower(), "medium")


@router.post("/alertmanager")
async def alertmanager_webhook(payload: AlertmanagerPayload):
    """
    Receives Alertmanager webhook payloads and auto-creates incidents.
    Alertmanager fires this when a Prometheus alert rule threshold is breached.
    """
    created = []
    for alert in payload.alerts:
        if alert.status != "firing":
            continue

        title = (
            alert.annotations.summary
            or alert.labels.alertname
            or "Unknown Alert"
        )
        severity = map_severity(alert.labels.severity or "warning")
        service = alert.labels.service or "unknown"

        logger.info(f"[WEBHOOK] Creating incident: {title} | severity={severity} | service={service}")

        # TODO: wire this to your actual incident creation logic
        # e.g. await create_incident(title=title, severity=severity)
        created.append({"title": title, "severity": severity, "service": service})

    return {"status": "received", "incidents_created": len(created), "details": created}
