from fastapi import FastAPI

from routes.deployments import router as deployment_router
from routes.incidents import router as incident_router
from routes.services import router as service_router
from routes.observability import router as observability_router
from routes.aiops import router as aiops_router
from auth.middleware import APIKeyMiddleware


app = FastAPI(title="Platform API")
app.add_middleware(APIKeyMiddleware)

app.include_router(deployment_router)
app.include_router(incident_router)
app.include_router(service_router)
app.include_router(observability_router)
app.include_router(aiops_router)


@app.get("/health")
def health():
    return {"status": "ok"}
