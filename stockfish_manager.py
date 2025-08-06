import chess.engine
import chess
from typing import Optional
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StockfishManager:
    depth: int
    engine: Optional[chess.engine.SimpleEngine] = None
    stockfish_path: str
    first_run = True
    
    def __init__(self, stockfish_path: str = None, depth=15):
        self.depth = depth
        self.stockfish_path = stockfish_path
    
    def _ensure_engine(self):
        if self.stockfish_path:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
        else:
            self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        logger.debug("Engine launched")
            
    
    def analyze_position(self, board: chess.Board):
        if self.first_run:
            self._ensure_engine()
            self.first_run = False    
        limit = chess.engine.Limit(depth=self.depth)
        return self.engine.analyse(board, limit)
    
    def close(self):
        self.engine.quit()