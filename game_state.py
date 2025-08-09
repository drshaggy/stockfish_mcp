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

    def game_state(self):
        return {
            "board": str(self.board),
            "current_player": self.current_player,
            "move_history": self.move_history
        }