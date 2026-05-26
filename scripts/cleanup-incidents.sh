#!/bin/bash

set -e

echo "=== Cleaning incidents ==="

kubectl exec -n platform deployment/postgres -- \
psql -U incident -d incidents \
-c "DELETE FROM incidents;" || true

kubectl exec -n platform deployment/redis -- \
redis-cli FLUSHALL || true

echo "✅ Cleanup completed"
