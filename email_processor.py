from db import db
from rag_agent import answer_question
from refund_processor import process_refund
from utils import categorize_email, assess_importance
from gmail_client import GmailClient

gmail = GmailClient()

def handle_email(email):
    category = categorize_email(email['subject'], email['body'])

    if category == 'question':
        response = answer_question(email['body'])
        if response:
            gmail.send_email(email['sender'], f"Re: {email['subject']}", response)
        else:
            db.execute(
                "INSERT INTO unhandled_emails (sender_email, subject, body, importance) VALUES (%s,%s,%s,%s)",
                (email['sender'], email['subject'], email['body'], 'high')
            )

    elif category == 'refund':
        process_refund(email)

    else:  # other emails
        importance = assess_importance(email['body'])
        db.execute(
            "INSERT INTO unhandled_emails (sender_email, subject, body, importance) VALUES (%s,%s,%s,%s)",
            (email['sender'], email['subject'], email['body'], importance)
        )
