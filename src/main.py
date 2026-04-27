"""MCP server for Ramp API integration."""

import os
import asyncio
from dotenv import load_dotenv
from dedalus_mcp import MCPServer
from dedalus_mcp.server import TransportSecuritySettings
from dedalus_mcp.auth import Connection, SecretKeys

load_dotenv()

ramp_connection = Connection(
    name="ramp-mcp",
    secrets=SecretKeys(token="RAMP_TOKEN"),
    base_url="https://api.ramp.com/developer/v1",
    auth_header_format="Bearer {api_key}",
)


def create_server() -> MCPServer:
    as_url = os.getenv("DEDALUS_AS_URL", "https://as.dedaluslabs.ai")
    return MCPServer(
        name="ramp-mcp",
        connections=[ramp_connection],
        http_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
        streamable_http_stateless=True,
        authorization_server=as_url,
    )


async def main() -> None:
    from src.tools import tools

    server = create_server()
    for tool_func in tools:
        server.collect(tool_func)
    await server.serve(port=8080)


if __name__ == "__main__":
    asyncio.run(main())
