import chess.engine
import chess
from typing import Optional
import logging
import threading

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class StockfishManager:
    limit: chess.engine.Limit
    engine: Optional[chess.engine.SimpleEngine] = None
    stockfish_path: str
    first_run = True
    _lock: threading.Lock
    
    def __init__(self, stockfish_path: str = None, depth=15):
        self.limit = chess.engine.Limit(depth=depth)
        self.stockfish_path = stockfish_path
        self._lock = threading.Lock()
    
    def _ensure_engine(self):
        """Ensure engine is running, start or restart if needed"""
        if self.engine is None or self.first_run:
            try:
                if self.stockfish_path:
                    self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
                else:
                    self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
                # Verify engine is responsive with ping
                self.engine.ping()
                logger.debug("Engine launched and verified")
                self.first_run = False
            except Exception as e:
                logger.error(f"Failed to start engine: {e}")
                self.engine = None
                raise
    
    def _restart_engine_if_needed(self):
        """Restart engine if it has terminated"""
        try:
            if self.engine is not None:
                self.engine.ping()
        except (chess.engine.EngineTerminatedError, chess.engine.EngineError) as e:
            logger.warning(f"Engine terminated, restarting: {e}")
            self.engine = None
            self._ensure_engine()
    
    def analyze_position(self, board: chess.Board):
        with self._lock:
            self._ensure_engine()
            self._restart_engine_if_needed()
            try:
                return self.engine.analyse(board, self.limit)
            except (chess.engine.EngineTerminatedError, chess.engine.EngineError) as e:
                logger.error(f"Engine error during analysis: {e}")
                self.engine = None
                self._ensure_engine()
                # Retry once after restart
                return self.engine.analyse(board, self.limit)
    
    def get_best_move(self, board:chess.Board):
        with self._lock:
            self._ensure_engine()
            self._restart_engine_if_needed()
            try:
                result = self.engine.play(board, self.limit)
                return result.move
            except (chess.engine.EngineTerminatedError, chess.engine.EngineError) as e:
                logger.error(f"Engine error during move search: {e}")
                self.engine = None
                self._ensure_engine()
                # Retry once after restart
                result = self.engine.play(board, self.limit)
                return result.move

    def get_top_moves(self, board: chess.Board, count=10):
        with self._lock:
            self._ensure_engine()
            self._restart_engine_if_needed()
            try:
                results = self.engine.analyse(board, self.limit, multipv=count)
                return [(result["pv"][0], result["score"]) for result in results]
            except (chess.engine.EngineTerminatedError, chess.engine.EngineError) as e:
                logger.error(f"Engine error during multi-pv analysis: {e}")
                self.engine = None
                self._ensure_engine()
                # Retry once after restart
                results = self.engine.analyse(board, self.limit, multipv=count)
                return [(result["pv"][0], result["score"]) for result in results]
    
    def close(self):
        with self._lock:
            if self.engine is not None:
                try:
                    self.engine.quit()
                except Exception as e:
                    logger.warning(f"Error closing engine: {e}")
                finally:
                    self.engine = None