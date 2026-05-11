from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import datetime

app = FastAPI(title="Health Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: replace with real k8s client in Phase 2
MOCK_SERVICES = [
    {"name": "incident-service", "status": "healthy", "replicas": 2},
    {"name": "api-gateway", "status": "healthy", "replicas": 1},
    {"name": "health-service", "status": "healthy", "replicas": 1},
    {"name": "frontend", "status": "healthy", "replicas": 1},
]


@app.get("/health")
async def service_health():
    return {"status": "ok", "service": "health-service"}


@app.get("/health/cluster")
async def cluster_health():
    # TODO: replace with real EKS cluster health check in Phase 2
    return {
        "cluster": "cloud-native-platform",
        "status": "healthy",
        "nodes": 3,
        "pods_running": 12,
        "pods_pending": 0,
        "pods_failed": 0,
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }


@app.get("/health/services")
async def services_health():
    # TODO: replace with real k8s pod status in Phase 2
    services = []
    for svc in MOCK_SERVICES:
        services.append({
            **svc,
            "cpu_usage": f"{random.randint(10, 60)}%",
            "memory_usage": f"{random.randint(100, 500)}Mi",
            "uptime": "2d 4h 32m",
            "last_checked": datetime.datetime.utcnow().isoformat(),
        })
    return {"services": services, "total": len(services)}
