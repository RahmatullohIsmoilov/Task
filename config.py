import os

GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "./token.json")

POSTGRES_DSN = os.getenv("POSTGRES_DSN", "dbname=customer_support user=postgres password=secret host=localhost")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 60))  # seconds
