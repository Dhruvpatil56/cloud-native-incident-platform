curl -X POST http://localhost:8080/webhook/alertmanager \
  -H "Content-Type: application/json" \
  -d '{
    "alerts": [{
      "status": "firing",
      "labels": {
        "alertname": "HighCPUUsage",
        "severity": "critical",
        "service": "order-service"
      },
      "annotations": {
        "summary": "CPU above 90% on order-service",
        "description": "order-service CPU has been above 90% for 3 minutes on K8s cluster"
      }
    }]
  }'
echo ""
sleep 15
curl -s http://localhost:8080/api/v1/incidents | python3 -m json.tool | grep -E "title|ai_analysis|severity|state"
