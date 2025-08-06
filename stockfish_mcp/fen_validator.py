from stockfish_mcp.logger import get_logger

logger = get_logger(__name__)

class FenValidationError(ValueError):
    pass

class FenValidator:
    
    def validate(self, fen:str) -> bool:
        self._validate_empty_fen(fen)
        self._validate_is_string(fen)
        self._validate_field_count(fen) 
        self._validate_board_ranks(fen)
        self._validate_rank_squares(fen)
        self._validate_en_passent_rank(fen)
        return True

    def is_valid(self, fen:str) -> bool:
        try:
            self.validate(fen)
        except FenValidationError as e:
            logger.error(f"Validation failed for {fen}", extra={"error": e})
            return False
        return True

    def get_validation_errors(self, fen:str) -> list[str]:
        pass
    
    def _validate_field_count(self, fen:str) -> bool:
        fields: str = fen.split(' ')
        if len(fields) != 6:
            raise FenValidationError(f"Invalid FEN string: The number of fields is {len(fields)}. 6 fields required")
        return True
        
    def _validate_empty_fen(self, fen:str) -> bool:
        if fen == "":
            raise FenValidationError("FEN is empty")
        return True
        
    def _validate_is_string(self, fen:str) -> bool:
        if not isinstance(fen, str):
            raise FenValidationError(f"Invalid FEN string: {fen} must be a string")
        return True

    def _validate_board_ranks(self, fen:str) -> bool:
        ranks = fen.split(' ')[0].split('/')
        logger.debug(ranks)
        if len(ranks) != 8:
            raise FenValidationError(f"Invalid FEN string: The number of ranks is {len(ranks)}. Must be 8 ranks.")
        return True

    def _validate_rank_squares(self, fen:str) -> bool:
        ranks = fen.split(' ')[0].split('/')
        for rank in ranks:
            square_count = 0
            for char in rank:
                if char.isdigit():
                    square_count += int(char)
                else:
                    square_count += 1

            if square_count != 8:
                raise FenValidationError(f"Invalid FEN string: The number of squares on a rank is {square_count}. Must be 8 squares.")
        return True

    def _validate_en_passent_rank(self, fen:str) -> bool:
        ep_square = fen.split(' ')[3]
        if ep_square == '-':
            return True
        if ep_square[1] != '3' and ep_square[1] != '6':
            raise FenValidationError(f"Invalid FEN string: The en passant rank is {ep_square[1]}. Must be 3 or 6.")
        return True
        