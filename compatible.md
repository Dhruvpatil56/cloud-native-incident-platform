# MASTER PLATFORM COMPATIBILITY + VALIDATION + INTEGRATION AUDIT CONTEXT

# Cloud Native Incident & Observability Platform

# EXECUTE AFTER PHASE 13

# CRITICAL STABILITY VALIDATION PHASE

# DO NOT SKIP

---

# GOAL OF THIS VALIDATION PHASE

This is NOT another feature phase.

This is:

## full-platform compatibility verification

## integration auditing

## operational validation

## repository consistency validation

## configuration alignment verification

## dependency integrity validation

This phase exists because:
large platform projects eventually fail due to:

- config drift
- incompatible YAML
- broken Grafana JSON
- incorrect OTEL configs
- invalid Prometheus rules
- missing dependencies
- broken imports
- incompatible Docker Compose configs
- stale paths
- Kubernetes schema mismatches
- Argo CD sync failures
- Terraform inconsistencies
- service naming drift

This validation phase forces:

## complete repository-wide consistency auditing.

---

# IMPORTANT RULES

1. Codex MUST inspect ALL files recursively
2. Codex MUST validate ALL YAML files
3. Codex MUST validate ALL JSON files
4. Codex MUST validate ALL Dockerfiles
5. Codex MUST validate ALL Python imports
6. Codex MUST validate ALL Grafana dashboards
7. Codex MUST validate ALL Prometheus rules
8. Codex MUST validate ALL Kubernetes manifests
9. Codex MUST validate ALL Terraform syntax
10. Codex MUST generate COMPLETE validation logs

IMPORTANT:
DO NOT silently ignore broken files.

EVERY issue MUST be documented.

---

# PRIMARY GOAL

Codex must produce:

```text
FULL PLATFORM VALIDATION REPORT
```

including:

- passed validations
- failed validations
- warnings
- dependency mismatches
- invalid references
- missing files
- invalid schema
- incompatible APIs
- stale paths
- broken imports

---

# VALIDATION EXECUTION ORDER

Codex MUST validate in THIS exact order:

```text
1. Repository Structure
2. Docker Compose
3. Python Services
4. Kubernetes Manifests
5. Kustomize
6. Argo CD
7. Terraform
8. Prometheus
9. Alertmanager
10. Grafana
11. Loki
12. Tempo
13. OpenTelemetry
14. AI/AIOps Layer
15. GitLab CI
16. Security Stack
17. Chaos Engineering
18. Autoscaling
19. Platform APIs
20. Dependency Cross-Validation
```

DO NOT change validation order.

---

# TASK 1 — FULL REPOSITORY TREE AUDIT

Codex must recursively scan:

```text
cloud-native-incident-platform/
```

Generate:

```text
FULL_DIRECTORY_TREE.log
```

Requirements:

- every directory
- every file
- full paths
- missing expected files
- duplicate configs
- stale files

IMPORTANT:
Flag:

- duplicate manifests
- old configs
- deprecated files
- unused dashboards
- broken symlinks

---

# TASK 2 — DOCKER COMPOSE VALIDATION

Validate:

```text
docker-compose.yml
```

Codex must verify:

- valid YAML
- all services defined correctly
- valid volume mounts
- valid networks
- valid ports
- no duplicate ports
- no invalid depends_on
- valid image references
- valid build contexts

Generate:

```text
docker-compose-validation.log
```

IMPORTANT:
Detect:

- invalid Grafana provisioning mounts
- Tempo conflicts
- OTEL conflicts
- Loki path issues
- Prometheus mount mismatches

---

# TASK 3 — PYTHON IMPORT + DEPENDENCY VALIDATION

Recursively validate ALL:

```text
*.py
```

Requirements:

- missing imports
- circular imports
- invalid package names
- incompatible SDK usage
- syntax errors
- deprecated imports
- unresolved references

Validate:

- FastAPI services
- AI engine
- platform-api
- tracing middleware
- incident service

Generate:

```text
python-validation.log
```

IMPORTANT:
Verify:

- Groq SDK usage
- OpenTelemetry compatibility
- FastAPI compatibility
- requests/httpx compatibility

---

