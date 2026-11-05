from datetime import datetime

PAYMENT_MODES = ['Cash','UPI','Card','NetBanking','Cheque','Other']

def validate_amount(v):
    try:
        val = float(str(v).strip())
        if val <= 0: raise ValueError("Amount must be positive")
        return round(val, 2)
    except ValueError:
        raise ValueError("Invalid amount. Enter a positive number (e.g. 250.50)")

def validate_date(d):
    d = str(d).strip()
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return d
    except ValueError:
        raise ValueError("Invalid date. Use YYYY-MM-DD format (e.g. 2024-10-15)")

def validate_payment_mode(m):
    if m in PAYMENT_MODES: return m
    raise ValueError(f"Invalid mode. Choose from: {', '.join(PAYMENT_MODES)}")
