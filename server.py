import os
from urllib.parse import quote
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cats")

@mcp.tool()
def random_cat() -> str:
    return "https://cataas.com/cat"

@mcp.tool()
def cat_says(text: str) -> str:
    return f"https://cataas.com/cat/says/{quote(text)}"

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
    )