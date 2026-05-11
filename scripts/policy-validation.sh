#!/bin/bash

set -e

kubectl get clusterpolicies

kubectl describe clusterpolicy restrict-latest-tag

kubectl describe clusterpolicy require-resource-limits

kubectl describe clusterpolicy block-privileged
