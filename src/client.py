"""Test client for the Ramp MCP server.

Uses ConnectionTester from dedalus_mcp to test the Ramp DAuth connection
locally — makes real HTTP requests with the connection's auth config,
without needing to run the full MCP server or DAuth enclave.

Usage:
    1. Ensure RAMP_TOKEN is set in your .env file
    2. Run:  python -m src.client
"""

import asyncio
from dotenv import load_dotenv
from dedalus_mcp.testing import ConnectionTester, TestRequest

from src.main import ramp_connection

load_dotenv()


async def main() -> None:
    tester = ConnectionTester.from_env(ramp_connection)

    print(f"Testing connection: {tester.connection.name}")
    print(f"Base URL: {tester.base_url}\n")

    ok = await tester.ping("/transactions?limit=1")
    print(f"Ping /transactions: {'OK' if ok else 'FAILED'}\n")

    if not ok:
        print("Connection failed — check that RAMP_TOKEN is valid.")
        return

    print("--- read_transaction (limit=3) ---")
    resp = await tester.request(TestRequest(path="/transactions", params={"limit": 3}))
    print(f"Status: {resp.status}")
    if resp.success and resp.body:
        items = resp.body.get("data", []) if isinstance(resp.body, dict) else []
        print(f"Returned {len(items)} transaction(s)")
        for txn in items[:3]:
            print(f"  - {txn.get('merchant_name', 'N/A')}: ${txn.get('amount', 0):.2f}")
    else:
        print(f"Error: {resp.body}")

    print("\n--- read_user (limit=3) ---")
    resp = await tester.request(TestRequest(path="/users", params={"limit": 3}))
    print(f"Status: {resp.status}")
    if resp.success and resp.body:
        items = resp.body.get("data", []) if isinstance(resp.body, dict) else []
        print(f"Returned {len(items)} user(s)")
        for user in items[:3]:
            name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
            print(f"  - {name or 'N/A'} ({user.get('email', 'N/A')})")
    else:
        print(f"Error: {resp.body}")

    print("\n--- read_department ---")
    resp = await tester.request(TestRequest(path="/departments"))
    print(f"Status: {resp.status}")
    if resp.success and resp.body:
        items = resp.body.get("data", []) if isinstance(resp.body, dict) else []
        print(f"Returned {len(items)} department(s)")
        for dept in items[:5]:
            print(f"  - {dept.get('name', 'N/A')}")
    else:
        print(f"Error: {resp.body}")

    print("\nAll connection tests complete.")


if __name__ == "__main__":
    asyncio.run(main())
