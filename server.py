import os
from fastmcp import FastMCP
import httpx

mcp = FastMCP(
    name="Cat MCP",
    instructions=(
        "Use the get_cat tool when the user asks for a cat picture. "
        "Return the image URL and a short description."
    ),
)


@mcp.tool()
async def get_cat() -> dict:
    """Get a random cat picture from cataas.com."""
    api_url = "https://cataas.com/cat?json=true"

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()

    # cataas usually returns a relative path like "/cat/abc123"
    path = data.get("url") or data.get("_id")

    if isinstance(path, str) and path.startswith("/"):
        image_url = f"https://cataas.com{path}"
    elif isinstance(path, str):
        image_url = f"https://cataas.com/cat/{path}"
    else:
        image_url = "https://cataas.com/cat"

    tags = data.get("tags", [])

    return {
        "title": "Random cat",
        "image_url": image_url,
        "source": "https://cataas.com/",
        "tags": tags,
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    # Simple and matches OpenAI's MCP examples closely.
    mcp.run(transport="sse", host="0.0.0.0", port=port)