import os
import time
from groq import Groq

from prompts import INCIDENT_ANALYSIS_PROMPT
from metrics import AIOPS_ANALYSIS_DURATION_SECONDS, AIOPS_ANALYSIS_FAILURES_TOTAL


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def analyze_incident(incident: dict):

    prompt = INCIDENT_ANALYSIS_PROMPT.format(
        incident=incident
    )

    started = time.perf_counter()
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception:
        AIOPS_ANALYSIS_FAILURES_TOTAL.inc()
        raise
    finally:
        AIOPS_ANALYSIS_DURATION_SECONDS.observe(time.perf_counter() - started)
