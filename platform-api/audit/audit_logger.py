import logging


logger = logging.getLogger("platform-audit")


def audit_event(action: str, actor: str):
    logger.info(
        f"AUDIT action={action} actor={actor}"
    )
