import random

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from shared.python.observability.logging_config import setup_logging
from shared.python.observability.middleware import RequestIDMiddleware
from shared.python.observability.metrics import setup_metrics
from observability.tracing.correlation import get_trace_id

logger = setup_logging("auth-service")

provider = TracerProvider()

processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
)

provider.add_span_processor(processor)

trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

app = FastAPI(title="Auth Service", version="1.0.0")
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(RequestIDMiddleware)

setup_metrics(app)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}


@app.post("/auth/login")
async def login():

    with tracer.start_as_current_span("login"):

        if random.random() < 0.08:
            logger.error("Authentication backend timeout", extra={"trace_id": get_trace_id()})

            return {
                "status": "error",
                "message": "authentication timeout"
            }

        logger.info("User authenticated successfully", extra={"trace_id": get_trace_id()})

        return {
            "token": "mock-jwt-token",
            "status": "success"
        }


@app.post("/auth/verify")
async def verify():

    with tracer.start_as_current_span("verify"):

        logger.info("Token verification completed", extra={"trace_id": get_trace_id()})

        return {
            "valid": True
        }
