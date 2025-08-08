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
    analysis = stockfish_manager.analyze_position(board)
    return {
          "best_move": analysis["pv"][0].uci(),
          "score": str(analysis["score"].relative),
          "depth": analysis["depth"],
          "nodes": analysis.get("nodes"),
          "time": analysis.get("time"),
          "pv": [move.uci() for move in analysis["pv"]]
    }

@mcp.tool()
def get_best_move(fen: str):
    """Get the best move for a chess position"""
    board  = chess.Board(fen)
    return stockfish_manager.get_best_move(board).uci()

@mcp.tool()
def get_top_moves(fen: str, count: int = 5):
    board = chess.Board(fen)
    moves_data = stockfish_manager.get_top_moves(board, count)
    return [
        {
            "move": move.uci(),
            "score": str(score.relative)
        }
        for move, score in moves_data
    ]

if __name__ == "__main__":
    main()