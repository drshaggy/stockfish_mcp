"""
Simple logging setup for Stockfish MCP Server following MCP best practices.

Usage:
    from stockfish_mcp.logger import get_logger
    
    logger = get_logger(__name__)
    logger.info("Starting validation")
    logger.debug("FEN string received", extra={"fen_length": len(fen)})
    logger.error("Validation failed", extra={"error": str(e)})
"""

import logging
import sys
import re
from typing import Optional, Dict, Any


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive information in logs."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'msg') and record.msg:
            message = str(record.msg)
            # Mask API keys, tokens, etc.
            message = re.sub(r'(?i)(api[_-]?key|token|password|secret)["\s]*[:=]["\s]*([a-zA-Z0-9+/=]{8,})', 
                           r'\1: ***MASKED***', message)
            record.msg = message
        return True


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Get configured logger instance following MCP best practices.
    
    Args:
        name: Logger name (typically __name__)
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        
        # Formatter with context
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        handler.addFilter(SensitiveDataFilter())
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, level.upper()))
    
    return logger


def configure_logging(level: str = "INFO"):
    """Configure package-wide logging."""
    # Set root logger to avoid duplicate messages
    root = logging.getLogger()
    root.setLevel(logging.WARNING)
    
    # Configure our package logger
    logger = get_logger("stockfish_mcp", level)
    logger.info(f"Logging configured at {level} level")
    return logger