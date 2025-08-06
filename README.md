# Stockfish MCP Server

A Model Context Protocol (MCP) server that provides chess analysis and position evaluation using Stockfish engine capabilities.

## Overview

This MCP server offers chess analysis tools that can be used by MCP-compatible clients. It's designed with a flexible backend architecture that currently supports chess-api.com integration with plans to add direct Stockfish binary support.

## Implementation Status

### Core Chess Tools
- [x] **`validate_fen`** - Validate FEN position strings (partial implementation)
- [ ] **`analyze_position`** - Get position evaluation and analysis 
- [ ] **`get_best_move`** - Find the best move for a position
- [ ] **`get_top_moves`** - Get multiple good moves ranked by strength

### Position Information Tools
- [ ] **`position_info`** - Basic position details (turn, castling rights, en passant, etc.)
- [ ] **`is_legal_move`** - Check if a move is legal in a position
- [ ] **`make_move`** - Apply a move and return the new position

### Advanced Analysis Tools
- [ ] **`evaluate_move`** - Analyze a specific move's strength
- [ ] **`find_tactics`** - Look for tactical opportunities (pins, forks, etc.)
- [ ] **`opening_name`** - Identify the opening being played

### Utility Tools
- [ ] **`fen_to_pgn`** - Convert positions to PGN format
- [ ] **`pgn_to_fen`** - Extract FEN from PGN

### Current Status
- [x] **Basic MCP server setup** - Server runs and exposes tools
- [x] **Development environment** - UV package management configured
- [x] **Test-Driven Development** - Pytest framework with comprehensive test suite
- [x] **Logging system** - MCP-compliant logging with sensitive data masking
- [ ] **Chess-api.com integration** - Backend API integration
- [ ] **Stockfish binary support** - Local engine integration

## Architecture

The server is built with a flexible backend abstraction layer:

- **Current**: chess-api.com integration for remote Stockfish analysis (planned)
- **Future**: Direct Stockfish binary integration for local analysis
- **Framework**: Official MCP Python SDK with FastMCP
- **Chess Logic**: python-chess for position validation and manipulation

## Requirements

- Python 3.10+
- UV package manager

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd stockfish_mcp

# Install dependencies
uv sync
```

## Development

```bash
# Run the MCP server in development mode
uv run mcp dev server.py

# Add new dependencies
uv add package-name

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=stockfish_mcp
```

## Logging

The project includes MCP-compliant logging with automatic sensitive data masking:

```python
from stockfish_mcp.logger import get_logger

logger = get_logger(__name__)

# Basic logging
logger.info("Starting FEN validation")
logger.debug("Processing board position")
logger.error("Validation failed", extra={"error": str(e)})

# With structured context
logger.debug("Field validation", extra={"field": "board", "length": len(value)})
```

**Features:**
- Automatic masking of sensitive data (API keys, tokens)
- Structured logging with timestamps and function context
- MCP-friendly output format
- Configurable log levels

## Current Tools

Currently implemented tools:
- **`add`** - Basic test tool (adds two numbers)

*Chess-specific tools are planned and will be implemented incrementally.*

## License

MIT License - see LICENSE file for details