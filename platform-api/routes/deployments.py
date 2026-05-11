from fastapi import APIRouter, Header

from audit.audit_logger import audit_event
from integrations.argocd import sync_application

router = APIRouter(prefix="/deployments")


@router.get("/")
def list_deployments():
    return {
        "status": "deployment visibility endpoint"
    }


@router.post("/sync")
def trigger_gitops_sync(x_actor: str = Header(default="unknown")):
    audit_event("deployments.sync.requested", x_actor)
    return {
        "status": "GitOps sync requested",
        "result": sync_application("platform-services"),
    }
