# Buyscape on one small machine: the seller page, the back office and the
# engine, with the OCR models baked in so the first valuation is not slower
# than the rest. Any host that builds a Dockerfile can run it.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

# libgl and glib are what opencv-headless and onnxruntime still expect at
# import time on a slim image.
RUN apt-get update && apt-get install -y --no-install-recommends libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

COPY protocols ./protocols
COPY catalogue ./catalogue
COPY tenants ./tenants
COPY eval/prices ./eval/prices
COPY eval/adjudications.yaml ./eval/adjudications.yaml

# Fetch and check the OCR models now, not on the first seller.
RUN /app/.venv/bin/python -c "from rapidocr import RapidOCR; RapidOCR(params={'Global.log_level': 'warning'})"

# Never root: everything the app writes, sessions, recorded calls, the live
# price cache, lands under /app and is backed up to the Hub dataset.
RUN useradd -m -u 1000 user && mkdir -p /app/sessions /app/eval/fixtures && chown -R user:user /app
USER user
ENV BUYSCAPE_SESSIONS_DIR=/app/sessions
EXPOSE 8765
# Hosts hand the port in as PORT; 8765 when they do not.
CMD ["/bin/sh", "-c", "/app/.venv/bin/buyscape ui --host 0.0.0.0 --port ${PORT:-8765} --no-browser"]
