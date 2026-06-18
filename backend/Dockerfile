# =======================
#  Build & Dependencies
# =======================
FROM python:3.11-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# =======================
#  Runtime Execution
# =======================
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PATH=/home/opsie/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd -g 10001 opsie && \
    useradd -u 10001 -g opsie -m -s /sbin/nologin opsie

COPY --from=builder /root/.local /home/opsie/.local
COPY --chown=opsie:opsie ./app /app/app

USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--log-level", "info"]
