# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a Stockfish MCP (Model Context Protocol) server built with FastMCP and Python. The architecture includes:

- **Main Server**: `server.py` contains FastMCP instance and tool definitions
- **Engine Management**: `stockfish_manager.py` provides StockfishManager class for persistent Stockfish connections
- **Package Structure**: Currently flat structure with main files in root, `stockfish_mcp/` package exists but unused
- **MCP Tools**: Chess analysis tools exposed via FastMCP decorators (@mcp.tool())
- **Architecture Decision**: Persistent engine connection with lazy initialization for optimal performance
- **Dependencies**: FastMCP for MCP protocol, python-chess for chess logic and UCI communication
- **External Dependency**: Stockfish chess engine (user-installed binary)

## Development Commands

**Environment Setup:**
```bash
# Install dependencies and sync environment
uv sync

# Run the MCP server in development mode (with debugging/inspection)
uv run mcp dev server.py

# Run server via package entry point (when implemented)
uv run stockfish-mcp
```

**Development Tasks:**
```bash
# Add new dependencies
uv add package-name

# Run Python scripts with project dependencies
uv run python script.py

# Install project in development mode
uv pip install -e .

# Run tests
uv run python -m pytest

# Run tests with coverage
uv run python -m pytest --cov=stockfish_mcp

# Run single test file
uv run python -m pytest tests/test_specific.py

# Run tests in verbose mode
uv run python -m pytest -v
```

**Claude Desktop Installation:**
```bash
# Install to Claude Desktop with dependencies
uv run mcp install server.py --name stockfish --with python-chess

# Include additional dependencies if needed
uv run mcp install server.py --name stockfish --with python-chess --with pydantic

# Development testing (includes dependencies automatically)
uv run mcp dev server.py --with-editable .
```

**Important:** Always use the `--with` flag to include project dependencies when installing to Claude Desktop. The MCP install process creates an isolated environment that needs explicit dependency inclusion.

## Project Guidelines - CRITICAL INSTRUCTIONS
- **NEVER WRITE MCP CODE**: This is a learning project. I must implement ALL MCP-related code myself
- **NO CODE GENERATION**: Do not create, write, or suggest complete code implementations for MCP servers, tools, or handlers
- **NO FILE CREATION**: Do not create Python files with MCP implementations
- **MENTORSHIP ONLY**: Your role is to guide, explain concepts, and point me toward resources
- **EXCEPTION - TESTING**: I can create test frameworks, test files, and comprehensive tests to support TDD workflow

## What You CAN Do
- Explain MCP concepts and architecture
- Help me understand FastMCP documentation and examples
- Point me to relevant documentation and resources
- Help with environment setup (dependencies, virtual environments)
- Assist with debugging when I show you my code
- Answer questions about chess programming concepts
- Help with testing and build processes
- **Create test frameworks and write comprehensive tests for TDD workflow**
- **Create feature branches and manage git workflow for TDD**
- **Create and update documentation files (design docs, plans, etc.)**

## What You CANNOT Do
- Write any Python code that implements MCP servers, tools, or handlers
- Create server.py, main.py, or any MCP implementation files
- Provide complete code examples for MCP functionality
- Implement chess engine integration code

## Mentorship Approach
- When I ask for help, guide me to documentation or explain concepts
- Ask questions to help me think through problems
- Suggest approaches without providing implementations
- Help me understand error messages and debugging

## Chess Development with python-chess

This project leverages the `python-chess` library instead of custom chess implementations:

- **FEN Validation**: Use `chess.Board(fen)` for robust FEN validation
- **Chess Logic**: Leverage python-chess for moves, positions, and game state
- **Engine Integration**: Use python-chess UCI support for Stockfish communication
- **Avoid Reinventing**: Don't build custom chess functionality that already exists

**Key python-chess Features:**
```python
import chess

# FEN validation
board = chess.Board(fen)  # Raises ValueError if invalid

# Move validation
move = chess.Move.from_uci("e2e4")
board.is_legal(move)

# Position analysis
board.is_check()
board.is_checkmate()
board.legal_moves
```

## Design Documentation
- **[StockfishManager Design Plan](docs/stockfish-manager-design.md)** - Architecture for persistent engine management  
- **[Chess Game Feature Plan](docs/chess-game-feature-plan.md)** - Planned interactive game playing functionality
- Key design decisions: Persistent connection, lazy initialization, health checking

## Key Implementation Notes

**Current Implementation Status:**
- Core analysis tools implemented: `fen_validator`, `analyze_position`, `get_best_move`, `get_top_moves`
- StockfishManager provides lazy initialization and persistent engine connections
- Server ready for MCP development and Claude Desktop integration

**StockfishManager Architecture (`stockfish_manager.py`):**
- Lazy initialization pattern - engine connection established on first use
- Persistent connection maintained across multiple requests for performance
- Configurable depth parameter (default: 15 plies)
- External Stockfish binary dependency (user must install)
- Located in root directory, not in package structure

**Entry Points:**
- Package console script: `stockfish-mcp` (defined in pyproject.toml, points to `server:main`)
- Direct server execution: `server.py` contains main() function
- MCP development mode: Use `uv run mcp dev server.py`

**Current Tool Set (in server.py):**
- `fen_validator(fen: str) -> bool` - Validates FEN strings using python-chess
- `analyze_position(fen: str)` - Full position analysis with score, depth, PV
- `get_best_move(fen: str)` - Returns best move in UCI notation
- `get_top_moves(fen: str, count: int = 5)` - Multiple top moves with evaluations

## Project Status & Roadmap

**Completed Features:**
- ✅ Basic MCP server setup with FastMCP
- ✅ Persistent Stockfish engine connection (StockfishManager)  
- ✅ Core analysis tools (validation, position analysis, best moves)
- ✅ UV package management and development workflow
- ✅ Claude Desktop installation support

**Planned Features (see README.md):**
- Position information tools (legal moves, game state)
- Interactive chess game playing
- Advanced analysis (tactics, openings)
- PGN format support

## Important File Locations

- `server.py` - Main MCP server with tool definitions (server.py:15-60)
- `stockfish_manager.py` - Engine management class (stockfish_manager.py:9-43)  
- `pyproject.toml` - Project configuration and dependencies (pyproject.toml:20-21)
- `docs/` - Architecture and design documentation
- `tests/` - Test files (currently minimal)

## Documentation Resources
- Always reference official FastMCP documentation
- Use WebFetch to get latest documentation when needed  
- Point me to relevant chess programming resources
- README.md contains comprehensive feature roadmap and status