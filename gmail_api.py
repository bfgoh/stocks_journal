import base64
from typing import List
from google_apis import create_service


class GmailException(Exception):
    """gmail base exception class"""


class NoEmailFound(GmailException):
    """no email found"""


def search_emails(service, query_string: str, label_ids: List = None):
    try:
        message_list_response = (
            service.users()
            .messages()
            .list(userId="me", labelIds=label_ids, q=query_string)
            .execute()
        )

        message_items = message_list_response.get("messages")
        next_page_token = message_list_response.get("nextPageToken")

        while next_page_token:
            message_list_response = (
                service.users()
                .messages()
                .list(
                    userId="me",
                    labelIds=label_ids,
                    q=query_string,
                    pageToken=next_page_token,
                )
                .execute()
            )

            message_items.extend(message_list_response.get("messages"))
            next_page_token = message_list_response.get("nextPageToken")
        return message_items
    except Exception as e:
        raise NoEmailFound("No emails returned")


def get_file_data(service, message_id, attachment_id, file_name, save_location):
    response = (
        service.users()
        .messages()
        .attachments()
        .get(userId="me", messageId=message_id, id=attachment_id)
        .execute()
    )

    file_data = base64.urlsafe_b64decode(response.get("data").encode("UTF-8"))
    return file_data


def get_message_detail(
    service, message_id, msg_format="metadata", metadata_headers: List = None
):
    message_detail = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format=msg_format,
            metadataHeaders=metadata_headers,
        )
        .execute()
    )
    return message_detail
