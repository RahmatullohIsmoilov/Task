from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_TOKEN_PATH

class GmailClient:
    def __init__(self):
        self.creds = Credentials.from_authorized_user_file(GMAIL_TOKEN_PATH)
        self.service = build('gmail', 'v1', credentials=self.creds)

    def fetch_unread_emails(self):
        results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            m = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            emails.append({
                'id': m['id'],
                'subject': next((h['value'] for h in m['payload']['headers'] if h['name'] == 'Subject'), ''),
                'body': self._get_body(m['payload']),
                'sender': next((h['value'] for h in m['payload']['headers'] if h['name'] == 'From'), '')
            })
        return emails

    def _get_body(self, payload):
        if 'parts' in payload:
            return payload['parts'][0]['body'].get('data', '')
        return payload['body'].get('data', '')

    def send_email(self, to, subject, body):
        from email.mime.text import MIMEText
        import base64
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        self.service.users().messages().send(userId='me', body={'raw': encoded_message}).execute()
