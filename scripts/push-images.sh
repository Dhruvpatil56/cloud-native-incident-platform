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
  echo "Pushing ${SERVICE}"

  docker push ${ECR_REGISTRY}/cloud-native-platform/${SERVICE}:${CI_COMMIT_SHA}
  docker push ${ECR_REGISTRY}/cloud-native-platform/${SERVICE}:latest

done
