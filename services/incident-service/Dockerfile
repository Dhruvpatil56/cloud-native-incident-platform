FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir setuptools==70.0.0

COPY . .

RUN pip install --no-cache-dir -e .

# SET PYTHONPATH to the root so "src.app.shared" or "app.shared" is resolved relative to the package install
ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
