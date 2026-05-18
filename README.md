# Cloud Native Incident & Observability Platform

A production-style DevOps/SRE platform designed for automated incident detection, response, and AI-driven analysis.

## Architecture

- **Incident Service**: Core IMS (FastAPI, PostgreSQL, Redis, NATS, MongoDB).
- **AIOps Engine**: AI-driven root cause analysis powered by **Groq LLM**.
- **Observability**: Full-stack monitoring via Prometheus, Grafana, Alertmanager, and OpenTelemetry.
- **API Gateway**: Central routing and security layer.

## Quick Start (Cloud/EC2 Setup)

When deploying on a fresh AWS/EC2 instance, follow these steps in order to set up your environment, configuration, and networking:

### 1. Create the Environment File
Always initialize your local configuration file from the template first:
```bash
cp .env.example .env
```

### 2. Initialize Secrets & AI Config
Run the initialization script to securely paste your Groq API key without exposing it to Git:
```bash
chmod +x init-env.sh
./init-env.sh
```

### 3. Update Public Connectivity
Map the frontend API URL to your current EC2 instance's Public IP:
```bash
chmod +x update_ip.sh
./update_ip.sh
```

### 4. Launch the Stack
Build and launch all services cleanly in detached mode:
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
