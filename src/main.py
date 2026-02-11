"""MCP server for Ramp API integration."""
import asyncio
import sys
import os
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.auth import Connection, SecretKeys

# Load environment variables from .env file
load_dotenv()

# Ramp connection: Bearer token is passed via DAuth from the client
ramp_connection = Connection(
    name="ramp",
    secrets=SecretKeys(token="RAMP_TOKEN"),
    base_url="https://api.ramp.com/developer/v1",
    auth_header_format="Bearer {api_key}",
)

server = MCPServer(
    name="ramp-mcp",
    connections=[ramp_connection],
    authorization_server=os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai"),
    streamable_http_stateless=True,
)

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


async def main() -> None:
    """Run the MCP server."""
    for tool in ramp_tools:
        server.collect(tool)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
