from fastapi import APIRouter

router = APIRouter(prefix="/aiops")


@router.get("/status")
def aiops_status():
    return {
        "aiops": "operational"
    }
