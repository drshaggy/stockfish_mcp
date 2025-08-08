# Stockfish MCP Server

A Model Context Protocol (MCP) server that provides chess analysis and position evaluation using Stockfish engine capabilities.

## Overview

This MCP server provides comprehensive chess capabilities including position analysis and interactive game playing. AI agents can analyze chess positions, get move recommendations, and play full games against human opponents using Stockfish engine integration.

## Implementation Status

### Core Chess Tools
- [x] **`fen_validator`** - Validate FEN position strings using python-chess
- [x] **`analyze_position`** - Get position evaluation and analysis via persistent Stockfish connection 
- [x] **`get_best_move`** - Find the best move for a position
- [x] **`get_top_moves`** - Get multiple good moves ranked by strength

### Position Information Tools
- [ ] **`position_info`** - Basic position details (turn, castling rights, en passant, etc.)
- [ ] **`is_legal_move`** - Check if a move is legal in a position
- [ ] **`make_move`** - Apply a move and return the new position

### Chess Game Playing Tools
- [ ] **`start_game`** - Initialize new game with AI color and difficulty selection
- [ ] **`record_opponent_move`** - Record and validate human player's move  
- [ ] **`make_move`** - AI plays its move in the current game
- [ ] **`get_game_status`** - View current board position and game state
- [ ] **`set_difficulty`** - Configure AI playing strength
- [ ] **`reset_game`** - Clear current game state

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
- [Chess Game Feature Plan](docs/chess-game-feature-plan.md) - Architecture for interactive game playing functionality

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

## Installation to Claude Desktop

To install this MCP server for use with Claude Desktop:

```bash
# Install the server to Claude Desktop with dependencies
uv run mcp install server.py --name stockfish --with python-chess

# Alternative: Include all project dependencies
uv run mcp install server.py --name stockfish --with python-chess --with pydantic
```

**Important:** Use the `--with` flag to include project dependencies in the MCP environment. Without this, Claude Desktop won't have access to required packages like `python-chess`.

This command registers the server with Claude Desktop, making the chess analysis tools available in your Claude conversations.

## Implemented Tools

### Chess Analysis Tools
- **`fen_validator(fen: str)`** - Validates FEN position strings using python-chess library
- **`analyze_position(fen: str)`** - Analyzes chess positions using Stockfish engine
  - Returns comprehensive analysis including position evaluation, best moves, search depth, and principal variation
  - Uses persistent Stockfish connection for optimal performance
  - Configurable analysis depth (default: 15)
- **`get_best_move(fen: str)`** - Gets the best move for a position
  - Returns the strongest move in UCI notation (e.g., "e2e4")
  - Uses Stockfish engine with configurable depth
  - Leverages persistent connection for fast response times
- **`get_top_moves(fen: str, count: int = 5)`** - Gets multiple best moves ranked by strength
  - Returns list of top moves with evaluations using Stockfish MultiPV
  - Each move includes UCI notation, centipawn score, and search depth
  - Configurable count parameter (default: 5 moves)
  - Uses persistent connection for optimal performance

## License

MIT License - see LICENSE file for details