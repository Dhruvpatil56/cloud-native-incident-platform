#!/bin/bash

set -e

cosign verify ${ECR_REGISTRY}/cloud-native-platform/order-service:${CI_COMMIT_SHA}

cosign verify ${ECR_REGISTRY}/cloud-native-platform/auth-service:${CI_COMMIT_SHA}
