from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI(title="API Gateway", version="1.0.0")
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

INCIDENT_SERVICE_URL = os.getenv("INCIDENT_SERVICE_URL", "http://incident-service:8000")
HEALTH_SERVICE_URL = os.getenv("HEALTH_SERVICE_URL", "http://health-service:8001")


@app.get("/health")
async def gateway_health():
    return {"status": "ok", "service": "api-gateway"}


@app.api_route("/api/incidents/{path:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def proxy_incidents(path: str, request: Request):
    url = f"{INCIDENT_SERVICE_URL}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=await request.body(),
            params=request.query_params,
        )
    return response.json()


@app.api_route("/api/health/{path:path}", methods=["GET"])
async def proxy_health(path: str, request: Request):
    url = f"{HEALTH_SERVICE_URL}/{path}"
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            params=request.query_params,
        )
    return response.json()
