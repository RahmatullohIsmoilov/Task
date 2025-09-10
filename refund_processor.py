from db import db
from gmail_client import gmail
from utils import extract_order_id

def process_refund(email):
    order_id = extract_order_id(email['body'])
    if not order_id:
        gmail.send_email(email['sender'], f"Re: {email['subject']}", "Please provide your order ID.")
        return

    order = db.fetchone("SELECT * FROM orders WHERE order_id=%s", (order_id,))
    if order:
        db.execute("UPDATE orders SET status='refund_requested' WHERE order_id=%s", (order_id,))
        gmail.send_email(email['sender'], f"Re: {email['subject']}", "Refund will be processed within 3 days.")
    else:
        gmail.send_email(email['sender'], f"Re: {email['subject']}", "Invalid order ID.")
        db.execute(
            "INSERT INTO not_found_refunds (sender_email, subject, body) VALUES (%s,%s,%s)",
            (email['sender'], email['subject'], email['body'])
        )
