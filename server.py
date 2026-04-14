import os
import contextlib
from urllib.parse import quote

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cats")

@mcp.tool()
def random_cat() -> str:
    return "https://cataas.com/cat"

@mcp.tool()
def cat_says(text: str) -> str:
    return f"https://cataas.com/cat/says/{quote(text)}"

# ✅ health check so Railway doesn't think it's dead
async def root(request):
    return JSONResponse({"ok": True})

# ✅ REQUIRED for proper MCP HTTP handling
@contextlib.asynccontextmanager
async def lifespan(app):
    async with mcp.session_manager.run():
        yield

app = Starlette(
    routes=[
        Route("/", root),  # important!
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