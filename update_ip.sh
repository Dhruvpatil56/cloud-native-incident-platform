#!/bin/bash
read -p "Enter new EC2 IP: " NEW_IP
sed -i "s|VITE_API_URL=.*|VITE_API_URL=http://$NEW_IP:8080|" services/incident-service-ui/.env
echo "Frontend IP updated to $NEW_IP"
