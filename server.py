from urllib.parse import quote
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cats")

@mcp.tool()
def random_cat() -> str:
    return "https://cataas.com/cat"

@mcp.tool()
def cat_says(text: str) -> str:
    return f"https://cataas.com/cat/says/{quote(text)}"

app = mcp.streamable_http_app()