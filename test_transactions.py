#!/usr/bin/env python3
"""Test script to read transactions from Ramp API."""
import sys
import os
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tools import read_transaction

def format_transaction(txn):
    """Format a transaction as readable text."""
    # Parse date
    date_str = txn.get('accounting_date', '')
    if date_str:
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            date_display = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            date_display = date_str
    else:
        date_display = 'N/A'
    
    # Get card holder info
    card_holder = txn.get('card_holder', {})
    card_holder_name = f"{card_holder.get('first_name', '')} {card_holder.get('last_name', '')}".strip()
    if not card_holder_name:
        card_holder_name = 'Unknown'
    
    # Get merchant info
    merchant_name = txn.get('merchant_name', 'Unknown Merchant')
    amount = txn.get('amount', 0)
    currency = txn.get('currency_code', 'USD')
    state = txn.get('state', 'UNKNOWN')
    
    # Get category
    category = txn.get('sk_category_name', 'N/A')
    
    # Build formatted string
    lines = [
        f"{'='*80}",
        f"Merchant: {merchant_name}",
        f"Amount: {currency} ${amount:.2f}",
        f"Date: {date_display}",
        f"State: {state}",
        f"Card Holder: {card_holder_name}",
        f"Category: {category}",
    ]
    
    # Add memo if present
    memo = txn.get('memo')
    if memo:
        lines.append(f"Memo: {memo}")
    
    # Add merchant descriptor if different from name
    descriptor = txn.get('merchant_descriptor')
    if descriptor and descriptor != merchant_name:
        lines.append(f"Descriptor: {descriptor}")
    
    # Add location if available
    location = txn.get('merchant_location', {})
    if location:
        city = location.get('city', '')
        state_code = location.get('state', '')
        if city or state_code:
            location_str = ', '.join(filter(None, [city, state_code]))
            lines.append(f"Location: {location_str}")
    
    return '\n'.join(lines)

if __name__ == "__main__":
    try:
        result = read_transaction(number_of_transactions=6)
        
        print(f"\nFound {len(result.data)} transactions:\n")
        
        for i, txn in enumerate(result.data, 1):
            print(f"\nTransaction #{i}:")
            print(format_transaction(txn))
        
        print(f"\n{'='*80}\n")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
