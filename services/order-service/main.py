import random
import time

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

logger = setup_logging("order-service")

provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

app = FastAPI(title="Order Service", version="1.0.0")
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(RequestIDMiddleware)

setup_metrics(app)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "order-service"}


@app.get("/orders")
async def list_orders():
    with tracer.start_as_current_span("list_orders"):

        if random.random() < 0.10:
            logger.warning("Slow request detected", extra={"trace_id": get_trace_id()})
            time.sleep(2)

        logger.info("Orders listed successfully", extra={"trace_id": get_trace_id()})

        return {
            "orders": [
                {"id": i, "status": "pending"}
                for i in range(5)
            ]
        }


@app.post("/orders")
async def create_order():
    with tracer.start_as_current_span("create_order"):

        if random.random() < 0.05:
            logger.error("Database timeout while creating order", extra={"trace_id": get_trace_id()})
            return {
                "status": "error",
                "message": "database timeout"
            }

        logger.info("Order created successfully", extra={"trace_id": get_trace_id()})

        return {
            "order_id": random.randint(1000, 9999),
            "status": "created"
        }
