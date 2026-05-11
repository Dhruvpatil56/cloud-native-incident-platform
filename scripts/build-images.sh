#!/bin/bash

set -e

SERVICES=(
  incident-service
  api-gateway
  health-service
  order-service
  auth-service
)

for SERVICE in "${SERVICES[@]}"
do
  echo "Building ${SERVICE}"

  docker build     -t ${ECR_REGISTRY}/cloud-native-platform/${SERVICE}:${CI_COMMIT_SHA}     -t ${ECR_REGISTRY}/cloud-native-platform/${SERVICE}:latest     ./services/${SERVICE}
done
