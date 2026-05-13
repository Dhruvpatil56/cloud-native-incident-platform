from fastapi import FastAPI, Request, Response
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

@app.api_route("/api/v1/incidents", methods=["GET", "POST"])
async def proxy_incidents_root(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=f"{INCIDENT_SERVICE_URL}/api/v1/incidents",
            headers=dict(request.headers),
            content=await request.body(),
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )

@app.api_route("/api/v1/incidents/{path:path}", methods=["GET", "POST", "PATCH", "DELETE"])
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

from prometheus_client import make_asgi_app
from starlette.routing import Mount

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

from prometheus_client import make_asgi_app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
