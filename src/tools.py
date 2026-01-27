# tools.py - Ramp API tools
import os
import base64
import httpx
from dedalus_mcp import tool
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


def get_credentials() -> tuple[str, str]:
    """Get Ramp API credentials from .env file."""
    from dotenv import load_dotenv
    
    # Load environment variables from .env file in project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(project_root, ".env")
    load_dotenv(env_file)
    
    ramp_id = os.getenv("RAMP_ID")
    ramp_sec = os.getenv("RAMP_SEC")
    
    if not ramp_id or not ramp_sec:
        raise ValueError(
            "Missing credentials in .env file. "
            "Please ensure RAMP_ID and RAMP_SEC are set in your .env file."
        )
    
    return ramp_id, ramp_sec


def _get_access_token(scope: str) -> str:
    """Get an access token from the Ramp API."""
    ramp_id, ramp_sec = get_credentials()
    auth = base64.b64encode(f"{ramp_id}:{ramp_sec}".encode()).decode()
    
    resp = httpx.post(
        "https://api.ramp.com/developer/v1/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "client_credentials",
            "scope": scope
        }
    )
    resp.raise_for_status()
    token_data = resp.json()
    access_token = token_data.get("access_token")
    
    if not access_token:
        raise Exception(f"Failed to get access token: {token_data}")
    
    return access_token


class TransactionResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read transactions from Ramp API")
def read_transaction(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> TransactionResult:
    scope: str = "transactions:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/transactions",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return TransactionResult(**result)


class MerchantResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read merchants from Ramp API")
def read_merchant(
    merchant_name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> MerchantResult:
    scope: str = "merchants:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/merchants",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
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


@tool(description="Read reimbursements from Ramp API")
def read_reimbursement(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> ReimbursementResult:
    scope: str = "reimbursements:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/reimbursements",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return ReimbursementResult(**result)


class UserResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read users from Ramp API")
def read_user(
    user_name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> UserResult:
    scope: str = "users:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/users",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
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
@tool(description="Read cards from Ramp API")
def read_card(
    number_of_cards: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "cards:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_cards}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/cards",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_cards:
        result["data"] = result["data"][:number_of_cards]
    
    return GenericResult(**result)


# Bills
@tool(description="Read bills from Ramp API")
def read_bill(
    number_of_bills: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "bills:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_bills}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/bills",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_bills:
        result["data"] = result["data"][:number_of_bills]
    
    return GenericResult(**result)


# Receipts
@tool(description="Read receipts from Ramp API")
def read_receipt(
    number_of_receipts: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "receipts:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_receipts}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/receipts",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_receipts:
        result["data"] = result["data"][:number_of_receipts]
    
    return GenericResult(**result)


# Limits
@tool(description="Read spending limits from Ramp API")
def read_limit(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "limits:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/limits",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Vendors
@tool(description="Read vendors from Ramp API")
def read_vendor(
    vendor_name: Optional[str] = None,
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "vendors:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/vendors",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    # Filter by vendor_name if provided
    if vendor_name and result.get("data"):
        filtered_data = [
            vendor for vendor in result["data"]
            if vendor_name.lower() in vendor.get("name", "").lower()
        ]
        result["data"] = filtered_data
    
    return GenericResult(**result)


# Departments
@tool(description="Read departments from Ramp API")
def read_department(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "departments:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/departments",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Locations
@tool(description="Read locations from Ramp API")
def read_location(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "locations:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/locations",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Cashbacks
@tool(description="Read cashbacks from Ramp API")
def read_cashback(
    number_of_cashbacks: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "cashbacks:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_cashbacks}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/cashbacks",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_cashbacks:
        result["data"] = result["data"][:number_of_cashbacks]
    
    return GenericResult(**result)


# Statements
@tool(description="Read statements from Ramp API")
def read_statement(
    number_of_statements: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "statements:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_statements}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/statements",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_statements:
        result["data"] = result["data"][:number_of_statements]
    
    return GenericResult(**result)


# Transfers
@tool(description="Read transfers from Ramp API")
def read_transfer(
    number_of_transfers: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "transfers:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_transfers}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/transfers",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_transfers:
        result["data"] = result["data"][:number_of_transfers]
    
    return GenericResult(**result)


# Business
@tool(description="Read business information from Ramp API")
def read_business() -> GenericResult:
    scope: str = "business:read"
    access_token = _get_access_token(scope)
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/business",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    resp.raise_for_status()
    result = resp.json()
    
    # Business endpoint typically returns a single object, wrap in data array
    if isinstance(result, dict) and "data" not in result:
        result = {"data": [result]}
    
    return GenericResult(**result)


# Repayments
@tool(description="Read repayments from Ramp API")
def read_repayment(
    number_of_repayments: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "repayments:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_repayments}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/repayments",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_repayments:
        result["data"] = result["data"][:number_of_repayments]
    
    return GenericResult(**result)


# Spend Programs
@tool(description="Read spend programs from Ramp API")
def read_spend_program(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "spend_programs:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/spend_programs",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Treasury
@tool(description="Read treasury information from Ramp API")
def read_treasury(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "treasury:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/treasury",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Trips
@tool(description="Read trips from Ramp API")
def read_trip(
    number_of_trips: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "trips:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_trips}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/trips",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_trips:
        result["data"] = result["data"][:number_of_trips]
    
    return GenericResult(**result)


# Accounting
@tool(description="Read accounting information from Ramp API")
def read_accounting(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "accounting:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/accounting",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Bank Accounts
@tool(description="Read bank accounts from Ramp API")
def read_bank_account(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "bank_accounts:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/bank_accounts",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Bank Feeds
@tool(description="Read bank feeds from Ramp API")
def read_bank_feed(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "bank_feeds:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/bank_feeds",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Memos
@tool(description="Read memos from Ramp API")
def read_memo(
    number_of_memos: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "memos:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_memos}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/memos",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_memos:
        result["data"] = result["data"][:number_of_memos]
    
    return GenericResult(**result)


# Purchase Orders
@tool(description="Read purchase orders from Ramp API")
def read_purchase_order(
    number_of_orders: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "purchase_orders:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_orders}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/purchase_orders",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_orders:
        result["data"] = result["data"][:number_of_orders]
    
    return GenericResult(**result)


# Receipt Integrations
@tool(description="Read receipt integrations from Ramp API")
def read_receipt_integration(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "receipt_integrations:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/receipt_integrations",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Item Receipts
@tool(description="Read item receipts from Ramp API")
def read_item_receipt(
    number_of_receipts: Optional[int] = 10,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "item_receipts:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_receipts}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/item_receipts",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_receipts:
        result["data"] = result["data"][:number_of_receipts]
    
    return GenericResult(**result)


# Entities
@tool(description="Read entities from Ramp API")
def read_entity(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "entities:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/entities",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# External Attendees
@tool(description="Read external attendees from Ramp API")
def read_external_attendee(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "external_attendees:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/external_attendees",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Leads
@tool(description="Read leads from Ramp API")
def read_lead(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "leads:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/leads",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Attendee Types
@tool(description="Read attendee types from Ramp API")
def read_attendee_type(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "attendee_types:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/attendee_types",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    return GenericResult(**result)


# Audit Logs
@tool(description="Read audit logs from Ramp API")
def read_audit_log(
    number_of_logs: Optional[int] = 50,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "audit_logs:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_logs}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/audit_logs",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    if result.get("data") and number_of_logs:
        result["data"] = result["data"][:number_of_logs]
    
    return GenericResult(**result)


# Custom Records
@tool(description="Read custom records from Ramp API")
def read_custom_record(
    limit: Optional[int] = None,
    start: Optional[str] = None
) -> GenericResult:
    scope: str = "custom_records:read"
    access_token = _get_access_token(scope)
    
    params = {}
    if limit:
        params["limit"] = limit
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/custom_records",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
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
