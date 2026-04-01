# Ramp MCP Server

A MCP server for integrating with the Ramp API, built with the [dedalus_mcp](https://docs.dedaluslabs.ai/dmcp) framework. Authentication is handled by **DAuth** (Dedalus Auth) — the server never sees raw API credentials.

## Prerequisites

- Python 3.10 or higher
- A Ramp account with API access
- Ramp API Bearer token (`RAMP_TOKEN`) passed via DAuth when connecting to the server

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd ramp-mcp
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

   Or if using `uv`:
   ```bash
   uv pip install -e .
   ```

## Configuration

### Environment Variables

Copy the example and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|----------|-------------|
| `DEDALUS_AS_URL` | Dedalus authorization server URL (default: `https://as.dedaluslabs.ai`) |
| `DEDALUS_API_KEY` | Your Dedalus platform API key |
| `DEDALUS_API_URL` | Dedalus API URL (default: `https://api.dedaluslabs.ai`) |
| `RAMP_TOKEN` | Your Ramp API Bearer token (passed by the client via DAuth) |

### Authentication (DAuth)

The server receives the Ramp Bearer token (`RAMP_TOKEN`) via Dedalus Auth. When a client connects, it provides this secret through DAuth; the server uses `ctx.dispatch()` to route all API calls through the DAuth enclave. The token is never exposed to server code.

## Available Tools

All tools make authenticated requests through DAuth. Each tool accepts optional `limit` and `start` parameters for pagination.

### Core Tools

| Tool | Description | Scope |
|------|-------------|-------|
| `read_transaction` | Read transactions | `transactions:read` |
| `read_merchant` | Read merchants (filterable by `merchant_name`) | `merchants:read` |
| `read_reimbursement` | Read reimbursements | `reimbursements:read` |
| `read_user` | Read users (filterable by `user_name`) | `users:read` |
| `read_card` | Read cards | `cards:read` |
| `read_bill` | Read bills | `bills:read` |
| `read_receipt` | Read receipts | `receipts:read` |
| `read_limit` | Read spending limits | `limits:read` |
| `read_vendor` | Read vendors (filterable by `vendor_name`) | `vendors:read` |
| `read_department` | Read departments | `departments:read` |
| `read_location` | Read locations | `locations:read` |

### Financial Tools

| Tool | Description | Scope |
|------|-------------|-------|
| `read_cashback` | Read cashbacks | `cashbacks:read` |
| `read_statement` | Read statements | `statements:read` |
| `read_transfer` | Read transfers | `transfers:read` |
| `read_business` | Read business information | `business:read` |
| `read_repayment` | Read repayments | `repayments:read` |
| `read_treasury` | Read treasury information | `treasury:read` |

### Administrative Tools

| Tool | Description | Scope |
|------|-------------|-------|
| `read_spend_program` | Read spend programs | `spend_programs:read` |
| `read_trip` | Read trips | `trips:read` |
| `read_accounting` | Read accounting information | `accounting:read` |
| `read_bank_account` | Read bank accounts | `bank_accounts:read` |
| `read_bank_feed` | Read bank feeds | `bank_feeds:read` |
| `read_memo` | Read memos | `memos:read` |
| `read_purchase_order` | Read purchase orders | `purchase_orders:read` |
| `read_receipt_integration` | Read receipt integrations | `receipt_integrations:read` |
| `read_item_receipt` | Read item receipts | `item_receipts:read` |
| `read_entity` | Read entities | `entities:read` |
| `read_external_attendee` | Read external attendees | `external_attendees:read` |
| `read_lead` | Read leads | `leads:read` |
| `read_attendee_type` | Read attendee types | `attendee_types:read` |
| `read_audit_log` | Read audit logs | `audit_logs:read` |
| `read_custom_record` | Read custom records | `custom_records:read` |

## Running the Server

Start the MCP server:

```bash
python -m src.main
```

The server starts on port 8080. Verify with the test client:

```bash
python -m src.client
```

Update `src/client.py` to call your tools by name with the correct arguments.

## Project Structure

```
ramp-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py          # MCP server entry point and DAuth connection
│   ├── tools.py         # Ramp API tool implementations
│   └── client.py        # Test client for verifying tools
├── .env.example         # Environment variable template
├── pyproject.toml       # Project configuration and dependencies
├── LICENSE
└── README.md
```

## Security Notes

- **Never commit `.env`** to version control
- All API calls go through the DAuth enclave — your server code never touches raw credentials
- Rotate your credentials if they are ever compromised

## Additional Resources

- [Ramp API Documentation](https://docs.ramp.com/developer-api/v1/getting-started)
- [Ramp API OpenAPI Spec](https://docs.ramp.com/openapi/developer-api.json)
- [Ramp API Plain Text Docs](https://docs.ramp.com/llms.txt)
- [Dedalus MCP docs](https://docs.dedaluslabs.ai/dmcp)
- [DAuth launch blog post](https://www.dedaluslabs.ai/blog/dedalus-auth-launch)

## License

See LICENSE file for details.
