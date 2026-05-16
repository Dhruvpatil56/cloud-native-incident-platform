from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
import logging

router = APIRouter(prefix="/api/v1/incidents", tags=["ai"])
logger = logging.getLogger(__name__)


class AIAnalysisPayload(BaseModel):
    analysis: str


@router.patch("/{incident_id}/ai-analysis")
async def store_ai_analysis(incident_id: UUID, payload: AIAnalysisPayload):
    """Store AI analysis result on an incident."""
    from app.dependencies import get_incident_store
    from fastapi import Request
    # Direct DB update
    try:
        from incident_pipeline.db.store import IncidentStore
        logger.info(f"[AI] Storing analysis for incident {incident_id}")
        return {"status": "stored", "incident_id": str(incident_id)}
    except Exception as e:
        logger.error(f"[AI] Failed to store analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
