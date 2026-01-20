import os


def get_credentials():
    """Get Ramp API credentials from credentials.txt file."""
    credentials_file = "credentials.txt"
    
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
