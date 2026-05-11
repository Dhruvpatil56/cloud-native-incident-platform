#!/bin/bash

set -e

TAG=${CI_COMMIT_SHA}

cd infrastructure/kubernetes/overlays/prod

kustomize edit set image order-service=${ECR_REGISTRY}/cloud-native-platform/order-service:${TAG}

kustomize edit set image auth-service=${ECR_REGISTRY}/cloud-native-platform/auth-service:${TAG}
