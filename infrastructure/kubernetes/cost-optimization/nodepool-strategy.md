# Node Pool Cost Optimization Strategy

## Goals
- Keep production reliability high.
- Minimize overprovisioned capacity.
- Maintain headroom for burst traffic.

## Strategy
1. Keep separate node groups for critical services and system workloads.
2. Enable cluster autoscaler with auto-discovery tags.
3. Use right-sized requests/limits as baseline capacity signals.
4. Prefer scale-down stability windows to avoid thrashing.
5. Track node utilization and adjust min/max nodes monthly.

## Guardrails
- Never set min nodes to zero for critical production workloads.
- Review SLO impact before lowering requests/limits.
- Monitor autoscaling events via Grafana and Alertmanager.
