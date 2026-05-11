import asyncio
import random
import logging

import httpx

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

TARGETS = [
    "http://order-service:8002/orders",
    "http://auth-service:8003/health",
    "http://api-gateway:8080/api/health/services",
]


async def simulate():

    async with httpx.AsyncClient() as client:

        while True:

            target = random.choice(TARGETS)

            try:
                response = await client.get(target, timeout=5)

                logger.info(
                    f"[SIMULATOR] {target} -> {response.status_code}"
                )

            except Exception as e:
                logger.error(
                    f"[SIMULATOR] {target} -> ERROR: {e}"
                )

            await asyncio.sleep(random.uniform(0.5, 2.0))


if __name__ == "__main__":
    asyncio.run(simulate())
