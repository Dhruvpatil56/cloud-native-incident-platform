import json
import nats


async def publish_event(nc, subject: str, payload: dict):
    await nc.publish(subject, json.dumps(payload).encode())
