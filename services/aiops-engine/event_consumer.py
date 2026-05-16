import asyncio
import json
import nats
import httpx
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
                print(f"[AIOPS] Processing: {data.get('alertname', 'unknown')}")

                analysis = await analyze_incident(data)
                AIOPS_INCIDENTS_ANALYZED_TOTAL.inc()

                print(f"\n===== AI INCIDENT ANALYSIS =====\n")
                print(analysis)
                print("\n================================\n")

                # Store analysis back to incident if incident_id present
                incident_id = data.get("incident_id")
                if incident_id:
                    try:
                        async with httpx.AsyncClient() as client:
                            await client.patch(
                                f"http://incident-service:8000/api/v1/incidents/{incident_id}/ai-analysis",
                                json={"analysis": analysis},
                                timeout=10.0
                            )
                            print(f"[AIOPS] Analysis stored for incident {incident_id}")
                    except Exception as e:
                        print(f"[AIOPS] Failed to store analysis: {e}")

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
