# Stockfish MCP Server

A Model Context Protocol (MCP) server that provides chess analysis and position evaluation using Stockfish engine capabilities.

## Overview

This MCP server offers chess analysis tools that can be used by MCP-compatible clients. It's designed with a flexible backend architecture that currently supports chess-api.com integration with plans to add direct Stockfish binary support.

## Implementation Status

### Core Chess Tools
- [x] **`fen_validator`** - Validate FEN position strings using python-chess
- [x] **`analyze_position`** - Get position evaluation and analysis via persistent Stockfish connection 
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
- [x] **Stockfish binary support** - Local engine integration with persistent connection
- [x] **StockfishManager implementation** - Engine lifecycle management with lazy initialization

## Architecture

The server is built with a persistent Stockfish engine architecture:

- **Engine Integration**: External Stockfish binary via python-chess UCI interface
- **Connection Management**: Persistent engine connection with lazy initialization for optimal performance
- **Framework**: Official MCP Python SDK with FastMCP
- **Chess Logic**: python-chess library for all chess operations (validation, moves, analysis)

### Design Documents
- [StockfishManager Design Plan](docs/stockfish-manager-design.md) - Detailed architecture for engine management

## Requirements

- Python 3.10+
- UV package manager
- Stockfish chess engine (external dependency)

### Installing Stockfish

```bash
# macOS
brew install stockfish

# Ubuntu/Debian
sudo apt install stockfish

# Windows
# Download from https://stockfishchess.org
```

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
```

## Implemented Tools

### Chess Analysis Tools
- **`fen_validator(fen: str)`** - Validates FEN position strings using python-chess library
- **`analyze_position(fen: str)`** - Analyzes chess positions using Stockfish engine
  - Returns comprehensive analysis including position evaluation, best moves, search depth, and principal variation
  - Uses persistent Stockfish connection for optimal performance
  - Configurable analysis depth (default: 15)

## License

MIT License - see LICENSE file for details