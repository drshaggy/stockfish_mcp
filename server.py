from mcp.server.fastmcp import FastMCP
import chess
from game_state import GameState
from stockfish_manager import StockfishManager as StockfishManager
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.debug("Server started")
mcp = FastMCP("stockfish",
        description="Chess analysis and interactive game playing server using Stockfish engine. Provides position analysis, move generation, and interactive chess gameplay tools.")
stockfish_manager = StockfishManager()
current_game: GameState = None


CHESS_API_BASE = 'https://chess-api.com/v1'

def main():
    mcp.run()

@mcp.tool()
def fen_validator(fen: str) -> bool:
    """Validate a FEN string for a chess game"""
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
    """Start a new chess game"""
    global current_game
    try:
        color = chess.BLACK if ai_color.lower() == "black" else chess.WHITE
        current_game = GameState(color, difficulty, fen)
        return {"status": "Game started", "ai_color": ai_color}
    except ValueError as e:
        return {"error": str(e)}

@mcp.tool()
def record_opponent_move(move: str):
    """Record an oppenent's move in the current chess game"""
    global current_game
    if current_game is None:
        return {"error": "No active game. Start a game first."}
    try:
        move_obj = chess.Move.from_uci(move)
        current_game.make_move(move_obj)
        return {"status": "Move recorded"}
    except ValueError as e:
        return {"error": f"Invalid move: {e}"}
  
@mcp.tool()
def make_move(move: str):
    """Make your move in the current chess game"""
    global current_game
    if current_game is None:
        return {"error": "No active game. Start a game first."}
    try:
        move_obj = chess.Move.from_uci(move)
        current_game.make_move(move_obj)
        return {"status": "Move made"}
    except ValueError as e:
        return {"error": f"Invalid move: {e}"}

if __name__ == "__main__":
    main()