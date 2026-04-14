import os
import contextlib
from urllib.parse import quote

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route
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

async def root(request):
    return JSONResponse({
        "ok": True,
        "name": "cats",
        "streamable_http": "/mcp",
        "sse": "/sse",
    })

@contextlib.asynccontextmanager
async def lifespan(app):
    async with mcp.session_manager.run():
        yield

app = Starlette(
    routes=[
        Route("/", root),
        Mount("/mcp", app=mcp.streamable_http_app()),
        Mount("/sse", app=mcp.sse_app()),
    ],
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )