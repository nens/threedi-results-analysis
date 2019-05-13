"""Monkeypatch sys.excepthook with one that logs the exception."""
import logging
import sys


root_logger = logging.getLogger("")


original_excepthook = sys.excepthook


def _excepthook_with_logging(exc_type, exc_value, exc_traceback):
    root_logger.error(
        "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
    )
    return original_excepthook(exc_type, exc_value, exc_traceback)


sys.excepthook = _excepthook_with_logging
