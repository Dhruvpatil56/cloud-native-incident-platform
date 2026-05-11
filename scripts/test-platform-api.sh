#!/bin/bash

set -e

curl http://localhost:8080/health

curl http://localhost:8080/deployments/

curl http://localhost:8080/incidents/

curl http://localhost:8080/observability/metrics

curl http://localhost:8080/aiops/status
