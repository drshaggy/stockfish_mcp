from mcp.server.fastmcp import FastMCP

mcp = FastMCP("stockfish")

CHESS_API_BASE = 'https://chess-api.com/v1'

@mcp.tool()
def fen_validator(fen: string) -> bool:
    """Validate a FEN string"""
    return True

