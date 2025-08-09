"""Mock StockfishManager for testing without external engine dependency"""

import chess
import chess.engine
from typing import List, Tuple
from unittest.mock import Mock


class MockStockfishManager:
    """Mock StockfishManager that returns predictable results for testing"""
    
    def __init__(self, stockfish_path: str = None, depth: int = 15):
        self.limit = chess.engine.Limit(depth=depth)
        self.stockfish_path = stockfish_path
        self.engine = Mock()
        self.first_run = False  # Mock is always "initialized"
        self.engine_calls = []  # Track calls for test verification
        
        # Predefined responses for common positions
        self._responses = {
            # Starting position
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": {
                "best_move": "e2e4",
                "score": 20,  # +0.20 for white
                "top_moves": [
                    ("e2e4", 20),
                    ("d2d4", 15),
                    ("g1f3", 10),
                    ("b1c3", 5),
                    ("c2c4", 0)
                ]
            },
            # After 1.e4
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1": {
                "best_move": "e7e5",
                "score": -15,  # Slight advantage to white
                "top_moves": [
                    ("e7e5", -15),
                    ("c7c5", -20),
                    ("e7e6", -25),
                    ("d7d6", -30),
                    ("g8f6", -35)
                ]
            },
            # Sicilian Defense
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2": {
                "best_move": "g1f3",
                "score": 25,
                "top_moves": [
                    ("g1f3", 25),
                    ("d2d4", 20),
                    ("b1c3", 15),
                    ("f2f4", 10),
                    ("c2c3", 5)
                ]
            }
        }
    
    def _get_response(self, fen: str):
        """Get predefined response for a position, or default values"""
        if fen in self._responses:
            return self._responses[fen]
        else:
            # Default response for unknown positions
            return {
                "best_move": "e2e4",  # Default move
                "score": 0,  # Equal position
                "top_moves": [("e2e4", 0), ("d2d4", -5), ("g1f3", -10)]
            }
    
    def _ensure_engine(self):
        """Mock implementation - always succeeds"""
        pass
    
    def analyze_position(self, board: chess.Board):
        """Mock analyze_position that returns predictable results"""
        fen = board.fen()
        self.engine_calls.append(("analyze", fen))
        
        response = self._get_response(fen)
        best_move = chess.Move.from_uci(response["best_move"])
        score = chess.engine.PovScore(chess.engine.Cp(response["score"]), chess.WHITE)
        
        return {
            "pv": [best_move],
            "score": score,
            "depth": self.limit.depth,
            "nodes": 100000,  # Mock node count
            "time": 0.5  # Mock analysis time
        }
    
    def get_best_move(self, board: chess.Board) -> chess.Move:
        """Mock get_best_move that returns predictable moves"""
        fen = board.fen()
        self.engine_calls.append(("best_move", fen))
        
        response = self._get_response(fen)
        return chess.Move.from_uci(response["best_move"])
    
    def get_top_moves(self, board: chess.Board, count: int = 10) -> List[Tuple[chess.Move, chess.engine.PovScore]]:
        """Mock get_top_moves that returns predictable move lists"""
        fen = board.fen()
        self.engine_calls.append(("top_moves", fen, count))
        
        response = self._get_response(fen)
        top_moves = response["top_moves"][:count]  # Limit to requested count
        
        return [
            (chess.Move.from_uci(move), chess.engine.PovScore(chess.engine.Cp(score), chess.WHITE))
            for move, score in top_moves
        ]
    
    def close(self):
        """Mock close method"""
        self.engine_calls.append(("close",))
    
    def reset_calls(self):
        """Reset call tracking for test isolation"""
        self.engine_calls = []


class MockGameState:
    """Mock GameState for testing game functionality"""
    
    def __init__(self, ai_color: chess.Color, difficulty: int = 10, fen: str = None):
        if fen:
            try:
                self.board = chess.Board(fen)
            except ValueError as e:
                raise ValueError(f"Invalid FEN string: {e}")
        else:
            self.board = chess.Board()
            
        self.ai_color = ai_color
        self.current_player = chess.WHITE
        self.difficulty = difficulty
        self.move_history = []
    
    def make_move(self, move: chess.Move):
        """Make a move and update game state"""
        if move in self.board.legal_moves:
            self.board.push(move)
            self.move_history.append(move)
            self.current_player = not self.current_player
        else:
            raise ValueError(f"Illegal move: {move}")
    
    def is_game_over(self) -> bool:
        """Check if game is over"""
        return self.board.is_game_over()
    
    def get_result(self) -> str:
        """Get game result"""
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            return f"{winner} wins by checkmate"
        elif self.board.is_stalemate():
            return "Draw by stalemate"
        elif self.board.is_insufficient_material():
            return "Draw by insufficient material"
        else:
            return "Game in progress"