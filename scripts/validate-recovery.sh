#!/bin/bash

set -e

echo "Checking deployment health..."

kubectl get pods -n platform

kubectl rollout status deployment/order-service -n platform
kubectl rollout status deployment/auth-service -n platform
kubectl rollout status deployment/health-service -n platform

echo "Recovery validation completed"
