# Chess Game Playing Feature Plan

## Overview
Add interactive chess game playing capability to the Stockfish MCP server, allowing AI agents to play games against humans while maintaining game state.

## Architecture

### Core Components
- **GameState Class**: Manages board position, move history, game status, and color assignments
- **Server State**: Single `current_game` variable for active game persistence
- **Integration**: Leverage existing `StockfishManager` for AI move generation

### Design Philosophy
Tools provide mechanical functionality - agents handle interpretation and decision-making:
- Tools: Validate moves, update state, generate positions
- Agent: Interprets human requests, chooses difficulty, manages game flow

## New MCP Tools

### Game Setup
- **✅ `start_game(ai_color: str = "black", difficulty: int = 10, fen: str = None)`** - Initialize new game ✅ **IMPLEMENTED**
  - Parameters: "white" or "black" (AI's color), search depth (default: 10), optional custom starting position
  - Validates FEN if provided, creates GameState instance with dual-layer validation
  - Returns success status with AI color confirmation or error message for invalid FEN
  - Agent interprets human request and sets color and difficulty
  - Example: Human says "I'll play white at medium difficulty" → Agent calls `start_game("black", 12)`

- **`set_difficulty(depth: int)`** - Configure AI search depth
  - Parameters: Stockfish search depth (1-20)
  - Agent interprets difficulty requests ("easy" → depth 8, "hard" → depth 18)

### Game Play  
- **`record_opponent_move(move: str)`** - Record human's move
  - Parameters: Move in UCI format (e.g., "e2e4")
  - Validates move legality, updates game state
  - Like writing opponent's move on tournament scorecard

- **`make_move(move: str)`** - AI plays its move
  - Parameters: AI's chosen move in UCI format
  - Agent calls when ready to respond
  - Updates game state with AI move

- **`get_game_status()`** - View current game state
  - Returns: Board position (FEN), move history, whose turn, game status

- **`reset_game()`** - Clear current game state

## Natural Game Flow

**Setup:**
```
Human: "Let's play chess, you be white, play at medium difficulty"
Agent: [calls start_game("white", 12)]
Agent: [calls make_move("e2e4")] "I'll open with the King's pawn"
```

**Move Exchange:**
```
Human: "I'll play e5"  
Agent: [calls record_opponent_move("e7e5")]
Agent: "Good response! Let me think..." [calls make_move("g1f3")]
Agent: "I'll develop my knight to f3"
```

## Implementation Strategy

### GameState Class
```python
class GameState:
    - board: chess.Board (current position)
    - move_history: List[chess.Move] (chess.Move objects)  
    - ai_color: chess.Color (WHITE or BLACK)
    - difficulty: int (search depth)
    - current_player: chess.Color (whose turn it is)
```

## Implementation Status

### ✅ Completed Features
- **GameState Class**: Fully implemented with constructor-based initialization (`game_state.py`)
  - FEN validation using python-chess with clear error messages
  - Proper type annotations and dual-layer validation
  - Constructor accepts ai_color, difficulty, and optional custom FEN
- **start_game Tool**: Implemented in server.py with comprehensive error handling
  - Global game state management with `current_game` variable  
  - String-based AI color parameter ("black"/"white") for user-friendly MCP interface
  - Exception handling converts ValueError to user-friendly error responses
- **Server Integration**: Tool properly registered with FastMCP and ready for use

### 🔄 Next Implementation Priority
- `get_game_status()` - View current game state and position
- `record_opponent_move(move: str)` - Record and validate human moves
- `make_move()` - AI move generation using StockfishManager

### Tool Responsibilities
- **Mechanical only**: Validate inputs, update state, return results
- **No interpretation**: Tools don't decide difficulty meanings or color preferences
- **Error handling**: Return clear errors for invalid moves or game states

### Agent Responsibilities  
- **Interpretation**: Convert human language to tool parameters
- **Decision making**: Choose when to move, what difficulty to use
- **Game management**: Decide flow, provide commentary, handle edge cases

## Integration Notes

- **Shared Engine**: Reuse existing `StockfishManager` for move generation
- **Single Game**: One active game at a time initially  
- **In-Memory State**: Game persists while server runs
- **Clean Separation**: Game tools distinct from analysis tools

## Implementation Status

### Completed Features ✅
- ✅ **`start_game` Tool**: Initialize games with AI color, difficulty, custom positions
- ✅ **GameState Class**: Comprehensive game state management with FEN validation
- ✅ **Global Game Tracking**: Single active game management with proper state handling
- ✅ **Error Handling**: Invalid FEN detection and user-friendly error messages

### Testing Implementation ✅
- ✅ **Game State Testing**: Unit tests for GameState class initialization and validation
- ✅ **start_game Testing**: Complete testing of game initialization with various parameters
- ✅ **FEN Validation Testing**: Comprehensive coverage of valid/invalid position handling
- ✅ **Integration Testing**: End-to-end game setup workflows
- ✅ **Mock Testing**: MockGameState for reliable unit testing

### In Progress 🔄
- [ ] **`record_opponent_move`**: Accept and validate human player moves
- [ ] **`make_move`**: AI move generation and game state updates
- [ ] **`get_game_status`**: Board visualization and game state queries

## Future Enhancements
- Multiple concurrent games
- Game persistence across server restarts
- PGN import/export
- Time controls
- Opening book integration