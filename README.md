# Ramp MCP Server

A Micro-Capability Platform (MCP) server for integrating with the Ramp API. This server provides tools to read transactions, merchants, reimbursements, and users from your Ramp account.

## Prerequisites

- Python 3.10 or higher
- A Ramp account with API access
- Ramp API credentials (RAMP_ID and RAMP_SEC)

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

### Getting Your Ramp API Credentials

1. Visit the [Ramp API Getting Started Guide](https://docs.ramp.com/developer-api/v1/getting-started) to learn how to obtain your API credentials.

2. In your Ramp developer dashboard, you'll find:
   - **RAMP_ID**: Your Ramp API client ID
   - **RAMP_SEC**: Your Ramp API client secret

### Setting Up Credentials

1. Create a `credentials.txt` file in the project root directory (this file is not included in the repository for security reasons).

2. Add your Ramp API credentials in the following format:
   ```
   # Ramp API Credentials
   # Please replace the values below with your own RAMP_ID and RAMP_SEC
   # You can find these in your Ramp developer dashboard

   RAMP_ID=your_ramp_id_here
   RAMP_SEC=your_ramp_secret_here
   ```

3. Replace `your_ramp_id_here` and `your_ramp_secret_here` with your actual credentials from your Ramp developer dashboard.

4. **Important**: Never commit `credentials.txt` to version control. This file is already included in `.gitignore` and should remain local and secure.

## Available Tools

The MCP server provides the following tools:

### `read_transaction`
Read transactions from your Ramp account.

- **Parameters**:
  - `number_of_transactions` (optional, int): Number of transactions to retrieve (default: 5)
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

Test the transaction reading functionality:

```bash
python test_transactions.py
```

This will fetch and display the most recent transactions in a readable text format.

## Project Structure

```
ramp-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py          # MCP server entry point
│   └── tools.py         # Ramp API tool implementations
├── credentials.txt       # Your Ramp API credentials (not committed)
├── get_token.py         # Utility script for token management
├── test_transactions.py # Test script for transactions
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

- **Never commit `credentials.txt`** to version control
- Keep your API credentials secure and private
- Rotate your credentials if they are ever compromised
- Use environment variables or secure credential management in production environments

## Troubleshooting

### Credentials Not Found
If you see an error about missing credentials:
- Create `credentials.txt` in the project root directory if it doesn't exist
- Ensure the file follows the format shown in the Configuration section above
- Verify the file contains `RAMP_ID=` and `RAMP_SEC=` lines with your actual credentials
- Check that there are no extra spaces or quotes around the values
- Make sure the file is in the project root directory (same level as `pyproject.toml`)

### Authentication Errors
If you encounter authentication errors:
- Verify your credentials are correct in `credentials.txt`
- Ensure your Ramp API credentials are active in your developer dashboard
- Check that the required scopes are enabled for your API credentials

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
