#!/bin/bash

set -e

curl http://localhost:3200/ready

kubectl get pods -n observability

echo "Tempo operational"
