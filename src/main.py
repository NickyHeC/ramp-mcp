"""MCP server for Ramp API integration."""
import asyncio
import sys
import os

from dedalus_mcp import MCPServer

# Import tools - handle both installed package and direct execution
try:
    # Try absolute import (works when package is installed)
    from tools import ramp_tools
except ImportError:
    # Fallback: add parent directory to path and import from src
    _parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _parent_dir not in sys.path:
        sys.path.insert(0, _parent_dir)
    from src.tools import ramp_tools


# --- Server ---

server = MCPServer(name="ramp-mcp")


async def main() -> None:
    """Run the MCP server."""
    for tool in ramp_tools:
        server.collect(tool)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
