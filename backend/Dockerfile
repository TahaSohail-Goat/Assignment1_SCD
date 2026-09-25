# syntax=docker/dockerfile:1
# CivicPulse backend image (ASG-DEVOPS-001..007). Build context: backend/  (docker build backend)

# ---- builder: installs the pinned dependencies into a virtual environment --------------------
FROM python:3.12.14-slim-bookworm AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Requirements first, source later: this layer is rebuilt only when requirements.txt changes,
# so a source edit does not reinstall every dependency (ASG-DEVOPS-004).
COPY requirements.txt ./
RUN pip install -r requirements.txt

# ---- runtime: the venv and the source, no build tools, not root ----------------------------------
FROM python:3.12.14-slim-bookworm AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app

USER app
EXPOSE 8000

# The image has no curl; the interpreter is enough to ask the liveness probe.
HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

# Exec form: uvicorn is PID 1 and receives SIGTERM, so shutdown is graceful (ASG-NFR-008).
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
