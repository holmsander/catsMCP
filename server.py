import os
import httpx
from fastmcp import FastMCP
from fastmcp.utilities.types import Image

mcp = FastMCP(
    name="Cat MCP",
    instructions="Use get_cat when the user asks for a cat picture.",
)

@mcp.tool()
async def get_cat():
    """Get a random cat image and return it as actual image content."""
    api_url = "https://cataas.com/cat?json=true"

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        meta_resp = await client.get(api_url)
        meta_resp.raise_for_status()
        data = meta_resp.json()

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

        img_resp = await client.get(image_url)
        img_resp.raise_for_status()

    content_type = img_resp.headers.get("content-type", "").lower()
    if "png" in content_type:
        fmt = "png"
    elif "webp" in content_type:
        fmt = "webp"
    elif "gif" in content_type:
        fmt = "gif"
    else:
        fmt = "jpeg"

    return Image(data=img_resp.content, format=fmt)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    mcp.run(transport="sse", host="0.0.0.0", port=port)