FROM debian:trixie-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-requests curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv --system-site-packages /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir "django>=5.2,<5.3" "gunicorn==23.0.0"
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
RUN django-admin startproject hostile .
USER nobody
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "hostile.wsgi"]
