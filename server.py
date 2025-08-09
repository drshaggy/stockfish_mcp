from mcp.server.fastmcp import FastMCP
import chess
from game_state import GameState
from stockfish_manager import StockfishManager as StockfishManager
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("Server started")
mcp = FastMCP("stockfish")
stockfish_manager = StockfishManager()
current_game: GameState = None


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

# Stockfish tools

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
    """Get the top N moves for a chess position"""
    board = chess.Board(fen)
    moves_data = stockfish_manager.get_top_moves(board, count)
    return [
        {
            "move": move.uci(),
            "score": str(score.relative)
        }
        for move, score in moves_data
    ]

# Game state tools

@mcp.tool()
def start_game(ai_color: str = "black", difficulty: int = 10, fen:str = None):
    """Start a new game"""
    global current_game
    try:
        color = chess.BLACK if ai_color.lower() == "black" else chess.WHITE
        current_game = GameState(color, difficulty, fen)
        return {"status": "Game started", "ai_color": ai_color}
    except ValueError as e:
        return {"error": str(e)}

    

if __name__ == "__main__":
    main()