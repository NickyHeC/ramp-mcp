"""Ramp API tools.

Tools make authenticated requests to the Ramp API using ctx.dispatch().
DAuth applies the credential inside the enclave — tool code never handles
raw secrets.
"""

from typing import Any
from urllib.parse import urlencode

from dedalus_mcp import tool, get_context, HttpMethod, HttpRequest
from pydantic import BaseModel

from src.main import ramp_connection


class RampResult(BaseModel):
    success: bool
    data: list[dict[str, Any]] = []
    page: dict[str, Any] | None = None
    error: str | None = None


async def api_request(path: str, params: dict | None = None) -> dict:
    """Dispatch an authenticated GET request to the Ramp API through DAuth.

    Args:
        path: API path appended to the connection's base_url (e.g. "/transactions").
        params: Optional query parameters.

    """
    ctx = get_context()
    if params:
        path = f"{path}?{urlencode(params)}"
    req = HttpRequest(method=HttpMethod.GET, path=path)
    resp = await ctx.dispatch(ramp_connection, req)
    if resp.success and resp.response is not None:
        body = resp.response.body
        if isinstance(body, dict):
            data = body.get("data")
            if data is None:
                data = [body]
            return {"success": True, "data": data, "page": body.get("page")}
        return {"success": True, "data": [body] if not isinstance(body, list) else body}
    error = resp.error.message if resp.error else "Request failed"
    return {"success": False, "error": error}


@tool(description="Read transactions from Ramp API", required_scopes=["transactions:read"])
async def read_transaction(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/transactions", params)
    return RampResult(**result)


@tool(description="Read merchants from Ramp API", required_scopes=["merchants:read"])
async def read_merchant(
    merchant_name: str | None = None,
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/merchants", params)
    if merchant_name and result.get("data"):
        result["data"] = [
            m for m in result["data"]
            if merchant_name.lower() in m.get("name", "").lower()
        ]
    return RampResult(**result)


@tool(description="Read reimbursements from Ramp API", required_scopes=["reimbursements:read"])
async def read_reimbursement(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/reimbursements", params)
    return RampResult(**result)


@tool(description="Read users from Ramp API", required_scopes=["users:read"])
async def read_user(
    user_name: str | None = None,
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/users", params)
    if user_name and result.get("data"):
        result["data"] = [
            u for u in result["data"]
            if user_name.lower() in u.get("full_name", "").lower()
            or user_name.lower() in f"{u.get('first_name', '')} {u.get('last_name', '')}".lower()
        ]
    return RampResult(**result)


@tool(description="Read cards from Ramp API", required_scopes=["cards:read"])
async def read_card(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/cards", params)
    return RampResult(**result)


@tool(description="Read bills from Ramp API", required_scopes=["bills:read"])
async def read_bill(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/bills", params)
    return RampResult(**result)


@tool(description="Read receipts from Ramp API", required_scopes=["receipts:read"])
async def read_receipt(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/receipts", params)
    return RampResult(**result)


@tool(description="Read spending limits from Ramp API", required_scopes=["limits:read"])
async def read_limit(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/limits", params)
    return RampResult(**result)


@tool(description="Read vendors from Ramp API", required_scopes=["vendors:read"])
async def read_vendor(
    vendor_name: str | None = None,
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/vendors", params)
    if vendor_name and result.get("data"):
        result["data"] = [
            v for v in result["data"]
            if vendor_name.lower() in v.get("name", "").lower()
        ]
    return RampResult(**result)


@tool(description="Read departments from Ramp API", required_scopes=["departments:read"])
async def read_department(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/departments", params)
    return RampResult(**result)


@tool(description="Read locations from Ramp API", required_scopes=["locations:read"])
async def read_location(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/locations", params)
    return RampResult(**result)


@tool(description="Read cashbacks from Ramp API", required_scopes=["cashbacks:read"])
async def read_cashback(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/cashbacks", params)
    return RampResult(**result)


@tool(description="Read statements from Ramp API", required_scopes=["statements:read"])
async def read_statement(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/statements", params)
    return RampResult(**result)


@tool(description="Read transfers from Ramp API", required_scopes=["transfers:read"])
async def read_transfer(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/transfers", params)
    return RampResult(**result)


@tool(description="Read business information from Ramp API", required_scopes=["business:read"])
async def read_business() -> RampResult:
    result = await api_request("/business")
    return RampResult(**result)


@tool(description="Read repayments from Ramp API", required_scopes=["repayments:read"])
async def read_repayment(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/repayments", params)
    return RampResult(**result)


@tool(description="Read spend programs from Ramp API", required_scopes=["spend_programs:read"])
async def read_spend_program(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/spend_programs", params)
    return RampResult(**result)


@tool(description="Read treasury information from Ramp API", required_scopes=["treasury:read"])
async def read_treasury(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/treasury", params)
    return RampResult(**result)


@tool(description="Read trips from Ramp API", required_scopes=["trips:read"])
async def read_trip(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/trips", params)
    return RampResult(**result)


@tool(description="Read accounting information from Ramp API", required_scopes=["accounting:read"])
async def read_accounting(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/accounting", params)
    return RampResult(**result)


@tool(description="Read bank accounts from Ramp API", required_scopes=["bank_accounts:read"])
async def read_bank_account(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/bank_accounts", params)
    return RampResult(**result)


@tool(description="Read bank feeds from Ramp API", required_scopes=["bank_feeds:read"])
async def read_bank_feed(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/bank_feeds", params)
    return RampResult(**result)


@tool(description="Read memos from Ramp API", required_scopes=["memos:read"])
async def read_memo(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/memos", params)
    return RampResult(**result)


@tool(description="Read purchase orders from Ramp API", required_scopes=["purchase_orders:read"])
async def read_purchase_order(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/purchase_orders", params)
    return RampResult(**result)


@tool(description="Read receipt integrations from Ramp API", required_scopes=["receipt_integrations:read"])
async def read_receipt_integration(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/receipt_integrations", params)
    return RampResult(**result)


@tool(description="Read item receipts from Ramp API", required_scopes=["item_receipts:read"])
async def read_item_receipt(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/item_receipts", params)
    return RampResult(**result)


@tool(description="Read entities from Ramp API", required_scopes=["entities:read"])
async def read_entity(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/entities", params)
    return RampResult(**result)


@tool(description="Read external attendees from Ramp API", required_scopes=["external_attendees:read"])
async def read_external_attendee(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/external_attendees", params)
    return RampResult(**result)


@tool(description="Read leads from Ramp API", required_scopes=["leads:read"])
async def read_lead(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/leads", params)
    return RampResult(**result)


@tool(description="Read attendee types from Ramp API", required_scopes=["attendee_types:read"])
async def read_attendee_type(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/attendee_types", params)
    return RampResult(**result)


@tool(description="Read audit logs from Ramp API", required_scopes=["audit_logs:read"])
async def read_audit_log(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/audit_logs", params)
    return RampResult(**result)


@tool(description="Read custom records from Ramp API", required_scopes=["custom_records:read"])
async def read_custom_record(
    limit: int | None = None,
    start: str | None = None,
) -> RampResult:
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    result = await api_request("/custom_records", params)
    return RampResult(**result)


# --- Tool Registry ---

tools = [
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
