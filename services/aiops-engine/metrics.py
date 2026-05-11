from prometheus_client import Counter, Histogram, start_http_server

AIOPS_INCIDENTS_ANALYZED_TOTAL = Counter(
    "aiops_incidents_analyzed_total",
    "Total number of incidents analyzed by AIOps",
)

AIOPS_ANALYSIS_FAILURES_TOTAL = Counter(
    "aiops_analysis_failures_total",
    "Total number of failed AIOps analyses",
)

AIOPS_ANALYSIS_DURATION_SECONDS = Histogram(
    "aiops_analysis_duration_seconds",
    "Duration of AIOps incident analysis",
)


def start_metrics_server(port: int = 8010):
    start_http_server(port)
