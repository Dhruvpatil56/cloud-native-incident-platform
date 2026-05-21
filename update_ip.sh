#!/bin/bash
read -p "Enter new EC2 IP: " NEW_IP

# Ensure the target directory exists
mkdir -p services/incident-service-ui

# SRE Best Practice: Write directly if it's missing, or update if it exists
echo "VITE_API_URL=http://$NEW_IP:8080" > services/incident-service-ui/.env

echo "Frontend IP successfully written to services/incident-service-ui/.env as http://$NEW_IP:8080"
