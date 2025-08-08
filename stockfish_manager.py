import chess.engine
import chess
from typing import Optional
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StockfishManager:
    limit: chess.engine.Limit
    engine: Optional[chess.engine.SimpleEngine] = None
    stockfish_path: str
    first_run = True
    
    def __init__(self, stockfish_path: str = None, depth=15):
        self.limit = chess.engine.Limit(depth=depth)
        self.stockfish_path = stockfish_path
    
    def _ensure_engine(self):
        if self.first_run:
            if self.stockfish_path:
                self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            else:
                self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
            logger.debug("Engine launched")
            self.first_run = False
    
    def analyze_position(self, board: chess.Board):
        self._ensure_engine()  
        return self.engine.analyse(board, self.limit)
    
    def get_best_move(self, board:chess.Board):
        self._ensure_engine()
        result = self.engine.play(board, self.limit) 
        return result.move

    def get_top_moves(self, board: chess.Board, count=10):
        self._ensure_engine()
        results = self.engine.analyse(board, self.limit, multipv=count)
        return  [(result["pv"][0], result["score"]) for result in results]
    
    def close(self):
        self.engine.quit()