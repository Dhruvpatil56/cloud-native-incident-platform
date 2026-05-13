# Cloud Native Incident & Observability Platform

A production-style DevOps/SRE platform designed for automated incident detection, response, and AI-driven analysis.

## Architecture

- **Incident Service**: Core IMS (FastAPI, PostgreSQL, Redis, NATS, MongoDB).
- **AIOps Engine**: AI-driven root cause analysis powered by **Groq LLM**.
- **Observability**: Full-stack monitoring via Prometheus, Grafana, Alertmanager, and OpenTelemetry.
- **API Gateway**: Central routing and security layer.

## Quick Start (Cloud/EC2 Setup)

For a fresh deployment on AWS/EC2, use the provided automation scripts to handle secrets and networking:

### 1. Initialize Environment & Secrets
This script creates your `.env` from the template and securely prompts for your AI keys.
```bash
chmod +x init-env.sh
./init-env.sh
```

### 2. Update Public Connectivity
Map the frontend to your current EC2 Public IP:
```bash
chmod +x update_ip.sh
./update_ip.sh
```

### 3. Launch the Stack
```bash
docker compose up --build -d
```

## Service Access (AWS Deployment)

| Service           | Port   | External URL Example             |
| ----------------- | ------ | -------------------------------- |
| **Frontend UI** | 5173   | http://<EC2_PUBLIC_IP>:5173      |
| **API Gateway** | 8080   | http://<EC2_PUBLIC_IP>:8080      |
| **Grafana** | 3000   | http://<EC2_PUBLIC_IP>:3000      |
| **Prometheus** | 9090   | http://<EC2_PUBLIC_IP>:9090      |

---

## SRE Features
- **Blameless Postmortems**: Automated via the AIOps engine.
- **Reliability Metrics**: Real-time tracking of MTTR, MTTD, and MTTA.
- **Self-Healing**: Automated incident triage via NATS event bus.

## Related Projects
- [Incident Management System](https://github.com/Dhruvpatil56/incident-management-system) - The core IMS engine.
