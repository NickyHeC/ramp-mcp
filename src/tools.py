# tools.py - Ramp API tools
#
# The Ramp Bearer token (RAMP_TOKEN) is provided via DAuth or server env and
# used directly for all API calls.
import os
from urllib.parse import urlencode
import httpx
from dedalus_mcp import tool, Context
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Optional: load .env for local/dev when token is passed via env
try:
    from dotenv import load_dotenv
    _project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(_project_root, ".env"))
except Exception:
    pass

RAMP_BASE_URL = "https://api.ramp.com/developer/v1"


async def _get_ramp_token(ctx: Context) -> str:
    """Get RAMP_TOKEN from context (resolve_client) or env. Use in tools."""
    try:
        resolver = ctx.resolver
        if resolver is not None:
            auth = ctx.auth_context
            if auth and getattr(auth, "claims", None):
                connections = (auth.claims or {}).get("ddls:connections") or {}
                if isinstance(connections, dict) and connections:
                    handle = next(iter(connections.values()))
                    client = await ctx.resolve_client(handle)
                    if isinstance(client, str):
                        return client
                    if hasattr(client, "token"):
                        return getattr(client, "token")
    except Exception:
        pass
    token = os.getenv("RAMP_TOKEN")
    if not token:
        raise ValueError(
            "Ramp token not available. Set RAMP_TOKEN in the environment, "
            "or connect via DAuth so the server can obtain it from the connection."
        )
    return token


def _path_with_params(base_path: str, params: dict) -> str:
    if not params:
        return base_path
    return f"{base_path}?{urlencode(params)}"


async def _ramp_get(ctx: Context, path: str, params: dict) -> dict:
    """Get RAMP_TOKEN and GET from Ramp API with Bearer auth."""
    token = await _get_ramp_token(ctx)
    full_path = _path_with_params(path, params)
    resp = httpx.get(
        f"{RAMP_BASE_URL}{full_path}",
        headers={"Authorization": f"Bearer {token}"},
    )
    resp.raise_for_status()
    result = resp.json()
    if isinstance(result, dict):
        return result
    raise RuntimeError(f"Unexpected response type: {type(result)}")


class TransactionResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read transactions from Ramp API", required_scopes=["transactions:read"])
async def read_transaction(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> TransactionResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/transactions", params)
    return TransactionResult(**result)


class MerchantResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read merchants from Ramp API", required_scopes=["merchants:read"])
async def read_merchant(
    ctx: Context,
    merchant_name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> MerchantResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/merchants", params)
    # Filter by merchant_name if provided
    if merchant_name and result.get("data"):
        filtered_data = [
            merchant for merchant in result["data"]
            if merchant_name.lower() in merchant.get("name", "").lower()
        ]
        result["data"] = filtered_data
    return MerchantResult(**result)


class ReimbursementResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read reimbursements from Ramp API", required_scopes=["reimbursements:read"])
async def read_reimbursement(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> ReimbursementResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/reimbursements", params)
    return ReimbursementResult(**result)


class UserResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read users from Ramp API", required_scopes=["users:read"])
async def read_user(
    ctx: Context,
    user_name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> UserResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/users", params)
    # Filter by user_name if provided
    if user_name and result.get("data"):
        filtered_data = [
            user for user in result["data"]
            if user_name.lower() in user.get("full_name", "").lower()
            or user_name.lower() in f"{user.get('first_name', '')} {user.get('last_name', '')}".lower()
        ]
        result["data"] = filtered_data
    return UserResult(**result)


# Generic result model for most endpoints
class GenericResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


# Cards
@tool(description="Read cards from Ramp API", required_scopes=["cards:read"])
async def read_card(
    ctx: Context,
    number_of_cards: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_cards}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/cards", params)
    if result.get("data") and number_of_cards:
        result["data"] = result["data"][:number_of_cards]
    return GenericResult(**result)


# Bills
@tool(description="Read bills from Ramp API", required_scopes=["bills:read"])
async def read_bill(
    ctx: Context,
    number_of_bills: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_bills}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/bills", params)
    if result.get("data") and number_of_bills:
        result["data"] = result["data"][:number_of_bills]
    return GenericResult(**result)


# Receipts
@tool(description="Read receipts from Ramp API", required_scopes=["receipts:read"])
async def read_receipt(
    ctx: Context,
    number_of_receipts: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_receipts}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/receipts", params)
    if result.get("data") and number_of_receipts:
        result["data"] = result["data"][:number_of_receipts]
    return GenericResult(**result)


# Limits
@tool(description="Read spending limits from Ramp API", required_scopes=["limits:read"])
async def read_limit(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/limits", params)
    return GenericResult(**result)


# Vendors
@tool(description="Read vendors from Ramp API", required_scopes=["vendors:read"])
async def read_vendor(
    ctx: Context,
    vendor_name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/vendors", params)
    if vendor_name and result.get("data"):
        filtered_data = [
            vendor for vendor in result["data"]
            if vendor_name.lower() in vendor.get("name", "").lower()
        ]
        result["data"] = filtered_data
    return GenericResult(**result)


# Departments
@tool(description="Read departments from Ramp API", required_scopes=["departments:read"])
async def read_department(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/departments", params)
    return GenericResult(**result)


# Locations
@tool(description="Read locations from Ramp API", required_scopes=["locations:read"])
async def read_location(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/locations", params)
    return GenericResult(**result)


# Cashbacks
@tool(description="Read cashbacks from Ramp API", required_scopes=["cashbacks:read"])
async def read_cashback(
    ctx: Context,
    number_of_cashbacks: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_cashbacks}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/cashbacks", params)
    if result.get("data") and number_of_cashbacks:
        result["data"] = result["data"][:number_of_cashbacks]
    return GenericResult(**result)


# Statements
@tool(description="Read statements from Ramp API", required_scopes=["statements:read"])
async def read_statement(
    ctx: Context,
    number_of_statements: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_statements}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/statements", params)
    if result.get("data") and number_of_statements:
        result["data"] = result["data"][:number_of_statements]
    return GenericResult(**result)


# Transfers
@tool(description="Read transfers from Ramp API", required_scopes=["transfers:read"])
async def read_transfer(
    ctx: Context,
    number_of_transfers: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_transfers}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/transfers", params)
    if result.get("data") and number_of_transfers:
        result["data"] = result["data"][:number_of_transfers]
    return GenericResult(**result)


# Business
@tool(description="Read business information from Ramp API", required_scopes=["business:read"])
async def read_business(ctx: Context) -> GenericResult:
    result = await _ramp_get(ctx, "/business", {})
    if isinstance(result, dict) and "data" not in result:
        result = {"data": [result]}
    return GenericResult(**result)


# Repayments
@tool(description="Read repayments from Ramp API", required_scopes=["repayments:read"])
async def read_repayment(
    ctx: Context,
    number_of_repayments: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_repayments}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/repayments", params)
    if result.get("data") and number_of_repayments:
        result["data"] = result["data"][:number_of_repayments]
    return GenericResult(**result)


# Spend Programs
@tool(description="Read spend programs from Ramp API", required_scopes=["spend_programs:read"])
async def read_spend_program(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/spend_programs", params)
    return GenericResult(**result)


# Treasury
@tool(description="Read treasury information from Ramp API", required_scopes=["treasury:read"])
async def read_treasury(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/treasury", params)
    return GenericResult(**result)


# Trips
@tool(description="Read trips from Ramp API", required_scopes=["trips:read"])
async def read_trip(
    ctx: Context,
    number_of_trips: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_trips}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/trips", params)
    if result.get("data") and number_of_trips:
        result["data"] = result["data"][:number_of_trips]
    return GenericResult(**result)


# Accounting
@tool(description="Read accounting information from Ramp API", required_scopes=["accounting:read"])
async def read_accounting(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/accounting", params)
    return GenericResult(**result)


# Bank Accounts
@tool(description="Read bank accounts from Ramp API", required_scopes=["bank_accounts:read"])
async def read_bank_account(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/bank_accounts", params)
    return GenericResult(**result)


# Bank Feeds
@tool(description="Read bank feeds from Ramp API", required_scopes=["bank_feeds:read"])
async def read_bank_feed(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/bank_feeds", params)
    return GenericResult(**result)


# Memos
@tool(description="Read memos from Ramp API", required_scopes=["memos:read"])
async def read_memo(
    ctx: Context,
    number_of_memos: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_memos}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/memos", params)
    if result.get("data") and number_of_memos:
        result["data"] = result["data"][:number_of_memos]
    return GenericResult(**result)


# Purchase Orders
@tool(description="Read purchase orders from Ramp API", required_scopes=["purchase_orders:read"])
async def read_purchase_order(
    ctx: Context,
    number_of_orders: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_orders}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/purchase_orders", params)
    if result.get("data") and number_of_orders:
        result["data"] = result["data"][:number_of_orders]
    return GenericResult(**result)


# Receipt Integrations
@tool(description="Read receipt integrations from Ramp API", required_scopes=["receipt_integrations:read"])
async def read_receipt_integration(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/receipt_integrations", params)
    return GenericResult(**result)


# Item Receipts
@tool(description="Read item receipts from Ramp API", required_scopes=["item_receipts:read"])
async def read_item_receipt(
    ctx: Context,
    number_of_receipts: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_receipts}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/item_receipts", params)
    if result.get("data") and number_of_receipts:
        result["data"] = result["data"][:number_of_receipts]
    return GenericResult(**result)


# Entities
@tool(description="Read entities from Ramp API", required_scopes=["entities:read"])
async def read_entity(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/entities", params)
    return GenericResult(**result)


# External Attendees
@tool(description="Read external attendees from Ramp API", required_scopes=["external_attendees:read"])
async def read_external_attendee(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/external_attendees", params)
    return GenericResult(**result)


# Leads
@tool(description="Read leads from Ramp API", required_scopes=["leads:read"])
async def read_lead(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/leads", params)
    return GenericResult(**result)


# Attendee Types
@tool(description="Read attendee types from Ramp API", required_scopes=["attendee_types:read"])
async def read_attendee_type(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/attendee_types", params)
    return GenericResult(**result)


# Audit Logs
@tool(description="Read audit logs from Ramp API", required_scopes=["audit_logs:read"])
async def read_audit_log(
    ctx: Context,
    number_of_logs: Optional[int] = 50,
    start: Optional[str] = None
) -> GenericResult:
    params = {"limit": number_of_logs}
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/audit_logs", params)
    if result.get("data") and number_of_logs:
        result["data"] = result["data"][:number_of_logs]
    return GenericResult(**result)


# Custom Records
@tool(description="Read custom records from Ramp API", required_scopes=["custom_records:read"])
async def read_custom_record(
    ctx: Context,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await _ramp_get(ctx, "/custom_records", params)
    return GenericResult(**result)


ramp_tools = [
    read_transaction,
    read_merchant,
    read_reimbursement,
    read_user,
    read_card,
    read_bill,
    read_receipt,
    read_limit,
    read_vendor,
    read_department,
    read_location,
    read_cashback,
    read_statement,
    read_transfer,
    read_business,
    read_repayment,
    read_spend_program,
    read_treasury,
    read_trip,
    read_accounting,
    read_bank_account,
    read_bank_feed,
    read_memo,
    read_purchase_order,
    read_receipt_integration,
    read_item_receipt,
    read_entity,
    read_external_attendee,
    read_lead,
    read_attendee_type,
    read_audit_log,
    read_custom_record,
]
