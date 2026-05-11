#!/bin/bash

set -e

cosign sign --yes ${ECR_REGISTRY}/cloud-native-platform/order-service:${CI_COMMIT_SHA}

cosign sign --yes ${ECR_REGISTRY}/cloud-native-platform/auth-service:${CI_COMMIT_SHA}
