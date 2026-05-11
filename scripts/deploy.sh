#!/bin/bash

set -e

kubectl apply -f infrastructure/kubernetes/namespaces.yaml

kubectl apply -f infrastructure/kubernetes/services/

kubectl apply -f infrastructure/kubernetes/observability/

kubectl apply -f infrastructure/kubernetes/ingress/

kubectl rollout status deployment/incident-service -n platform
kubectl rollout status deployment/api-gateway -n platform
kubectl rollout status deployment/health-service -n platform
kubectl rollout status deployment/order-service -n platform
kubectl rollout status deployment/auth-service -n platform
