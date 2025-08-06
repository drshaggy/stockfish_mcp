from mcp.server.fastmcp import FastMCP
import chess
from stockfish_manager import StockfishManager as StockfishManager
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("Server started")
mcp = FastMCP("stockfish")
stockfish_manager = StockfishManager()

CHESS_API_BASE = 'https://chess-api.com/v1'


@mcp.tool()
def fen_validator(fen: str) -> bool:
    """Validate a FEN string"""
    try:
        chess.Board(fen)
        return True
    except ValueError:
        return False

@mcp.tool()
def analyze_position(fen: str):
    board  = chess.Board(fen)
    return stockfish_manager.analyze_position(board)
    