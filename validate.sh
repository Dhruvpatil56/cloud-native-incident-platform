#!/bin/bash

# =====================================================
# FULL PLATFORM VALIDATION + HEALTH CHECK SCRIPT
# Cloud Native Incident & Observability Platform
# =====================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SERVER_IP=$(curl -s ifconfig.me || echo "localhost")
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="platform-validation-report-${TIMESTAMP}"

mkdir -p "$REPORT_DIR"

REPORT_FILE="$REPORT_DIR/platform-health-report.log"

log() {
  echo -e "$1" | tee -a "$REPORT_FILE"
}

section() {
  echo "" | tee -a "$REPORT_FILE"
  echo "====================================================" | tee -a "$REPORT_FILE"
  echo "$1" | tee -a "$REPORT_FILE"
  echo "====================================================" | tee -a "$REPORT_FILE"
}

check_service_health() {
  SERVICE_NAME=$1
  URL=$2

  echo "Checking $SERVICE_NAME -> $URL" | tee -a "$REPORT_FILE"

  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || true)

  if [ "$HTTP_CODE" = "200" ]; then
    log "${GREEN}[PASS]${NC} $SERVICE_NAME healthy"
  else
    log "${RED}[FAIL]${NC} $SERVICE_NAME unhealthy (HTTP $HTTP_CODE)"
  fi
}

section "DOCKER COMPOSE STATUS"

docker compose ps | tee "$REPORT_DIR/docker-compose-ps.log"
docker compose ps | tee -a "$REPORT_FILE"

section "CONTAINER HEALTH CHECK"

UNHEALTHY=$(docker compose ps --format json | grep -i "unhealthy\|exited\|restarting" || true)

if [ -z "$UNHEALTHY" ]; then
  log "${GREEN}[PASS]${NC} All containers healthy"
else
  log "${RED}[FAIL]${NC} Some containers unhealthy"
  echo "$UNHEALTHY" | tee -a "$REPORT_FILE"
fi

section "API HEALTH CHECKS"

check_service_health "Incident Service" "http://localhost:8000/health"
check_service_health "Health Service" "http://localhost:8001/health"
check_service_health "Order Service" "http://localhost:8002/health"
check_service_health "Auth Service" "http://localhost:8003/health"
check_service_health "AIOps Engine" "http://localhost:8005/health"
check_service_health "Platform API" "http://localhost:8081/health"

section "PROMETHEUS TARGET VALIDATION"

PROM_TARGETS=$(curl -s http://localhost:9090/api/v1/targets || true)

if echo "$PROM_TARGETS" | grep -q '"health":"up"'; then
  log "${GREEN}[PASS]${NC} Prometheus targets reachable"
else
  log "${RED}[FAIL]${NC} Prometheus targets issue detected"
fi

echo "$PROM_TARGETS" > "$REPORT_DIR/prometheus-targets.json"

section "GRAFANA VALIDATION"

GRAFANA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/login || true)

if [ "$GRAFANA_STATUS" = "200" ]; then
  log "${GREEN}[PASS]${NC} Grafana reachable"
else
  log "${RED}[FAIL]${NC} Grafana unreachable"
fi

section "TEMPO VALIDATION"

TEMPO_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3200/ready || true)

if [ "$TEMPO_STATUS" = "200" ]; then
  log "${GREEN}[PASS]${NC} Tempo operational"
else
  log "${RED}[FAIL]${NC} Tempo unhealthy"
fi

section "OTEL COLLECTOR VALIDATION"

OTEL_STATUS=$(docker compose logs otel-collector --tail=20 2>/dev/null || true)

echo "$OTEL_STATUS" > "$REPORT_DIR/otel-collector.log"

if echo "$OTEL_STATUS" | grep -qi "error"; then
  log "${YELLOW}[WARNING]${NC} OTEL collector logs contain warnings/errors"
else
  log "${GREEN}[PASS]${NC} OTEL collector stable"
fi

section "AIOPS ENGINE VALIDATION"

AIOPS_LOGS=$(docker compose logs aiops-engine --tail=50 2>/dev/null || true)

echo "$AIOPS_LOGS" > "$REPORT_DIR/aiops-engine.log"

if echo "$AIOPS_LOGS" | grep -qi "traceback\|error\|exception"; then
  log "${RED}[FAIL]${NC} AIOps engine errors detected"
else
  log "${GREEN}[PASS]${NC} AIOps engine healthy"
fi

section "NATS VALIDATION"

NATS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8222/varz || true)

if [ "$NATS_STATUS" = "200" ]; then
  log "${GREEN}[PASS]${NC} NATS operational"
else
  log "${RED}[FAIL]${NC} NATS unreachable"
fi

section "POSTGRES VALIDATION"

POSTGRES_HEALTH=$(docker inspect --format='{{json .State.Health.Status}}' platform-postgres 2>/dev/null || true)

if echo "$POSTGRES_HEALTH" | grep -qi "healthy"; then
  log "${GREEN}[PASS]${NC} PostgreSQL healthy"
else
  log "${RED}[FAIL]${NC} PostgreSQL unhealthy"
fi

section "REDIS VALIDATION"

REDIS_HEALTH=$(docker inspect --format='{{json .State.Health.Status}}' platform-redis 2>/dev/null || true)

if echo "$REDIS_HEALTH" | grep -qi "healthy"; then
  log "${GREEN}[PASS]${NC} Redis healthy"
else
  log "${RED}[FAIL]${NC} Redis unhealthy"
fi

section "TRACE GENERATION TEST"

for i in {1..20}
do
  curl -s http://localhost:8000/health > /dev/null || true
done

log "${GREEN}[PASS]${NC} Test traffic generated for Tempo"

section "RESOURCE UTILIZATION"

docker stats --no-stream | tee "$REPORT_DIR/docker-stats.log"
docker stats --no-stream | tee -a "$REPORT_FILE"

section "FAILED CONTAINER LOG COLLECTION"

CONTAINERS=$(docker ps -a --format '{{.Names}}')

for container in $CONTAINERS
 do
   docker logs "$container" --tail=100 > "$REPORT_DIR/${container}.log" 2>&1 || true
 done

log "${GREEN}[PASS]${NC} Container logs exported"

section "FINAL PLATFORM STATUS"

FAILED_COUNT=$(grep -c "\[FAIL\]" "$REPORT_FILE" || true)
WARNING_COUNT=$(grep -c "\[WARNING\]" "$REPORT_FILE" || true)

if [ "$FAILED_COUNT" -eq 0 ]; then
  log "${GREEN}PLATFORM STATUS: HEALTHY${NC}"
elif [ "$FAILED_COUNT" -lt 5 ]; then
  log "${YELLOW}PLATFORM STATUS: PARTIALLY HEALTHY${NC}"
else
  log "${RED}PLATFORM STATUS: UNSTABLE${NC}"
fi

log ""
log "Failure Count: $FAILED_COUNT"
log "Warning Count: $WARNING_COUNT"
log ""
log "Validation reports saved to: $REPORT_DIR"

section "VALIDATION COMPLETE"
