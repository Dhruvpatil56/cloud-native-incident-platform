#!/bin/bash

set -e

trivy image --exit-code 1 --severity CRITICAL,HIGH ${ECR_REGISTRY}/cloud-native-platform/order-service:${CI_COMMIT_SHA}
trivy image --exit-code 1 --severity CRITICAL,HIGH ${ECR_REGISTRY}/cloud-native-platform/auth-service:${CI_COMMIT_SHA}
