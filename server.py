from urllib.parse import quote
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cats")

@mcp.tool()
def random_cat() -> str:
    """Return a random cat image URL."""
    return "https://cataas.com/cat"

@mcp.tool()
def cat_says(text: str) -> str:
    """Return a cat image URL with overlaid text."""
    return f"https://cataas.com/cat/says/{quote(text)}"

app = mcp.streamable_http_app()