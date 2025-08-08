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
- **`start_game(ai_color: str, difficulty: int = 15)`** - Initialize new game
  - Parameters: "white" or "black" (agent's color), search depth (default: 15)
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
    - move_history: List[str] (UCI moves)  
    - ai_color: chess.Color (WHITE or BLACK)
    - difficulty: int (search depth)
    - game_status: str (active, checkmate, stalemate, draw)
```

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

## Future Enhancements
- Multiple concurrent games
- Game persistence across server restarts
- PGN import/export
- Time controls
- Opening book integration