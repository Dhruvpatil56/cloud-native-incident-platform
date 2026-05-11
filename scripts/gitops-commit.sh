#!/bin/bash

set -e

git config --global user.email "gitlab-ci@platform.local"
git config --global user.name "gitlab-ci"

git add infrastructure/kubernetes/overlays/

git commit -m "gitops: update image tags ${CI_COMMIT_SHA}"

git push origin main
