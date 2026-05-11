# Cloud Native Incident & Observability Platform

A production-style DevOps/SRE platform that monitors, detects, and responds to incidents
in cloud-native environments.

## Architecture

- **Incident Service** - Core IMS with state machine, RCA, MTTR (FastAPI + PostgreSQL + Redis + NATS + MongoDB)
- **API Gateway** - Central routing layer (FastAPI)
- **Health Service** - Cluster and service health (FastAPI)
- **Observability** - Prometheus + Grafana + Loki + Alertmanager + OpenTelemetry
- **Frontend** - React operational dashboard

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

## Service URLs (local)

| Service          | URL                   |
| ---------------- | --------------------- |
| API Gateway      | http://localhost:8080 |
| Incident Service | http://localhost:8000 |
| Health Service   | http://localhost:8001 |
| Frontend         | http://localhost:5173 |
| Grafana          | http://localhost:3000 |
| Prometheus       | http://localhost:9090 |
| Alertmanager     | http://localhost:9093 |
| Loki             | http://localhost:3100 |

## Related Projects

- [Incident Management System](https://github.com/Dhruvpatil56/incident-management-system) - The core IMS engine this platform is built around
