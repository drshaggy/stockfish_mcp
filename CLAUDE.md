# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a Stockfish MCP (Model Context Protocol) server that exposes chess analysis tools to AI agents via FastMCP. Key architectural components:

- **Core Server**: `server.py` - FastMCP instance with @mcp.tool() decorated functions
- **Engine Manager**: `stockfish_manager.py` - Persistent Stockfish connection with lazy initialization 
- **Game State**: `game_state.py` - Chess game management for interactive play
- **Dependencies**: python-chess for all chess logic, external Stockfish binary required

The architecture uses persistent engine connections for performance - Stockfish stays alive between analysis requests, providing sub-100ms response times.

## Development Commands

**Environment & Development:**
```bash
# Install dependencies and sync environment
uv sync

# Run MCP server in development mode (with debugging)
uv run mcp dev server.py

# Add new dependencies
uv add package-name

# Run tests (comprehensive test suite with mocks)
uv run python -m pytest

# Run tests with coverage
uv run python -m pytest --cov=stockfish_mcp

# Run specific test files
uv run python -m pytest tests/test_tools.py
uv run python -m pytest tests/integration/
```

**Claude Desktop Installation:**
```bash
# Install to Claude Desktop with dependencies (CRITICAL: use --with flag)
uv run mcp install server.py --name stockfish --with python-chess

# Include additional dependencies if needed  
uv run mcp install server.py --name stockfish --with python-chess --with pydantic
```

**Important:** The `--with` flag is mandatory for Claude Desktop installation. MCP creates isolated environments that need explicit dependency inclusion.

## Testing Architecture

The project uses a comprehensive 3-layer testing approach based on MCP ecosystem best practices:

**Test Structure:**
- `tests/conftest.py` - pytest configuration with chess-specific fixtures
- `tests/test_tools.py` - Individual MCP tool tests with FastMCP Client
- `tests/mocks/mock_stockfish.py` - Mock engine for unit testing
- `tests/integration/` - Full server workflow tests with real Stockfish

**Testing Patterns:**
- **Unit Tests**: Fast tests with mock StockfishManager (no external dependencies)
- **Integration Tests**: Real Stockfish engine interaction for complete workflows
- **FastMCP Client Testing**: In-memory MCP protocol testing with `async with Client(mcp):`
- **Async Testing**: Uses `@pytest.mark.anyio` for async MCP tool testing

**Key Test Fixtures:**
- `starting_position` - Standard chess starting FEN
- `sample_game_positions` - Common positions (starting, after e4, sicilian, endgame)
- `invalid_fens` - Invalid FEN strings for negative testing

## Project Guidelines - CRITICAL LEARNING PROJECT RULES
- **NEVER WRITE MCP CODE**: This is a learning project - you must NOT implement MCP servers, tools, or handlers
- **NO CODE GENERATION**: Do not create or suggest complete implementations of MCP functionality
- **MENTORSHIP ONLY**: Guide, explain concepts, point to resources - do not implement
- **EXCEPTION - TESTING ONLY**: You can create test frameworks and comprehensive tests

## Current Implementation Status

**Implemented Tools:**
- `fen_validator(fen: str)` - FEN string validation using python-chess
- `analyze_position(fen: str)` - Position analysis with score, depth, principal variation
- `get_best_move(fen: str)` - Best move in UCI notation  
- `get_top_moves(fen: str, count: int = 5)` - Multiple top moves with MultiPV
- `start_game(ai_color: str = "black", difficulty: int = 10, fen: str = None)` - Initialize chess game

**Key Classes:**
- `StockfishManager` (stockfish_manager.py:9-43) - Manages persistent engine connection
- `GameState` (game_state.py:6-22) - Tracks game state, move history, player colors

## Architecture Decisions

**Persistent Engine Connection:**
- StockfishManager uses lazy initialization pattern (stockfish_manager.py:19-26)
- Engine connection maintained across requests for performance
- Default depth: 15 plies, configurable via constructor
- Health checking and reconnection logic planned

**Game State Management:**
- Global `current_game` variable tracks active game (server.py:13)
- GameState validates FEN positions at construction (game_state.py:14-17)
- Supports custom starting positions and standard games

**MCP Tool Design:**
- All tools use `@mcp.tool()` decorator for automatic registration
- Chess analysis tools return structured data with consistent formats
- Error handling with ValueError exceptions for invalid FEN strings

## Chess Development Patterns

Always use python-chess for chess logic:
```python
import chess

# FEN validation
board = chess.Board(fen)  # Raises ValueError if invalid

# Move validation  
move = chess.Move.from_uci("e2e4")
board.is_legal(move)

# Position queries
board.is_check()
board.is_checkmate()
list(board.legal_moves)
```

## Design Documentation

Architecture plans in `docs/`:
- [StockfishManager Design Plan](docs/stockfish-manager-design.md) - Persistent engine architecture
- [Chess Game Feature Plan](docs/chess-game-feature-plan.md) - Interactive game playing design
- [Testing Strategy](docs/testing-strategy.md) - Comprehensive MCP testing approach

## External Dependencies

**Required:**
- Stockfish chess engine must be installed separately:
  - macOS: `brew install stockfish` 
  - Ubuntu: `sudo apt install stockfish`
  - Windows: Download from stockfishchess.org

**Python Dependencies:**
- `python-chess>=1.999` - Core chess logic and UCI interface
- `mcp[cli]>=1.12.3` - MCP protocol implementation
- `pydantic>=2.0.0` - Data validation
- `pytest`, `pytest-asyncio`, `anyio` - Testing framework (optional dependencies)

## Project Status

**✅ Completed:**
- Basic MCP server with FastMCP
- Persistent Stockfish engine integration
- Core analysis tools (validation, analysis, best moves)
- Game state management foundation
- Comprehensive testing architecture setup

**🔄 In Progress:**
- Interactive game playing tools (record_opponent_move, make_move, get_game_status)
- Comprehensive error handling and reconnection logic

**📋 Planned:**
- Position information tools
- Advanced analysis (tactics, opening identification)
- PGN format support