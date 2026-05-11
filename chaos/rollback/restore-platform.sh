#!/bin/bash

set -e

kubectl delete chaosengine --all -n litmus

kubectl rollout restart deployment/order-service -n platform
kubectl rollout restart deployment/auth-service -n platform
kubectl rollout restart deployment/health-service -n platform

kubectl get pods -n platform
