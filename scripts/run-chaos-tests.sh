#!/bin/bash

set -e

echo "Running pod delete experiment"
kubectl apply -f chaos/pod-delete/order-service-pod-delete.yaml

sleep 90

echo "Running network latency experiment"
kubectl apply -f chaos/network-delay/api-latency.yaml

sleep 90

echo "Running CPU stress experiment"
kubectl apply -f chaos/cpu-stress/auth-service-cpu.yaml

sleep 90

echo "Running memory stress experiment"
kubectl apply -f chaos/memory-stress/health-service-memory.yaml
