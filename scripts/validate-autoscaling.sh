#!/bin/bash

set -e

kubectl get hpa -n platform

kubectl top pods -n platform

kubectl top nodes
