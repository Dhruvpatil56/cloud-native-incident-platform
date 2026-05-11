from pathlib import Path

import yaml
from fastapi import APIRouter

router = APIRouter(prefix="/services")
CATALOG_PATH = Path("service-catalog/services.yaml")


@router.get("/")
def list_services():
    if not CATALOG_PATH.exists():
        return {"services": [], "status": "catalog missing"}
    data = yaml.safe_load(CATALOG_PATH.read_text(encoding="utf-8")) or {}
    return {"services": data.get("services", [])}
