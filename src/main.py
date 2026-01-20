"""MCP server for Ramp API integration."""
import asyncio

from dedalus_mcp import MCPServer

from tools import ramp_tools


# --- Server ---

server = MCPServer(name="ramp-mcp")


async def main() -> None:
    """Run the MCP server."""
    for tool in ramp_tools:
        server.collect(tool)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
