# tools.py - Ramp API tools
import os
import base64
import httpx
from dedalus_mcp import tool
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


def get_credentials() -> tuple[str, str]:
    """Get Ramp API credentials from credentials.txt file."""
    # Look for credentials.txt in the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    credentials_file = os.path.join(project_root, "credentials.txt")
    
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(
            f"Credentials file '{credentials_file}' not found. "
            "Please create it with your RAMP_ID and RAMP_SEC."
        )
    
    ramp_id = None
    ramp_sec = None
    
    with open(credentials_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            if line.startswith('RAMP_ID='):
                ramp_id = line.split('=', 1)[1].strip()
            elif line.startswith('RAMP_SEC='):
                ramp_sec = line.split('=', 1)[1].strip()
    
    if not ramp_id or not ramp_sec:
        raise ValueError(
            f"Missing credentials in '{credentials_file}'. "
            "Please ensure RAMP_ID and RAMP_SEC are set."
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
    number_of_transactions: Optional[int] = 5,
    start: Optional[str] = None
) -> TransactionResult:
    scope: str = "transactions:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_transactions}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/transactions",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    # Ensure we only return the exact number of transactions requested
    if result.get("data") and number_of_transactions:
        result["data"] = result["data"][:number_of_transactions]
    
    return TransactionResult(**result)


class MerchantResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read merchants from Ramp API")
def read_merchant(
    merchant_name: str,
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
    number_of_reimbursements: Optional[int] = 5,
    start: Optional[str] = None
) -> ReimbursementResult:
    scope: str = "reimbursements:read"
    access_token = _get_access_token(scope)
    
    params = {"limit": number_of_reimbursements}
    if start:
        params["start"] = start
    
    resp = httpx.get(
        "https://api.ramp.com/developer/v1/reimbursements",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params
    )
    resp.raise_for_status()
    result = resp.json()
    
    # Ensure we only return the exact number of reimbursements requested
    if result.get("data") and number_of_reimbursements:
        result["data"] = result["data"][:number_of_reimbursements]
    
    return ReimbursementResult(**result)


class UserResult(BaseModel):
    data: List[Dict[str, Any]]
    page: Optional[Dict[str, Any]] = None


@tool(description="Read users from Ramp API")
def read_user(
    user_name: str,
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


ramp_tools = [read_transaction, read_merchant, read_reimbursement, read_user]
