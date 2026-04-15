import os
import httpx
from fastmcp import FastMCP

mcp = FastMCP(
    name="Cat MCP",
    instructions="Use get_cat when the user asks for a cat picture.",
)

@mcp.tool()
async def get_cat() -> str:
    """Get a random cat image URL from cataas.com."""
    api_url = "https://cataas.com/cat?json=true"

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()

    raw_url = data.get("url")
    cat_id = data.get("_id") or data.get("id")

    if isinstance(raw_url, str) and raw_url.startswith("http"):
        image_url = raw_url
    elif isinstance(raw_url, str) and raw_url.startswith("/"):
        image_url = f"https://cataas.com{raw_url}"
    elif isinstance(cat_id, str):
        image_url = f"https://cataas.com/cat/{cat_id}"
    else:
        image_url = "https://cataas.com/cat"

    return image_url

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    mcp.run(transport="sse", host="0.0.0.0", port=port)