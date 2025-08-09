"""Mock utilities for testing MCP server without external dependencies"""

from .mock_stockfish import MockStockfishManager, MockGameState

__all__ = ["MockStockfishManager", "MockGameState"]