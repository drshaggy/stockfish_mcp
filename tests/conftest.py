import pytest
import chess
from unittest.mock import Mock
from mocks.mock_stockfish import MockStockfishManager

@pytest.fixture
def event_loop_policy():
    """Configure asyncio for testing"""
    import asyncio
    return asyncio.get_event_loop_policy()

@pytest.fixture
def starting_position():
    """Standard chess starting position FEN"""
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@pytest.fixture
def sample_game_positions():
    """Common chess positions for testing"""
    return {
        "starting": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "after_e4": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        "sicilian": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
        "endgame": "8/8/8/8/8/8/4K3/4k3 w - - 0 1"
    }

@pytest.fixture
def invalid_fens():
    """Invalid FEN strings for negative testing"""
    return [
        "invalid_fen_string",
        "",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP",  # Missing game state entirely
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 extra",  # Extra data
        "rnbqkbnr/pppppppp/9/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Invalid rank (9 squares)
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR X KQkq - 0 1",  # Invalid turn
    ]

@pytest.fixture
def mock_manager():
    """Fixture providing a mock StockfishManager for all tests"""
    return MockStockfishManager()