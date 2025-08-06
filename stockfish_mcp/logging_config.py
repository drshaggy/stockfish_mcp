"""
Logging configuration for Stockfish MCP Server.

This module provides centralized logging setup following MCP best practices:
- Structured logging with appropriate levels
- Sensitive information masking
- MCP context-aware logging
- Development vs production configurations
"""

import logging
import sys
from typing import Any, Dict, Optional
from functools import wraps
import re


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive information in log messages."""
    
    SENSITIVE_PATTERNS = [
        # API keys, tokens, passwords
        (r'(?i)(api[_-]?key|token|password|secret|auth)["\s]*[:=]["\s]*([a-zA-Z0-9+/=]{8,})', r'\1: ***MASKED***'),
        # FEN strings (might contain sensitive game data)
        (r'(?i)(fen)["\s]*[:=]["\s]*([a-zA-Z0-9/\s\-]{20,})', r'\1: ***FEN_MASKED***'),
        # Email addresses (if any)
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '***EMAIL_MASKED***'),
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Mask sensitive data in log record."""
        if hasattr(record, 'msg') and record.msg:
            message = str(record.msg)
            for pattern, replacement in self.SENSITIVE_PATTERNS:
                message = re.sub(pattern, replacement, message)
            record.msg = message
        return True


class MCPLogger:
    """MCP-aware logger with context support."""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self._setup_handlers()
        self._mcp_context = None
    
    def _setup_handlers(self):
        """Setup logging handlers with appropriate formatting."""
        if not self.logger.handlers:
            # Console handler for development
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            
            # Formatter with timestamp and context
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            console_handler.addFilter(SensitiveDataFilter())
            
            self.logger.addHandler(console_handler)
    
    def set_mcp_context(self, context):
        """Set MCP context for sending logs to clients."""
        self._mcp_context = context
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log debug message."""
        self.logger.debug(message, extra=extra or {})
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log info message."""
        self.logger.info(message, extra=extra or {})
        if self._mcp_context:
            # Send to MCP client if context available
            try:
                # Note: This would be implemented when you add MCP context support
                pass
            except Exception as e:
                self.logger.debug(f"Failed to send log to MCP client: {e}")
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log warning message."""
        self.logger.warning(message, extra=extra or {})
        if self._mcp_context:
            try:
                # Send to MCP client if context available
                pass
            except Exception as e:
                self.logger.debug(f"Failed to send warning to MCP client: {e}")
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None, exc_info: bool = False):
        """Log error message."""
        self.logger.error(message, extra=extra or {}, exc_info=exc_info)
        if self._mcp_context:
            try:
                # Send to MCP client if context available
                pass
            except Exception as e:
                self.logger.debug(f"Failed to send error to MCP client: {e}")
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """Log critical message."""
        self.logger.critical(message, extra=extra or {})


def get_logger(name: str, level: str = "INFO") -> MCPLogger:
    """Get or create an MCP-aware logger instance."""
    return MCPLogger(name, level)


def log_function_calls(logger: MCPLogger):
    """Decorator to log function entry/exit with timing."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            start_time = time.time()
            
            # Log function entry
            args_str = ', '.join([str(arg)[:100] for arg in args[1:]])  # Skip 'self'
            kwargs_str = ', '.join([f"{k}={str(v)[:100]}" for k, v in kwargs.items()])
            params = ', '.join(filter(None, [args_str, kwargs_str]))
            
            logger.debug(f"Entering {func.__name__}({params})")
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.debug(f"Exiting {func.__name__} (duration: {duration:.3f}s)")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Error in {func.__name__} after {duration:.3f}s: {e}", exc_info=True)
                raise
        
        return wrapper
    return decorator


# Global logger instance for the package
package_logger = get_logger("stockfish_mcp")


def configure_logging(level: str = "INFO", enable_debug: bool = False):
    """Configure package-wide logging settings."""
    global package_logger
    
    if enable_debug:
        level = "DEBUG"
    
    package_logger = get_logger("stockfish_mcp", level)
    
    # Configure root logger to avoid duplicate messages
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.setLevel(logging.WARNING)  # Only show warnings/errors from other packages
    
    package_logger.info(f"Logging configured at {level} level")
    return package_logger