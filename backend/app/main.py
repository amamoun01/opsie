import json
import logging
import time

from fastapi import FastAPI, Request, Response

from app.api import chat, health
from app.config import settings


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger("opsie.runtime")

app = FastAPI(
    title="Opsie AI Orchestration Engine",
    description="Asynchronous ChatOps backend optimizing multi-model LLM routing.",
    version="1.0.0",
)


@app.middleware("http")
async def operational_telemetry_middleware(request: Request, call_next) -> Response:
    """
    Intercepts all incoming HTTP payloads to log clean, structured metrics.
    """
    start_time = time.perf_counter()

    response = await call_next(request)

    execution_latency = (time.perf_counter() - start_time) * 1000

    telemetry_payload = {
        "timestamp": time.time(),
        "http_method": request.method,
        "request_path": request.url.path,
        "status_code": response.status_code,
        "latency_ms": round(execution_latency, 2),
        "client_host": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
    }

    logger.info(json.dumps(telemetry_payload))

    return response


app.include_router(health.router)
app.include_router(chat.router)
