"""
Test suite for FEN (Forsyth-Edwards Notation) validation.

This module tests the validation of chess position FEN strings according to the
official FEN specification. Tests cover:
- Valid FEN strings (various positions)
- Invalid FEN strings (malformed, incorrect counts, etc.)
- Edge cases and boundary conditions
- Error message accuracy and specificity
"""

import pytest
from stockfish_mcp.fen_validator import FenValidator, FenValidationError


class TestFenValidator:
    """Test cases for FEN string validation."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.validator = FenValidator()
    
    # Valid FEN strings
    def test_starting_position(self):
        """Test validation of the standard chess starting position."""
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        assert self.validator.validate(fen) is True
        assert self.validator.is_valid(fen) is True
    
    def test_empty_board(self):
        """Test validation of an empty board FEN."""
        fen = "8/8/8/8/8/8/8/8 w - - 0 1"
        assert self.validator.validate(fen) is True
    
    def test_mid_game_position(self):
        """Test validation of a typical mid-game position."""
        fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 4 4"
        assert self.validator.validate(fen) is True
    
    def test_endgame_position(self):
        """Test validation of a king and pawn endgame."""
        fen = "8/8/8/8/8/8/4K3/4k3 w - - 0 50"
        assert self.validator.validate(fen) is True
    
    def test_en_passant_position(self):
        """Test validation with en passant square set."""
        fen = "rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3"
        assert self.validator.validate(fen) is True
    
    def test_castling_rights_variations(self):
        """Test various castling rights combinations."""
        fens = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w K - 0 1",    # White kingside only
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Q - 0 1",    # White queenside only
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w k - 0 1",    # Black kingside only
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w q - 0 1",    # Black queenside only
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kq - 0 1",   # Mixed rights
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1",    # No castling rights
        ]
        for fen in fens:
            assert self.validator.validate(fen) is True, f"Failed for FEN: {fen}"
    
    # Invalid FEN strings - Structure errors
    def test_too_few_fields(self):
        """Test FEN with insufficient fields."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -")
        assert "6 fields required" in str(exc_info.value)
    
    def test_too_many_fields(self):
        """Test FEN with too many fields."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 extra")
        assert "6 fields required" in str(exc_info.value)
    
    def test_empty_fen(self):
        """Test empty FEN string."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("")
        assert "empty" in str(exc_info.value).lower()
    
    def test_none_fen(self):
        """Test None as FEN input."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate(None)
        assert "must be a string" in str(exc_info.value)
    
    # Invalid board position
    def test_too_few_ranks(self):
        """Test board with less than 8 ranks."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP w KQkq - 0 1")
        assert "8 ranks" in str(exc_info.value)
    
    def test_too_many_ranks(self):
        """Test board with more than 8 ranks."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert "8 ranks" in str(exc_info.value)
    
    def test_rank_too_long(self):
        """Test rank with more than 8 squares."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnrr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert "8 squares" in str(exc_info.value)
    
    def test_rank_too_short(self):
        """Test rank with less than 8 squares."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbn/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        assert "8 squares" in str(exc_info.value)
    
    def test_invalid_piece_character(self):
        """Test board with invalid piece characters."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBXR w KQkq - 0 1")
        assert "invalid character" in str(exc_info.value).lower()
    
    def test_invalid_number_in_rank(self):
        """Test rank with invalid numbers (0 or >8)."""
        invalid_fens = [
            "rnbqkbnr/pppppppp/0/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Zero
            "rnbqkbnr/pppppppp/9/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Nine
        ]
        for fen in invalid_fens:
            with pytest.raises(FenValidationError):
                self.validator.validate(fen)
    
    # Invalid active color
    def test_invalid_active_color(self):
        """Test invalid active color field."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1")
        assert "active color" in str(exc_info.value).lower()
    
    # Invalid castling rights
    def test_invalid_castling_characters(self):
        """Test invalid characters in castling rights."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkqX - 0 1")
        assert "castling" in str(exc_info.value).lower()
    
    def test_duplicate_castling_rights(self):
        """Test duplicate castling rights."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KKq - 0 1")
        assert "duplicate" in str(exc_info.value).lower()
    
    # Invalid en passant square
    def test_invalid_en_passant_format(self):
        """Test invalid en passant square format."""
        invalid_squares = ["a9", "i1", "a0", "h9", "aa", "11", "a"]
        for square in invalid_squares:
            with pytest.raises(FenValidationError) as exc_info:
                self.validator.validate(f"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq {square} 0 1")
            assert "en passant" in str(exc_info.value).lower()
    
    def test_impossible_en_passant_rank(self):
        """Test en passant square on impossible ranks."""
        impossible_ranks = ["a1", "a2", "a4", "a5", "a7", "a8"]
        for square in impossible_ranks:
            with pytest.raises(FenValidationError) as exc_info:
                self.validator.validate(f"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq {square} 0 1")
            assert "rank 3 or 6" in str(exc_info.value)
    
    # Invalid move counters
    def test_negative_halfmove_clock(self):
        """Test negative halfmove clock."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1")
        assert "non-negative integer" in str(exc_info.value)
    
    def test_negative_fullmove_number(self):
        """Test negative fullmove number."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 -1")
        assert "positive integer" in str(exc_info.value)
    
    def test_zero_fullmove_number(self):
        """Test zero fullmove number."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0")
        assert "positive integer" in str(exc_info.value)
    
    def test_non_integer_counters(self):
        """Test non-integer move counters."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - abc 1")
        assert "integer" in str(exc_info.value)
        
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 def")
        assert "integer" in str(exc_info.value)
    
    # King validation
    def test_missing_kings(self):
        """Test positions with missing kings."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")  # Missing black king
        assert "exactly one" in str(exc_info.value) and "king" in str(exc_info.value).lower()
    
    def test_multiple_kings(self):
        """Test positions with multiple kings of same color."""
        with pytest.raises(FenValidationError) as exc_info:
            self.validator.validate("rnbqkknr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")  # Two black kings
        assert "exactly one" in str(exc_info.value) and "king" in str(exc_info.value).lower()
    
    # Utility method tests
    def test_get_validation_errors(self):
        """Test the get_validation_errors method returns detailed error info."""
        invalid_fen = "invalid fen string"
        errors = self.validator.get_validation_errors(invalid_fen)
        assert isinstance(errors, list)
        assert len(errors) > 0
        assert all(isinstance(error, str) for error in errors)
    
    def test_get_validation_errors_valid_fen(self):
        """Test get_validation_errors returns empty list for valid FEN."""
        valid_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        errors = self.validator.get_validation_errors(valid_fen)
        assert errors == []
    
    # Edge cases
    def test_whitespace_handling(self):
        """Test FEN with extra whitespace."""
        with pytest.raises(FenValidationError):
            self.validator.validate("  rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1  ")
    
    def test_case_sensitivity(self):
        """Test that piece characters are case-sensitive."""
        # This should be valid (mixed case pieces)
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        assert self.validator.validate(fen) is True
        
        # Test invalid cases in active color and castling
        with pytest.raises(FenValidationError):
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR W KQkq - 0 1")  # Capital W
            
        with pytest.raises(FenValidationError):
            self.validator.validate("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqkq - 0 1")  # Invalid castling case


class TestFenValidationError:
    """Test the FenValidationError exception class."""
    
    def test_error_creation(self):
        """Test creating FenValidationError with message."""
        error = FenValidationError("Test error message")
        assert str(error) == "Test error message"
        assert isinstance(error, ValueError)
    
    def test_error_with_position_info(self):
        """Test error with additional position information."""
        error = FenValidationError("Invalid piece", field="board", position="rank 1")
        assert "Invalid piece" in str(error)
        # Test that additional info can be stored if the class supports it