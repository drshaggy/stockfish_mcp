# MCP Testing Strategy for Stockfish Server

This document outlines the comprehensive testing approach for the Stockfish MCP server, based on research of MCP testing patterns and best practices.

## Research Summary

### Key Findings from MCP Ecosystem
- **pytest + anyio** is the standard for async MCP testing
- **FastMCP Client** provides excellent in-memory testing capabilities  
- **Layered testing approach**: Unit → Integration → End-to-end
- **Mock external dependencies** (Stockfish engine) for reliable unit tests

### Testing Patterns from MCP Projects
- In-memory client testing with FastMCP
- Session-based testing for server communication
- Tool metadata and execution validation
- Async testing with `@pytest.mark.anyio`

## Testing Architecture

### Test Structure
```
tests/
├── conftest.py              # pytest configuration & fixtures
├── test_tools.py            # Individual MCP tool tests  
├── test_stockfish_manager.py # Engine manager unit tests
├── test_game_state.py       # Game state logic tests
├── integration/
│   └── test_server_integration.py # Full server workflow tests
└── mocks/
    └── mock_stockfish.py     # Mock engine for testing
```

### Testing Layers

#### **Unit Tests (Fast, No External Dependencies)**
- Test each MCP tool with mock StockfishManager
- Test StockfishManager with mock engine
- Test GameState logic independently
- Test FEN validation and chess logic

#### **Integration Tests (Real Engine Interaction)**
- Test full tool workflow with real Stockfish
- Test engine persistence and lazy initialization  
- Test error handling with actual engine failures

#### **End-to-End Tests (Complete Server Testing)**
- Test MCP protocol communication
- Test tool discovery and metadata
- Test complete analysis workflows

## Key Testing Patterns

### FastMCP In-Memory Client Testing
```python
@pytest.mark.anyio
async def test_analyze_position():
    from server import mcp
    from fastmcp import Client
    
    async with Client(mcp) as client:
        result = await client.call_tool("analyze_position", {
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        })
        assert "best_move" in result
        assert "score" in result
        assert "depth" in result
```

### Tool Testing Structure
```python
# Test tool metadata
@pytest.mark.anyio
async def test_tool_discovery():
    from server import mcp
    from fastmcp import Client
    
    async with Client(mcp) as client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        
        assert "fen_validator" in tool_names
        assert "analyze_position" in tool_names
        assert "get_best_move" in tool_names
        assert "get_top_moves" in tool_names
        assert "start_game" in tool_names

# Test individual tool execution
@pytest.mark.anyio
async def test_fen_validator():
    from server import mcp
    from fastmcp import Client
    
    async with Client(mcp) as client:
        # Test valid FEN
        result = await client.call_tool("fen_validator", {
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        })
        assert result == True
        
        # Test invalid FEN
        result = await client.call_tool("fen_validator", {
            "fen": "invalid_fen"
        })
        assert result == False
```

### Mock Engine Testing
```python
# Mock StockfishManager for unit tests
class MockStockfishManager:
    def __init__(self):
        self.engine_calls = []
    
    def analyze_position(self, board):
        self.engine_calls.append(("analyze", board.fen()))
        return {
            "pv": [chess.Move.from_uci("e2e4")],
            "score": chess.engine.PovScore(chess.engine.Cp(20), chess.WHITE),
            "depth": 15,
            "nodes": 100000,
            "time": 0.5
        }
    
    def get_best_move(self, board):
        self.engine_calls.append(("best_move", board.fen()))
        return chess.Move.from_uci("e2e4")
```

### Parameterized Testing
```python
@pytest.mark.parametrize("fen,expected_valid", [
    ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", True),
    ("invalid_fen_string", False),
    ("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", True),
])
@pytest.mark.anyio
async def test_fen_validation_cases(fen, expected_valid):
    from server import mcp
    from fastmcp import Client
    
    async with Client(mcp) as client:
        result = await client.call_tool("fen_validator", {"fen": fen})
        assert result == expected_valid
```

