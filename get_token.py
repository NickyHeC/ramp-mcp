import os
from dotenv import load_dotenv


def get_credentials():
    """Get Ramp API credentials from .env file."""
    # Load environment variables from .env file
    load_dotenv()
    
    ramp_id = os.getenv("RAMP_ID")
    ramp_sec = os.getenv("RAMP_SEC")
    
    if not ramp_id or not ramp_sec:
        raise ValueError(
            "Missing credentials in .env file. "
            "Please ensure RAMP_ID and RAMP_SEC are set in your .env file."
        )
    
    return ramp_id, ramp_sec
