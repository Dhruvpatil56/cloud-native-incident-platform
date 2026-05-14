import asyncio
import json
import nats
import traceback

from analyzer import analyze_incident
from metrics import AIOPS_INCIDENTS_ANALYZED_TOTAL, AIOPS_ANALYSIS_FAILURES_TOTAL


async def start_consumer():
    try:
        nc = await nats.connect("nats://nats:4222")
        print("AIOps consumer connected to NATS")

        async def handler(msg):
            try:
                print(f"[AIOPS] Received message on {msg.subject}")
                data = json.loads(msg.data.decode())
                print(f"[AIOPS] Processing: {data}")
                analysis = await analyze_incident(data)
                AIOPS_INCIDENTS_ANALYZED_TOTAL.inc()
                print(f"\n===== AI INCIDENT ANALYSIS =====\n")
                print(analysis)
                print("\n================================\n")
            except Exception as e:
                AIOPS_ANALYSIS_FAILURES_TOTAL.inc()
                print(f"[AIOPS] Handler error: {e}")
                traceback.print_exc()

        await nc.subscribe("signals.alerts", cb=handler)
        print("AIOps consumer listening on signals.alerts...")

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"[AIOPS] Consumer startup error: {e}")
        traceback.print_exc()
