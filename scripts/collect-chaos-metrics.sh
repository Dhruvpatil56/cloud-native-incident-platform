#!/bin/bash

set -e

mkdir -p reports/chaos-results

kubectl get pods -n platform > reports/chaos-results/pods.txt

kubectl get events -n platform > reports/chaos-results/events.txt

kubectl top pods -n platform > reports/chaos-results/resource-usage.txt
