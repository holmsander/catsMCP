import contextlib
import os
from urllib.parse import quote

import uvicorn
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

mcp = FastMCP(
    "cats",
    stateless_http=True,
    json_response=True,
    streamable_http_path="/",
)

@mcp.tool()
def random_cat() -> str:
    """Return a random cat image URL."""
    return "https://cataas.com/cat"

@mcp.tool()
def cat_says(text: str) -> str:
    """Return a cat image URL with overlaid text."""
    return f"https://cataas.com/cat/says/{quote(text)}"

async def root(request):
    return JSONResponse(
        {
            "ok": True,
            "name": "cats",
            "mcp_endpoint": "/mcp",
        }
    )

@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with mcp.session_manager.run():
        yield

app = Starlette(
    routes=[
        Route("/", root),
        Mount("/mcp", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )