from fastapi import APIRouter

router = APIRouter(prefix="/incidents")


@router.get("/")
def list_incidents():
    return {
        "status": "incident listing endpoint"
    }


@router.get("/{incident_id}")
def get_incident(incident_id: str):
    return {
        "incident_id": incident_id
    }
