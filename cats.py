from urllib.parse import quote
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cats")

@mcp.tool()
def random_cat() -> str:
    """Return a random cat URL."""
    return "https://cataas.com/cat"

@mcp.tool()
def cat_says(text: str) -> str:
    """Return a cat-with-text URL."""
    return f"https://cataas.com/cat/says/{quote(text)}"

if __name__ == "__main__":
    mcp.run()

    #.venv\Scripts\activate
