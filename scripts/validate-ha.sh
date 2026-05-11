#!/bin/bash

set -e

kubectl get pdb -n platform

kubectl get deployments -n platform -o wide
