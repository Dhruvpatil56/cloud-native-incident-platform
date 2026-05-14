from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import logging
import json

from app.dependencies import get_pipeline
from incident_pipeline.models import (
    Incident,
    IncidentState,
    Severity,
    RcaCategory,
)
from incident_pipeline.pipeline import IncidentPipeline

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
        "warning": Severity.p2,
        "info": Severity.p3,
    }
    return mapping.get(severity.lower(), Severity.p2)


@router.post("/alertmanager")
async def alertmanager_webhook(
    request: Request,
    payload: AlertmanagerPayload,
    pipeline: IncidentPipeline = Depends(get_pipeline)
):

    logger.info(f"[WEBHOOK] Payload received: {payload.dict()}")

    processed = []

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

        logger.info(
            f"[WEBHOOK] Processing alert: "
            f"title={title} severity={severity.value} service={service}"
        )

        incident = Incident(
            title=title,
            description=alert.annotations.description or title,
            severity=severity,
            component=service,
            source="alertmanager",
            root_cause="Pending investigation",
            rca_category=RcaCategory.unknown,
            rca_description="Auto-generated from Alertmanager webhook",
            state=IncidentState.open,
        )

        try:

            result = pipeline.process(incident)

            if result.incident:

                incident_payload = result.incident.model_dump(mode="json")

                await request.app.state.nats.publish(
                    "incidents.created",
                    json.dumps(incident_payload).encode()
                )

                logger.info(
                    f"[WEBHOOK] Published incident event to NATS: "
                    f"{result.incident.id}"
                )

                processed.append({
                    "title": title,
                    "action": "created",
                    "incident_id": str(result.incident.id),
                })

            else:

                logger.warning(
                    f"[WEBHOOK] Incident creation failed: "
                    f"{result.reason or result.errors}"
                )

                processed.append({
                    "title": title,
                    "action": result.reason or "failed",
                })

        except Exception as e:

            logger.exception(
                f"[WEBHOOK] Pipeline failure while processing "
                f"'{title}': {e}"
            )

            processed.append({
                "title": title,
                "action": "exception",
                "error": str(e),
            })

    return {
        "status": "received",
        "processed": len(processed),
        "details": processed,
    }
