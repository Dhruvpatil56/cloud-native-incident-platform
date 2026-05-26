#!/bin/bash

set -e

WEBHOOK_URL=${WEBHOOK_URL:-"http://localhost:8000/webhook/alertmanager"}
API_URL=${API_URL:-"http://localhost:8000/api/v1/incidents"}
WAIT_SECONDS=${WAIT_SECONDS:-20}

ALERTNAME="SmokeTest-$(date +%s)"
SERVICE="order-service"

echo "=== Firing test incident ==="

RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"alerts\": [{
      \"status\": \"firing\",
      \"labels\": {
        \"alertname\": \"$ALERTNAME\",
        \"severity\": \"critical\",
        \"service\": \"$SERVICE\"
      },
      \"annotations\": {
        \"summary\": \"Smoke test alert\",
        \"description\": \"CI/CD validation alert\"
      }
    }]
  }")

echo "$RESPONSE"

if echo "$RESPONSE" | grep -q "created"; then
    echo "✅ Incident created"
else
    echo "❌ Incident creation failed"
    exit 1
fi

echo "Waiting for AI analysis..."
sleep $WAIT_SECONDS

echo "=== Smoke test passed ==="
