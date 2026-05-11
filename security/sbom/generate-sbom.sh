#!/bin/bash

set -e

mkdir -p sbom-output

syft packages docker:${ECR_REGISTRY}/cloud-native-platform/order-service:${CI_COMMIT_SHA} -o cyclonedx-json > sbom-output/order-service.json

syft packages docker:${ECR_REGISTRY}/cloud-native-platform/auth-service:${CI_COMMIT_SHA} -o cyclonedx-json > sbom-output/auth-service.json
