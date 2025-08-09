"""Test MCP tools using FastMCP client for proper MCP protocol testing"""

import pytest
from unittest.mock import patch
import chess

# Import server components for testing  
from server import mcp


class TestToolDiscovery:
    """Test MCP tool discovery and metadata"""
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test that all expected tools are registered with MCP server"""
        tools = await mcp.list_tools()
        tool_names = [tool.name for tool in tools]
        
        expected_tools = [
            "fen_validator",
            "analyze_position", 
            "get_best_move",
            "get_top_moves",
            "start_game"
        ]
        
        for tool_name in expected_tools:
            assert tool_name in tool_names, f"Tool {tool_name} not found in MCP server tools"
    
    @pytest.mark.asyncio
    async def test_tool_metadata(self):
        """Test that tools have proper metadata"""
        tools = await mcp.list_tools()
        
        for tool in tools:
            assert tool.name, "Tool should have a name"
            assert hasattr(tool, 'inputSchema'), "Tool should have input schema"


class TestFENValidator:
    """Test FEN validation tool"""
    
    @pytest.mark.asyncio
    async def test_valid_fen_positions(self, starting_position, sample_game_positions):
        """Test FEN validator with valid positions using MCP call_tool"""
        # Test starting position
        result = await mcp.call_tool("fen_validator", {"fen": starting_position})
        result_value = result[0][0].text.lower() == "true" if result and len(result[0]) > 0 else False
        assert result_value == True, "Starting position should be valid"
        
        # Test various game positions
        for position_name, fen in sample_game_positions.items():
            result = await mcp.call_tool("fen_validator", {"fen": fen})
            result_value = result[0][0].text.lower() == "true" if result and len(result[0]) > 0 else False
            assert result_value == True, f"Position {position_name} should be valid: {fen}"
    
    @pytest.mark.asyncio
    async def test_invalid_fen_positions(self, invalid_fens):
        """Test FEN validator with invalid positions using MCP call_tool"""
        for invalid_fen in invalid_fens:
            result = await mcp.call_tool("fen_validator", {"fen": invalid_fen})
            # Extract boolean result from TextContent
            result_value = result[0][0].text.lower() == "true" if result and len(result[0]) > 0 else False
            assert result_value == False, f"Invalid FEN should return False: {invalid_fen}"
    
    @pytest.mark.parametrize("fen,expected", [
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", True),
        ("invalid_fen", False),
        ("rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2", True),
        ("", False),
        ("8/8/8/8/8/8/4K3/4k3 w - - 0 1", True),
    ])
    @pytest.mark.asyncio
    async def test_fen_validation_cases(self, fen, expected):
        """Parameterized test for various FEN validation cases using MCP call_tool"""
        result = await mcp.call_tool("fen_validator", {"fen": fen})
        result_value = result[0][0].text.lower() == "true" if result and len(result[0]) > 0 else False
        assert result_value == expected, f"FEN {fen} validation result should be {expected}"


class TestAnalysisTools:
    """Test chess analysis tools with mocked StockfishManager"""
    
    @pytest.mark.asyncio 
    async def test_analyze_position_structure(self, starting_position, mock_manager):
        """Test analyze_position returns expected data structure using MCP call_tool"""
        with patch('server.stockfish_manager', mock_manager):
            result = await mcp.call_tool("analyze_position", {"fen": starting_position})
            
            # Parse JSON response from TextContent
            import json
            result_data = json.loads(result[0].text)
            
            # Verify required fields are present
            assert "best_move" in result_data, "analyze_position should return best_move"
            assert "score" in result_data, "analyze_position should return score"
            assert "depth" in result_data, "analyze_position should return depth"
            assert "pv" in result_data, "analyze_position should return principal variation"
            
            # Verify data types
            assert isinstance(result_data["best_move"], str), "best_move should be string"
            assert isinstance(result_data["pv"], list), "pv should be list of moves"
            assert len(result_data["pv"]) > 0, "pv should contain at least one move"
    
    @pytest.mark.asyncio
    async def test_get_best_move(self, starting_position, mock_manager):
        """Test get_best_move returns valid UCI move using MCP call_tool"""
        with patch('server.stockfish_manager', mock_manager):
            result = await mcp.call_tool("get_best_move", {"fen": starting_position})
            
            # Extract move string from TextContent
            move_str = result[0].text
            
            # Should return a string in UCI format
            assert isinstance(move_str, str), "get_best_move should return string"
            assert len(move_str) >= 4, "UCI move should be at least 4 characters"
            
            # Should be a valid chess move
            try:
                move = chess.Move.from_uci(move_str)
                board = chess.Board(starting_position)
                assert move in board.legal_moves, f"Move {move_str} should be legal in starting position"
            except ValueError:
                pytest.fail(f"get_best_move returned invalid UCI move: {move_str}")
    
    @pytest.mark.asyncio
    async def test_get_top_moves_structure(self, starting_position, mock_manager):
        """Test get_top_moves returns expected structure"""
        with patch('server.stockfish_manager', mock_manager):
            from server import get_top_moves
            
            # Test default count
            result = get_top_moves(starting_position)
            
            assert isinstance(result, list), "get_top_moves should return list"
            assert len(result) > 0, "get_top_moves should return at least one move"
            assert len(result) <= 5, "get_top_moves should respect default count of 5"
            
            # Check structure of each move entry
            for move_entry in result:
                assert isinstance(move_entry, dict), "Each move should be a dict"
                assert "move" in move_entry, "Each move entry should have 'move' field"
                assert "score" in move_entry, "Each move entry should have 'score' field"
                assert isinstance(move_entry["move"], str), "Move should be string"
    
    @pytest.mark.asyncio
    async def test_get_top_moves_count_parameter(self, starting_position, mock_manager):
        """Test get_top_moves respects count parameter"""
        with patch('server.stockfish_manager', mock_manager):
            from server import get_top_moves
            
            # Test different counts
            for count in [1, 3, 10]:
                result = get_top_moves(starting_position, count)
                assert len(result) <= count, f"get_top_moves should return at most {count} moves"


class TestGameTools:
    """Test chess game management tools"""
    
    @pytest.mark.asyncio
    async def test_start_game_default_parameters(self):
        """Test start_game with default parameters"""
        import server
        
        result = server.start_game()
        
        assert isinstance(result, dict), "start_game should return dict"
        assert result["status"] == "Game started", "Should confirm game started"
        assert result["ai_color"] == "black", "Default AI color should be black"
        
        # Check that global game state was created
        assert server.current_game is not None, "current_game should be initialized"
        assert server.current_game.ai_color == chess.BLACK, "AI should be playing black"
    
    @pytest.mark.asyncio
    async def test_start_game_with_parameters(self):
        """Test start_game with custom parameters"""
        import server
        
        result = server.start_game(ai_color="white", difficulty=15)
        
        assert result["status"] == "Game started"
        assert result["ai_color"] == "white", "AI color should be set to white"
        assert server.current_game.ai_color == chess.WHITE, "AI should be playing white"
        assert server.current_game.difficulty == 15, "Difficulty should be set to 15"
    
    @pytest.mark.asyncio
    async def test_start_game_with_custom_fen(self, sample_game_positions):
        """Test start_game with custom starting position"""
        import server
        
        sicilian_fen = sample_game_positions["sicilian"]
        result = server.start_game(fen=sicilian_fen)
        
        assert result["status"] == "Game started"
        # Compare normalized FEN (chess.Board normalizes en passant availability)
        import chess
        expected_board = chess.Board(sicilian_fen)
        assert server.current_game.board.fen() == expected_board.fen(), "Board should be set to custom position"
    
    @pytest.mark.asyncio
    async def test_start_game_invalid_fen(self):
        """Test start_game with invalid FEN"""
        import server
        
        result = server.start_game(fen="invalid_fen_string")
        
        assert "error" in result, "Invalid FEN should return error"
        assert "Invalid FEN string" in result["error"], "Error should mention invalid FEN"


class TestToolIntegration:
    """Test integration between tools and components"""
    
    @pytest.mark.asyncio
    async def test_analysis_workflow(self, sample_game_positions, mock_manager):
        """Test complete analysis workflow"""
        with patch('server.stockfish_manager', mock_manager):
            import server
            
            for position_name, fen in sample_game_positions.items():
                # First validate the position
                is_valid = server.fen_validator(fen)
                assert is_valid, f"Position {position_name} should be valid"
                
                # Then analyze it
                analysis = server.analyze_position(fen)
                best_move = server.get_best_move(fen)
                
                # Results should be consistent
                assert analysis["best_move"] == best_move, f"Analysis and get_best_move should agree for {position_name}"
    
    @pytest.mark.asyncio
    async def test_mock_manager_call_tracking(self, starting_position, mock_manager):
        """Test that mock manager properly tracks calls"""
        with patch('server.stockfish_manager', mock_manager):
            import server
            
            mock_manager.reset_calls()
            
            # Make various calls
            server.analyze_position(starting_position)
            server.get_best_move(starting_position)
            server.get_top_moves(starting_position, 3)
            
            # Verify calls were tracked
            calls = mock_manager.engine_calls
            assert len(calls) == 3, "Should track all three calls"
            assert calls[0][0] == "analyze", "First call should be analyze"
            assert calls[1][0] == "best_move", "Second call should be best_move"
            assert calls[2][0] == "top_moves", "Third call should be top_moves"