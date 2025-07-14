from googleapiclient.discovery import build
from base64 import urlsafe_b64decode
from email import message_from_bytes

def get_service(creds):
    return build("gmail", "v1", credentials=creds)

def get_latest_emails(service, max_results=5):
    results = service.users().messages().list(userId='me', q="is:unread", maxResults=max_results).execute()
    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])

        email_data = {
            "gmail_id": msg_data.get("id"),
            "received_at": int(msg_data.get("internalDate", 0)) / 1000,  # epoch to datetime
            "subject": next((h['value'] for h in headers if h['name'] == 'Subject'), ''),
            "from": next((h['value'] for h in headers if h['name'] == 'From'), ''),
            "body": extract_body(payload)
        }
        emails.append(email_data)

    return emails

def extract_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    body = urlsafe_b64decode(data.encode()).decode('utf-8')
                    break
    else:
        data = payload.get('body', {}).get('data', '')
        if data:
            body = urlsafe_b64decode(data.encode()).decode('utf-8')
    return body
