#!/bin/bash

set -e

API_URL=${API_URL:-"http://localhost:8000/api/v1/incidents"}

echo ""
echo "=============================================="
echo " CLOUD NATIVE INCIDENT PLATFORM DEMO"
echo "=============================================="
echo ""

echo "1. Cleaning previous incidents..."
bash scripts/cleanup-incidents.sh

echo ""
echo "2. Triggering incident pipeline..."
bash scripts/fire-incident.sh

echo ""
echo "3. Fetching incidents..."
curl -s $API_URL | python3 -m json.tool

echo ""
echo "=============================================="
echo " DEMO COMPLETE"
echo "=============================================="
echo ""
echo "Flow demonstrated:"
echo "Alertmanager → Incident Service → PostgreSQL"
echo "→ NATS → AIOps Engine → AI Analysis"
echo ""
