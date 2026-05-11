import json
import logging
import sys
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "service": getattr(record, "service", "unknown"),
            "request_id": getattr(record, "request_id", "unknown"),
            "trace_id": getattr(record, "trace_id", "unknown"),
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging(service_name: str):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    logger = logging.getLogger()
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    class ServiceFilter(logging.Filter):
        def filter(self, record):
            record.service = service_name
            return True

    logger.addFilter(ServiceFilter())

    return logger
