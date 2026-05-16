from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging
import json

from incident_pipeline.models import Incident, RcaCategory, Severity
from incident_pipeline.pipeline import IncidentPipeline
from app.dependencies import get_pipeline

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


def map_severity(severity: str) -> Severity:
    mapping = {
        "critical": Severity.p0,
        "warning": Severity.p1,
        "info": Severity.p2,
    }
    return mapping.get(severity.lower(), Severity.p2)


@router.post("/alertmanager")
async def alertmanager_webhook(
    payload: AlertmanagerPayload,
    request: Request,
    pipeline: IncidentPipeline = Depends(get_pipeline),
):
    created = []

    for alert in payload.alerts:
        if alert.status != "firing":
            continue

        title = alert.annotations.summary or alert.labels.alertname or "Alert detected"
        description = alert.annotations.description or title
        severity = map_severity(alert.labels.severity or "warning")
        service = alert.labels.service or "platform"
        alertname = alert.labels.alertname or "alert"

        # Step 1 — Run incident pipeline first to get incident_id
        incident_id = None
        try:
            incident = Incident(
                title=title,
                description=description,
                source="alertmanager",
                root_cause=f"Alert triggered: {alertname} on {service}. Automated detection via Prometheus alerting rules.",
                rca_category=RcaCategory.dependency_failure,
                rca_description=f"Automated incident from Alertmanager. Alert: {alertname}. Service: {service}. Engineer investigation required to determine full root cause and apply fix.",
                severity=severity,
                component=service,
            )
            result = pipeline.process(incident)

            if result.status == 201 and result.incident:
                incident_id = str(result.incident.id)
                logger.info(f"[WEBHOOK] Incident created: {incident_id}")
                created.append({
                    "incident_id": incident_id,
                    "title": title,
                    "severity": severity.value,
                    "service": service,
                    "action": "created"
                })
            else:
                logger.info(f"[WEBHOOK] Skipped: {result.reason}")
                created.append({"title": title, "action": result.reason or "skipped"})

        except Exception as e:
            logger.error(f"[WEBHOOK] Pipeline error: {e}")
            created.append({"title": title, "action": "exception", "error": str(e)})

        # Step 2 — Publish raw signal to NATS with incident_id for AI
        try:
            nats = request.app.state.nats
            raw_signal = {
                "event_type": "alert.firing",
                "alertname": alertname,
                "severity": alert.labels.severity,
                "service": service,
                "summary": alert.annotations.summary,
                "description": description,
                "incident_id": incident_id,
            }
            await nats.publish("signals.alerts", json.dumps(raw_signal).encode())
            logger.info(f"[WEBHOOK] Published to NATS: {alertname}")
        except Exception as e:
            logger.warning(f"[WEBHOOK] NATS publish failed: {e}")

    return {"status": "received", "processed": len(created), "details": created}
