INCIDENT_ANALYSIS_PROMPT = """
You are an SRE incident analysis engine.

Analyze the following operational incident.

Provide:
1. Short summary
2. Possible root cause
3. Operational impact
4. Suggested remediation
5. Severity assessment

Incident:
{incident}
"""
