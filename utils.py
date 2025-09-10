def categorize_email(subject, body):
    if 'refund' in body.lower():
        return 'refund'
    elif '?' in body:
        return 'question'
    else:
        return 'other'

def assess_importance(body):
    if 'urgent' in body.lower():
        return 'high'
    return 'medium'

def extract_order_id(body):
    import re
    match = re.search(r'Order\s*ID[:\s]*([A-Za-z0-9-]+)', body, re.I)
    return match.group(1) if match else None