# TASK 4 — REQUIREMENTS.TXT VALIDATION

Validate ALL:

```text
requirements.txt
```

Requirements:

- conflicting versions
- missing packages
- incompatible OTEL packages
- incompatible FastAPI versions
- duplicate packages
- missing Grafana/Prometheus clients

Generate:

```text
requirements-validation.log
```

---

# TASK 5 — GRAFANA DASHBOARD VALIDATION

CRITICAL TASK.

Validate ALL:

```text
*.json
```

inside:

```text
observability/grafana/dashboards/
```

Requirements:

- valid JSON
- Grafana schema compatibility
- datasource references exist
- valid PromQL queries
- panel structure valid
- dashboard UID conflicts
- invalid templating
- invalid variables
- broken panels

Generate:

```text
grafana-dashboard-validation.log
```

IMPORTANT:
This task specifically exists because:
Grafana JSON commonly breaks.

Codex MUST:

- parse ALL JSON strictly
- validate against Grafana dashboard schema
- flag malformed panels
- flag missing datasource UIDs

---

# TASK 6 — PROMETHEUS RULE VALIDATION

Validate ALL:

```text
*.yml
```

inside:

```text
observability/prometheus/
```

Requirements:

- valid YAML
- valid PromQL
- valid alert syntax
- no duplicate alert names
- valid labels
- valid annotations
- no invalid metrics references

Generate:

```text
prometheus-validation.log
```

IMPORTANT:
Flag:

- nonexistent metrics
- invalid histogram_quantile usage
- invalid rate() usage
- malformed expressions

---

# TASK 7 — ALERTMANAGER VALIDATION

Validate:

- routes
- receivers
- grouping
- webhook configs
- email configs

Generate:

```text
alertmanager-validation.log
```

---

# TASK 8 — KUBERNETES MANIFEST VALIDATION

Validate recursively:

```text
*.yaml
*.yml
```

Requirements:

- Kubernetes schema validation
- valid apiVersion
- valid kinds
- valid selectors
- valid labels
- service/deployment matching
- ingress correctness
- HPA correctness
- RBAC correctness
- namespace consistency

Generate:

```text
kubernetes-validation.log
```

IMPORTANT:
Detect:

- selector mismatch
- service port mismatch
- duplicate resource names
- invalid namespace references
- invalid probes
- missing resource limits

---

# TASK 9 — KUSTOMIZE VALIDATION

Validate:

- overlays
- image overrides
- namespace overrides
- base references

Generate:

```text
kustomize-validation.log
```

IMPORTANT:
Verify:

- overlays/dev
- overlays/prod
- overlays/staging (if exists)

---

# TASK 10 — ARGO CD VALIDATION

Validate:

- Application manifests
- sync policies
- repo paths
- namespace references
- destination configs

Generate:

```text
argocd-validation.log
```

IMPORTANT:
Detect:

- broken repo paths
- invalid sync options
- invalid app references

---

# TASK 11 — TERRAFORM VALIDATION

Validate ALL:

```text
*.tf
```

Requirements:

- terraform validate
- formatting
- provider compatibility
- variable validation
- module references
- backend correctness

Generate:

```text
terraform-validation.log
```

IMPORTANT:
Flag:

- old AWS account IDs
- invalid provider versions
- deprecated syntax
- broken module paths

---

# TASK 12 — OPENTELEMETRY VALIDATION

Validate:

- OTEL Collector config
- exporter compatibility
- Tempo endpoints
- trace pipeline configs
- SDK instrumentation

Generate:

```text
otel-validation.log
```

IMPORTANT:
Verify:

- OTLP ports
- exporter endpoints
- tracing middleware correctness

---

# TASK 13 — TEMPO + LOKI VALIDATION

Validate:

- datasource connectivity
- Grafana integration
- ports
- storage paths
- retention configs

Generate:

```text
tempo-loki-validation.log
```

---

# TASK 14 — AI/AIOPS VALIDATION

Validate:

- Groq integration
- model configs
- async processing
- NATS integration
- trace-aware incident enrichment
- AI response parsing

Generate:

```text
aiops-validation.log
```

IMPORTANT:
Detect:

- OpenAI leftovers
- invalid Groq usage
- stale model references

---

