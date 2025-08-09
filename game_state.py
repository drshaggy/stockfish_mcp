import chess.engine
import chess
from typing import Optional
import logging

class GameState():
    board: chess.Board
    move_history: list[chess.Move]
    ai_color: chess.Color
    difficulty: int

    @property 
    def current_player(self) -> chess.Color:
        return self.board.turn

    def __init__(self, ai_color: chess.Color, difficulty: int = 10, fen: str = None):
        try:
            self.board = chess.Board(fen) if fen else chess.Board()
        except ValueError as e:
            raise ValueError(f"Invalid FEN string: {e}")
        self.ai_color = ai_color
        self.difficulty = difficulty
        self.move_history = []
    
    def make_move(self, move: chess.Move):
        if not self.board.is_legal(move):
            raise ValueError(f"Invalid move: {move}")
        self.board.push(move)
        self.move_history.append(move)

    def game_status(self):
        return {
            "fen": self.board.fen(),
            "current_player": "white" if self.current_player == chess.WHITE else "black",
            "move_history": [move.uci() for move in self.move_history],  # UCI strings
            "is_check": self.board.is_check(),
            "is_checkmate": self.board.is_checkmate(),
            "is_stalemate": self.board.is_stalemate(),
            "is_game_over": self.board.is_game_over(),
            "ai_color": "white" if self.ai_color == chess.WHITE else "black"
      }