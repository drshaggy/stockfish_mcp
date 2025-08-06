# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a Stockfish MCP (Model Context Protocol) server built with FastMCP and Python. The architecture includes:

- **Package Structure**: Main implementation in `stockfish_mcp/` package
- **Server Entry Point**: `server.py` contains the FastMCP server instance and chess-api.com integration
- **Planned Backend Abstraction**: Designed to support switching between chess-api.com and local Stockfish binary
- **Dependencies**: FastMCP for MCP protocol, python-chess for chess logic, requests for API calls

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

## TDD Workflow
Our Test-Driven Development process follows this pattern:

1. **Feature Planning**: Discuss and define the feature requirements
2. **Branch Creation**: I create a new feature branch for the work
3. **Test Creation**: I create comprehensive tests that define the expected behavior
4. **Feature Development**: You implement the feature until all tests pass
5. **Integration**: I merge the feature branch once tests are satisfied

**Test Commands:**
```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=stockfish_mcp

# Run specific test file
uv run pytest tests/test_fen_validator.py

# Run specific test class
uv run pytest tests/test_fen_validator.py::TestFenValidator

# Run specific test method
uv run pytest tests/test_fen_validator.py::TestFenValidator::test_starting_position

# Run tests with verbose output
uv run pytest -v

# Run failing tests only
uv run pytest --lf

# Run tests and stop on first failure
uv run pytest -x

# Check test collection without running
uv run pytest --collect-only

# Run tests in watch mode (if available)
uv run pytest-watch
```

## Logging

The project includes MCP-compliant logging with sensitive data masking:

**Setup:**
```python
from stockfish_mcp.logger import get_logger

logger = get_logger(__name__)
```

**Usage:**
```python
# Basic logging
logger.info("Starting FEN validation")
logger.debug("Processing board position")
logger.warning("Invalid castling rights detected")
logger.error("Validation failed", extra={"error": str(e)})

# With structured data
logger.debug("Field validation", extra={"field": "board", "value_length": len(value)})
```

**Features:**
- Automatic sensitive data masking (API keys, tokens)
- Structured logging with timestamps and context
- Function names and line numbers included
- MCP-friendly output format

## Project Documentation

**Documentation Structure**: All project documentation (except README.md and CLAUDE.md) is stored in the `docs/` directory to maintain clean repository organization.

**Future Development Plans**: See [docs/pydantic-refactoring-plan.md](docs/pydantic-refactoring-plan.md) for comprehensive plan to enhance type safety using Pydantic models for validation and mypy for static type checking.

## Documentation Resources
- Always reference official FastMCP documentation
- Use WebFetch to get latest documentation when needed
- Point me to relevant chess programming resources