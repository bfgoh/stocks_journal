from gmail_api import *
from google_apis import create_service
import ingestibkr
from gmail_api import *
import time
import os

if __name__ == "__main__":
    CLIENT_FILE = "credentials.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = [
        "https://mail.google.com/",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

    query_string = "is:unread filename:*.csv "

    save_location = os.getcwd()
    email_messages = search_emails(service, query_string)
    if email_messages:
        for email_message in email_messages:
            messageDetail = get_message_detail(
                service,
                email_message["id"],
                msg_format="full",
                metadata_headers=["parts"],
            )
            messageDetailPayload = messageDetail.get("payload")

            if "parts" in messageDetailPayload:
                for msgPayload in messageDetailPayload["parts"]:
                    file_name = msgPayload["filename"]
                    body = msgPayload["body"]
                    if "attachmentId" in body and "DayTrade" in file_name:
                        attachment_id = body["attachmentId"]
                        attachment_content = get_file_data(
                            email_message["id"], attachment_id, file_name, save_location
                        )
                        csv_file_path = os.path.join(save_location, file_name)
                        with open(file=csv_file_path, mode="wb") as _f:
                            _f.write(attachment_content)
                        ingestibkr.main(csv_file_path)
                        # Remove Unread label after completion of updating file
                        service.users().messages().modify(
                            userId="me",
                            id=email_message["id"],
                            body={"removeLabelIds": ["UNREAD"]},
                        ).execute()

            time.sleep(0.5)
    else:
        print("no new messages found.")