# TASK 15 — GITLAB CI VALIDATION

Validate:

```text
.gitlab-ci.yml
```

Requirements:

- valid stages
- valid dependencies
- valid variables
- valid image references
- valid shell syntax

Generate:

```text
gitlab-ci-validation.log
```

IMPORTANT:
Detect:

- broken stages
- duplicate jobs
- invalid artifact references
- invalid script blocks

---

# TASK 16 — SECURITY STACK VALIDATION

Validate:

- Kyverno policies
- Falco rules
- Trivy configs
- Cosign workflows

Generate:

```text
security-validation.log
```

IMPORTANT:
Detect:

- malformed policies
- invalid Falco syntax
- broken Trivy config

---

# TASK 17 — CHAOS ENGINEERING VALIDATION

Validate:

- Litmus manifests
- chaos experiments
- rollback scripts

Generate:

```text
chaos-validation.log
```

---

# TASK 18 — AUTOSCALING VALIDATION

Validate:

- HPA manifests
- metrics references
- autoscaler configs
- resource requests

Generate:

```text
autoscaling-validation.log
```

IMPORTANT:
Detect:

- invalid CPU metrics
- invalid memory metrics
- missing requests/limits

---

# TASK 19 — PLATFORM API VALIDATION

Validate:

- routes
- integrations
- API schemas
- Dockerfile
- service catalog references

Generate:

```text
platform-api-validation.log
```

---

# TASK 20 — CROSS-SYSTEM COMPATIBILITY VALIDATION

CRITICAL TASK.

Codex MUST validate:
ALL systems TOGETHER.

Requirements:

- Grafana datasource UIDs match
- Prometheus targets exist
- Tempo endpoints exist
- Loki endpoints exist
- OTEL endpoints exist
- service names consistent
- namespaces consistent
- ports consistent
- traces/logs/metrics correlation works

Generate:

```text
cross-system-validation.log
```

IMPORTANT:
This is the MOST IMPORTANT validation task.

---

# TASK 21 — GENERATE FINAL MASTER REPORT

Generate:

```text
MASTER_PLATFORM_VALIDATION_REPORT.md
```

Must contain:

## Repository Summary

- total files
- total manifests
- total dashboards
- total services

---

## Validation Results

For EACH validation category:

- PASS
- WARNING
- FAIL

---

## Critical Failures

List:

- blocking issues
- incompatible configs
- malformed JSON
- invalid manifests
- broken imports

---

## Warnings

List:

- deprecated configs
- stale paths
- duplicated configs
- weak defaults

---

## Compatibility Matrix

Validate:

- Grafana ↔ Prometheus
- Grafana ↔ Loki
- Grafana ↔ Tempo
- OTEL ↔ Tempo
- FastAPI ↔ OTEL
- GitLab ↔ ArgoCD
- Kubernetes ↔ HPA
- AI Engine ↔ Incidents
- AI Engine ↔ Traces

---

## Final Platform Status

Codex must produce:

```text
PLATFORM STATUS:
HEALTHY
PARTIALLY HEALTHY
UNSTABLE
BROKEN
```

with explanation.

---

# TASK 22 — GENERATE FIX SUGGESTIONS

Generate:

```text
RECOMMENDED_FIXES.md
```

Requirements:

- exact file paths
- exact issue
- exact recommended fix
- severity level

Severity:

- CRITICAL
- HIGH
- MEDIUM
- LOW

---

# TASK 23 — GENERATE SAFE EXECUTION ORDER

Generate:

```text
SAFE_PLATFORM_STARTUP_ORDER.md
```

Requirements:
Correct startup order for:

- observability stack
- Tempo
- OTEL
- Prometheus
- Grafana
- Loki
- services
- AI engine
- Argo CD

This avoids:

- dependency race conditions
- missing datasource errors
- startup timing failures

---

# FINAL INSTRUCTION TO CODEX

Codex MUST behave like:

```text
Senior Platform Reliability Auditor
```

NOT:

```text
Code generator
```

The goal is:

## repository-wide operational consistency verification

Codex must:

- inspect deeply
- validate strictly
- produce logs
- explain failures
- recommend fixes
- verify compatibility

NO silent assumptions allowed.
