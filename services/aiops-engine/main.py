import asyncio

from fastapi import FastAPI

from event_consumer import start_consumer
from metrics import start_metrics_server

app = FastAPI(title="AIOps Engine", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    start_metrics_server(8010)
    asyncio.create_task(start_consumer())


@app.get("/health")
async def health():
    return {"status": "ok", "service": "aiops-engine"}
