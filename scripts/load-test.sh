#!/bin/bash

set -e

hey -n 10000 -c 100 http://localhost:8000/orders
