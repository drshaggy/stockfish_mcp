import chess.engine
import chess
from typing import Optional
import logging

class GameState():
    board: chess.Board
    move_history: list[chess.Move]
    current_player: chess.Color
    ai_color: chess.Color
    difficulty: int

    def __init__(self, ai_color: chess.Color, difficulty: int = 10, fen: str = None):
        try:
          self.board = chess.Board(fen) if fen else chess.Board()
        except ValueError as e:
          raise ValueError(f"Invalid FEN string: {e}")
        self.ai_color = ai_color
        self.current_player = chess.WHITE
        self.difficulty = difficulty
        self.move_history = []
    