## Testing Categories

### Tool Testing
- **Parameter validation**: Test required/optional parameters
- **Return format validation**: Ensure consistent response structure
- **Error handling**: Test invalid inputs and error responses
- **Schema generation**: Validate tool metadata

### StockfishManager Testing
- **Lazy initialization**: Test engine starts on first use
- **Connection persistence**: Test engine reuse across requests
- **Error recovery**: Test engine crash and reconnection
- **Performance**: Test response times and resource usage

### GameState Testing
- **Initialization**: Test various starting positions
- **Move validation**: Test legal/illegal move handling
- **State tracking**: Test move history and game status
- **FEN handling**: Test custom position setup

### Integration Testing
- **Complete workflows**: Test full analysis sequences
- **Engine integration**: Test real Stockfish interaction
- **Performance validation**: Test analysis speed requirements
- **Resource management**: Test proper cleanup

## Implementation Plan

### Phase 1 - Foundation
1. **Set up pytest configuration**
   - Configure anyio backend
   - Add test dependencies to pyproject.toml
   - Create conftest.py with fixtures

2. **Create mock utilities**
   - MockStockfishManager class
   - Test fixture for common FEN positions
   - Mock game state scenarios

3. **Basic tool tests**
   - Test tool discovery and metadata
   - Test simple tools like fen_validator
   - Validate FastMCP Client integration

### Phase 2 - Unit Tests
1. **Individual tool testing**
   - Test each MCP tool with mocked dependencies
   - Parameterized tests for edge cases
   - Error scenario testing

2. **Component testing**
   - StockfishManager unit tests
   - GameState logic tests
   - Chess utility function tests

3. **Mock validation**
   - Ensure mocks accurately represent real behavior
   - Test mock vs real engine consistency

### Phase 3 - Integration Tests
1. **Real engine testing**
   - Test with actual Stockfish installation
   - Performance and reliability testing
   - Engine lifecycle management

2. **End-to-end workflows**
   - Complete analysis sequences
   - Game playing workflows
   - Error recovery scenarios

3. **CI/CD integration**
   - Separate unit and integration test suites
   - Optional Stockfish installation for CI
   - Performance benchmarking

## Test Configuration

### pytest Configuration (conftest.py)
```python
import pytest
import chess
from unittest.mock import Mock

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def starting_position():
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@pytest.fixture
def mock_stockfish_manager():
    return MockStockfishManager()

@pytest.fixture
def sample_game_positions():
    return {
        "starting": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "after_e4": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        "sicilian": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
    }
```

### Dependencies
Add to pyproject.toml:
```toml
[project.optional-dependencies]
test = [
    "pytest>=7.0",
    "pytest-anyio>=0.21.0",
    "pytest-cov>=4.0",
    "pytest-mock>=3.10.0"
]
```

## Success Metrics

### Test Coverage Goals
- **Tool Coverage**: 100% of MCP tools tested
- **Code Coverage**: >90% for core components  
- **Integration Coverage**: All major workflows tested

### Performance Benchmarks
- **Unit Tests**: Complete in <5 seconds
- **Integration Tests**: Complete in <30 seconds
- **Analysis Performance**: <100ms for depth-15 analysis

### Quality Assurance
- **Reliability**: Tests pass consistently
- **Maintainability**: Tests are easy to update
- **Documentation**: All testing patterns documented

## Benefits

### Development Benefits
- **Fast feedback** - Unit tests run without external dependencies
- **Reliable CI/CD** - Mock tests won't fail due to missing Stockfish  
- **Regression detection** - Catch bugs before deployment
- **Refactoring confidence** - Safe to modify code with test coverage

### MCP-Specific Benefits
- **Protocol validation** - Ensure MCP compliance
- **Tool reliability** - Verify tool behavior and metadata
- **Client compatibility** - Test with FastMCP Client patterns
- **Performance validation** - Ensure responsive tool execution

This testing strategy provides comprehensive coverage while following MCP community best practices and ensuring reliable, maintainable test suite.