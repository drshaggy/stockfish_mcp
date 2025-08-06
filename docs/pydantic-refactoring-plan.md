# Pydantic-Based Type Strict Refactoring Plan

## Overview

This document outlines the plan to refactor the Stockfish MCP server to use Pydantic models for enhanced type safety, better validation, and cleaner code architecture.

## Current State

- Manual validation logic in `FenValidator` class
- Limited type annotations across the codebase
- No static type checking configuration
- Manual error handling and validation

## Refactoring Goals

- Leverage Pydantic for runtime type validation and static type safety
- Replace manual validation with declarative Pydantic models
- Enable strict type checking with mypy
- Improve error handling and user feedback

## Implementation Plan

### Phase 1: Create Pydantic Models

Create `stockfish_mcp/models.py` with type-strict Pydantic models:

- **`FenString`** model with parsed FEN fields:
  - `board: str` - board position (8 ranks separated by '/')
  - `active_color: Literal['w', 'b']` - whose turn it is
  - `castling: str` - castling availability (KQkq format)
  - `en_passant: str` - en passant target square or '-'
  - `halfmove: int` - halfmove clock for 50-move rule
  - `fullmove: int` - fullmove number

- **`ChessPosition`** model for validated chess positions
- Use `Literal` types for constrained values (colors, pieces)
- Use `Field()` for validation constraints and documentation

### Phase 2: Add Custom Validators

Migrate existing validation logic to Pydantic field validators:

- **Board validation** → `@field_validator('board')`
  - Validate 8 ranks separated by '/'
  - Validate each rank has exactly 8 squares
  - Validate piece characters and empty square numbers

- **En passant validation** → `@field_validator('en_passant')`
  - Must be '-' or valid square notation
  - If square, must be on rank 3 or 6

- **Castling rights validation** → custom validator
  - Must be combination of 'KQkq' characters or '-'

- **Move counters validation** → built-in int validators with constraints

### Phase 3: Refactor FenValidator Class

Update the existing `FenValidator` class to use Pydantic:

- Replace manual parsing/validation with Pydantic model instantiation
- Update `validate()` method to use Pydantic parsing
- Update `is_valid()` to catch `ValidationError` instead of custom exceptions
- Update `get_validation_errors()` to return structured Pydantic error details
- Maintain backward compatibility with existing interface

### Phase 4: Update Server Integration

Modify `server.py` to leverage Pydantic models:

- Update MCP tool definitions with proper Pydantic type hints
- Use Pydantic models for request/response validation
- Leverage automatic JSON schema generation for MCP protocol
- Improve error responses with structured validation details

### Phase 5: Add Type Checking Infrastructure

Configure comprehensive type checking:

- Add mypy to dev dependencies in `pyproject.toml`
- Configure mypy with strict settings:
  ```toml
  [tool.mypy]
  python_version = "3.10"
  strict = true
  disallow_untyped_defs = true
  disallow_any_generics = true
  warn_return_any = true
  strict_optional = true
  ```
- Add type checking commands to `CLAUDE.md`
- Ensure all code passes strict type validation

## Benefits

### Type Safety
- Runtime type validation with automatic coercion
- Full static type checking with mypy integration
- IDE support with better autocomplete and error detection

### Code Quality
- Declarative model definitions instead of imperative validation
- Reduced boilerplate code
- Better separation of concerns

### Error Handling
- Structured, detailed error messages
- Multiple validation errors collected and reported together
- JSON-serializable error details for API responses

### Integration
- Seamless integration with FastMCP and MCP protocol
- Automatic JSON schema generation
- Easy serialization/deserialization

## Migration Strategy

1. **Incremental**: Implement Pydantic models alongside existing validation
2. **Backward Compatible**: Maintain existing `FenValidator` interface
3. **Test-Driven**: Create comprehensive tests for new models
4. **Gradual Adoption**: Update server integration piece by piece

## Success Criteria

- [ ] All existing tests pass with new Pydantic-based validation
- [ ] Full mypy type checking passes in strict mode
- [ ] Better error messages for invalid FEN strings
- [ ] Improved code maintainability and readability
- [ ] Documentation updated with new patterns and practices

## Timeline

This refactoring can be implemented incrementally over multiple development sessions, with each phase building on the previous one while maintaining system functionality.