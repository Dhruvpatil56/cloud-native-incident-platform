# Secrets Migration Strategy (Phase 8)

Current state:
- `.env` is used for local/dev convenience.

Target state:
- AWS Secrets Manager + External Secrets Operator (ESO).

Planned migration path:
1. Store runtime secrets in AWS Secrets Manager.
2. Install ESO in cluster and bind IAM roles for service accounts.
3. Define `ExternalSecret` manifests in Git for each service.
4. Remove direct secret env values from deployment manifests.
5. Keep only non-sensitive config in ConfigMaps.

Notes:
- Do not commit plaintext credentials to Git.
- Keep secrets access least-privileged by namespace and service.
