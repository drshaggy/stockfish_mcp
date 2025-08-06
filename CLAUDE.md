# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a Stockfish MCP (Model Context Protocol) server built with FastMCP and Python. The architecture includes:

- **Package Structure**: Main implementation in `stockfish_mcp/` package
- **Server Entry Point**: `server.py` contains the FastMCP server instance
- **Engine Management**: StockfishManager class provides persistent connection to external Stockfish binary
- **Architecture Decision**: Persistent engine connection with lazy initialization for optimal performance
- **Dependencies**: FastMCP for MCP protocol, python-chess for chess logic and UCI communication
- **External Dependency**: Stockfish chess engine (user-installed)

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
```

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
- Key design decisions: Persistent connection, lazy initialization, health checking

## Documentation Resources
- Always reference official FastMCP documentation
- Use WebFetch to get latest documentation when needed
- Point me to relevant chess programming resources