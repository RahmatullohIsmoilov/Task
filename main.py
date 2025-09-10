import time
from email_processor import handle_email
from gmail_client import GmailClient
from config import POLL_INTERVAL

gmail = GmailClient()

def main():
    while True:
        try:
            emails = gmail.fetch_unread_emails()
            for email in emails:
                handle_email(email)
        except Exception as e:
            print("Error:", e)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
