FROM python:3.12-slim

WORKDIR /app

# Install only the core requirements
RUN pip install --no-cache-dir fastapi uvicorn setuptools==70.0.0

# Copy service code
COPY . .

# Ensure Python looks at the root for modules
ENV PYTHONPATH=/app

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
