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

def main():
    mcp.run()

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
    """Analyze a chess position"""
    board  = chess.Board(fen)
    return stockfish_manager.analyze_position(board)

@mcp.tool()
def get_best_move(fen: str):
    """Get the best move for a chess position"""
    board  = chess.Board(fen)
    return stockfish_manager.get_best_move(board).uci()


if __name__ == "__main__":
    main()