#!/bin/bash
set -e

WEBHOOK_URL=${WEBHOOK_URL:-"http://localhost:8000/webhook/alertmanager"}
API_URL=${API_URL:-"http://localhost:8000/api/v1/incidents"}
WAIT_SECONDS=${WAIT_SECONDS:-20}

ALERTNAME="SmokeTest-$(date +%s)"
SERVICE="order-service"

echo "=== Firing test incident ==="
echo "Webhook URL: $WEBHOOK_URL"
echo "Alert name: $ALERTNAME"

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
        \"summary\": \"Smoke test alert for CI/CD pipeline validation\",
        \"description\": \"Automated smoke test to verify incident creation pipeline\"
      }
    }]
  }")

echo "Raw response: $RESPONSE"

ACTION=$(echo $RESPONSE | python3 -m json.tool 2>/dev/null | grep '"action"' | head -1)
echo "Action: $ACTION"

if echo "$ACTION" | grep -q "created"; then
    echo "✅ Incident created successfully"
    INCIDENT_ID=$(echo $RESPONSE | python3 -c "
import sys,json
data=json.load(sys.stdin)
print(data['details'][0].get('incident_id',''))
" 2>/dev/null)
    echo "Incident ID: $INCIDENT_ID"
else
    echo "❌ Incident creation failed"
    echo "Full response: $RESPONSE"
    exit 1
fi

echo "Waiting ${WAIT_SECONDS}s for AI analysis..."
sleep $WAIT_SECONDS

echo "=== Final incidents in DB ==="
curl -s "$API_URL" | python3 -m json.tool | grep -E "title|state|severity" || true

echo "=== Smoke test completed successfully ==="
