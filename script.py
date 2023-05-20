import os
import subprocess
import base64
import mimetypes
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

python_files = ['/home/gaurav/ScrapIt/naukricom_job_scraper.py','/home/gaurav/ScrapIt/TimesJobs.py']

for file in python_files:
    subprocess.run(['python',file])


def create_gmail_service():
    creds = None
   
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
   
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/home/gaurav/python-project/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0,browser='/usr/bin/brave')
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message_with_attachment(sender, to, subject, message_text, file_paths):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    message.attach(MIMEText(message_text, 'plain'))

    for file_path in file_paths:
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        with open(file_path, 'rb') as file:
            file_data = file.read()
        file_part = MIMEBase(main_type, sub_type)
        file_part.set_payload(file_data)
        file_part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        message.attach(file_part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def send_email(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message sent successfully.')
    except Exception as e:
        print('An error occurred while sending the email:', str(e))


def main():
    
    parser = argparse.ArgumentParser(description='Send email with attachments using Gmail API')
    parser.add_argument('--sender', required=True, help='Sender email address')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', required=True, help='Email subject')
    parser.add_argument('--message', required=True, help='Email message')
    parser.add_argument('--file1', required=True, help='Path to file 1')
    parser.add_argument('--file2', required=True, help='Path to file 2')
    args = parser.parse_args()

    
    service = create_gmail_service()

    # Create a message with attachments
    file_paths = [args.file1, args.file2]
    message = create_message_with_attachment(args.sender, args.to, args.subject, args.message, file_paths)

        # Send the email
    send_email(service, 'me', message)

if __name__ == '__main__':
    main()