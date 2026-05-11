import asyncio
import json
import nats

from analyzer import analyze_incident
from metrics import AIOPS_INCIDENTS_ANALYZED_TOTAL, AIOPS_ANALYSIS_FAILURES_TOTAL


async def start_consumer():

    nc = await nats.connect("nats://nats:4222")

    async def handler(msg):

        data = json.loads(msg.data.decode())

        try:
            analysis = await analyze_incident(data)
            AIOPS_INCIDENTS_ANALYZED_TOTAL.inc()

            print(analysis)
            print("\n===============================\n")
        except Exception as e:
            AIOPS_ANALYSIS_FAILURES_TOTAL.inc()
            print(f"AIOps analysis failed: {e}")

    await nc.subscribe("incidents.created", cb=handler)

    print("AIOps consumer listening...")

    while True:
        await asyncio.sleep(1)
