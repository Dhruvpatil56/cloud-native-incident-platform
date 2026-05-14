import asyncio
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from event_consumer import start_consumer


def run_consumer():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_consumer())


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=run_consumer, daemon=True)
    thread.start()
    print("[AIOPS] Consumer thread started")
    yield
    print("[AIOPS] Shutting down...")


app = FastAPI(title="AIOps Engine", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "aiops-engine"}
