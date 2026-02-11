# Ramp MCP Server

A Micro-Capability Platform (MCP) server for integrating with the Ramp API. This server provides tools to read transactions, merchants, reimbursements, and users from your Ramp account.

## Prerequisites

- Python 3.10 or higher
- A Ramp account with API access
- Ramp API Bearer token (RAMP_TOKEN) passed via **Dedalus Auth (DAuth)** when connecting to the server

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

### Authentication (DAuth)

The server is configured to receive **the Ramp Bearer token (RAMP_TOKEN) via Dedalus Auth**. When a client connects, it provides this secret through DAuth; the server uses it to call the Ramp API on behalf of that client. The token is not read from the server environment or `.env` for tool execution when DAuth is used.

- **RAMP_TOKEN**: Your Ramp API Bearer token (passed by the client via DAuth)

Optional: You can keep a `.env` file (e.g. from `.env.example`) for local reference or for use by the client; do not commit `.env` to version control.

## Available Tools

The MCP server provides the following tools:

### `read_transaction`
Read transactions from your Ramp account. Requires scope: `transactions:read`.

- **Parameters**:
  - `limit` (optional, int): Number of transactions to retrieve
  - `start` (optional, str): Transaction ID to start pagination from

### `read_merchant`
Read merchant information filtered by merchant name.

- **Parameters**:
  - `merchant_name` (required, str): Name of the merchant to search for
  - `limit` (optional, int): Maximum number of results to return
  - `start` (optional, str): Merchant ID to start pagination from

### `read_reimbursement`
Read reimbursements from your Ramp account.

- **Parameters**:
  - `number_of_reimbursements` (optional, int): Number of reimbursements to retrieve (default: 5)
  - `start` (optional, str): Reimbursement ID to start pagination from

### `read_user`
Read user information filtered by user name.

- **Parameters**:
  - `user_name` (required, str): Name of the user to search for
  - `limit` (optional, int): Maximum number of results to return
  - `start` (optional, str): User ID to start pagination from

## Running the Server

Start the MCP server:

```bash
python src/main.py
```

The server will start on port 8080 by default. You can connect to it using an MCP client.

## Testing

Tools run in the MCP request context and require the Ramp token from the client via DAuth. To test:

1. Start the server: `python src/main.py`
2. Connect with an MCP client that sends the Ramp token (RAMP_TOKEN) through DAuth, then call tools (e.g. `read_transaction` with `limit` and optional `start`).

The script `test_transactions.py` is a standalone formatter example; it does not run the tools without a full MCP/DAuth context.

## Project Structure

```
ramp-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py          # MCP server entry point
│   └── tools.py         # Ramp API tool implementations
├── .env                  # Optional local / client credential reference (not committed)
├── .env.example          # Template for .env (DAuth client credentials)
├── test_transactions.py  # Example formatter (tools require MCP/DAuth context)
├── pyproject.toml       # Project configuration and dependencies
└── README.md            # This file
```

## API Scopes

The following OAuth scopes are used by the tools:

- `transactions:read` - For reading transactions
- `merchants:read` - For reading merchant information
- `reimbursements:read` - For reading reimbursements
- `users:read` - For reading user information

Make sure your Ramp API credentials have the necessary scopes enabled in your Ramp developer dashboard.

## Security Notes

- **Never commit `.env`** to version control
- Keep your API credentials secure and private
- Rotate your credentials if they are ever compromised
- Use environment variables or secure credential management in production environments

## Troubleshooting

### Credentials / DAuth
- Credentials are provided by the **client** via Dedalus Auth when connecting to the server.
- Ensure your MCP client is configured to send RAMP_TOKEN through DAuth for the Ramp connection.
- Verify required scopes are enabled for your Ramp API credentials in the Ramp developer dashboard.

### Authentication Errors
- Confirm the client is sending a valid Ramp token (RAMP_TOKEN) through DAuth.
- Check that the required scopes are enabled for your API credentials in the Ramp developer dashboard.

### Import Errors
If you see import errors for `dedalus_mcp`, `pydantic`, or `httpx`:
- Run `pip install -e .` to install all dependencies
- Ensure you're using Python 3.10 or higher

## Additional Resources

- [Ramp API Documentation](https://docs.ramp.com/developer-api/v1/getting-started)
- [Ramp API OpenAPI Spec](https://docs.ramp.com/openapi/developer-api.json)
- [Ramp API Plain Text Docs](https://docs.ramp.com/llms.txt)

## License

See LICENSE file for details.
