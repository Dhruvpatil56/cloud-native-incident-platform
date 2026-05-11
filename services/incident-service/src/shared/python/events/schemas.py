from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IncidentEvent(BaseModel):
    event_type: str
    incident_id: str
    service: str
    severity: str
    message: str
    timestamp: datetime
    request_id: Optional[str] = None
