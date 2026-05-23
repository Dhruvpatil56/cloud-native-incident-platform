#!/bin/bash
set -e

echo "=== CNIP Platform Startup ==="

# Step 1 - Update IP
read -p "Enter EC2 public IP: " IP
echo "VITE_API_URL=http://$IP:8080" > services/incident-service-ui/.env
echo "Frontend IP updated to $IP"

# Step 2 - Rebuild and push frontend

# Step 3 - Deploy full stack
echo "Deploying to Kind cluster..."

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl apply -f infrastructure/kubernetes/namespaces.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

kubectl apply -f infrastructure/kubernetes/base/databases.yaml
kubectl wait --for=condition=ready pod -l app=postgres -n platform --timeout=60s
kubectl wait --for=condition=ready pod -l app=redis -n platform --timeout=60s

kubectl delete job db-migration -n platform 2>/dev/null || true
sleep 2
kubectl apply -f infrastructure/kubernetes/base/db-migration-job.yaml
kubectl wait --for=condition=complete job/db-migration -n platform --timeout=60s

kubectl apply -f infrastructure/kubernetes/base/services/incident-service.yaml
kubectl apply -f infrastructure/kubernetes/base/services/api-gateway.yaml
kubectl apply -f infrastructure/kubernetes/base/services/health-service.yaml
kubectl apply -f infrastructure/kubernetes/base/services/frontend.yaml
kubectl apply -f infrastructure/kubernetes/base/services/order-service.yaml
kubectl apply -f infrastructure/kubernetes/base/services/auth-service.yaml
kubectl apply -f infrastructure/kubernetes/base/services/aiops-engine.yaml

kubectl apply -f infrastructure/kubernetes/base/observability/prometheus.yaml
kubectl apply -f infrastructure/kubernetes/base/observability/grafana.yaml
kubectl apply -f infrastructure/kubernetes/base/observability/loki.yaml
kubectl apply -f infrastructure/kubernetes/base/observability/alertmanager.yaml

kubectl apply -f infrastructure/kubernetes/base/services/nodeport.yaml

kubectl create configmap grafana-dashboards \
  --from-file=observability/grafana/dashboards/ \
  -n observability \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl rollout restart deployment/grafana -n observability

# kube-state-metrics
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kube-state-metrics/main/examples/standard/cluster-role.yaml 2>/dev/null || true
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kube-state-metrics/main/examples/standard/cluster-role-binding.yaml 2>/dev/null || true
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kube-state-metrics/main/examples/standard/service-account.yaml 2>/dev/null || true
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kube-state-metrics/main/examples/standard/deployment.yaml 2>/dev/null || true
kubectl apply -f https://raw.githubusercontent.com/kubernetes/kube-state-metrics/main/examples/standard/service.yaml 2>/dev/null || true

# Step 4 - Port forwards
echo "Starting port forwards..."
pkill -f "kubectl port-forward" 2>/dev/null || true
sudo fuser -k 5173/tcp 8080/tcp 3000/tcp 9090/tcp 9093/tcp 8000/tcp 2>/dev/null || true
sleep 2

kubectl port-forward -n platform svc/frontend-nodeport 5173:5173 --address 0.0.0.0 &
kubectl port-forward -n platform svc/api-gateway-nodeport 8080:8080 --address 0.0.0.0 &
kubectl port-forward -n platform svc/incident-service 8000:8000 --address 0.0.0.0 &
kubectl port-forward -n observability svc/grafana-nodeport 3000:3000 --address 0.0.0.0 &
kubectl port-forward -n observability svc/prometheus-nodeport 9090:9090 --address 0.0.0.0 &
kubectl port-forward -n observability svc/alertmanager-nodeport 9093:9093 --address 0.0.0.0 &
sleep 3

# Step 5 - Update Groq key
GROQ_KEY=$(grep GROQ_API_KEY .env | cut -d= -f2)
if [ -z "$GROQ_KEY" ]; then
    echo "WARNING: GROQ_API_KEY is empty in .env - AI features will not work"
else
    kubectl create secret generic aiops-secrets \
      --from-literal=GROQ_API_KEY=$GROQ_KEY \
      -n platform \
      --dry-run=client -o yaml | kubectl apply -f -
    kubectl rollout restart deployment/aiops-engine -n platform
fi

echo ""
echo "=== Status ==="
kubectl get pods -n platform
kubectl get pods -n observability

echo ""
echo "=== Access URLs ==="
echo "Frontend:     http://$IP:5173"
echo "API Gateway:  http://$IP:8080"
echo "Grafana:      http://$IP:3000"
echo "Prometheus:   http://$IP:9090"
echo "Alertmanager: http://$IP:9093"
echo ""
echo "=== CNIP Platform Ready ==="
