"""Utils file for common operations."""

# Imports
from datetime import datetime
from nanoid import generate
import requests


# Valid characters
valid_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_uid(size=11, prefix="NL", year=True):
    """Generate a unique identifier.

    Args:
        size (int, optional): Size of the random string to be generated. Defaults to 11.
        prefix (str, optional): Prefix for the unique ID. Defaults to "".

    Raises:
        TypeError: If size is not int.
        TypeError: If prefix is not str.

    Returns:
        str: Unique ID.
    """
    # Error handling for incorrect data types
    if not isinstance(size, int):
        raise TypeError("size must of type int")
    if not isinstance(prefix, str):
        raise TypeError("prefix must of type str")

    # Set current year
    this_year = str(datetime.now().year)
    # Generate random text using nanoid
    random_txt = generate(alphabet=valid_chars, size=size)
    # Create the final string without prefix
    if year:
        uid = f"{prefix}-{random_txt}-{this_year}"
    else:
        uid = f"{prefix}-{random_txt}"

    return uid

def send_to_teams_webhook(text):
    webhook_url = "https://agrkspl.webhook.office.com/webhookb2/1b84cd4c-0d32-4220-9a4b-5315a75b76b9@ef6d8f52-9afa-48ef-8b83-bc822e9c656c/IncomingWebhook/4258b3d92808457daa11556be7b9fcca/9c644380-8921-43a0-b192-3644c7fbe1c7"

    payload = {
        "text": text
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Log sent successfully to Microsoft Teams webhook!")
    else:
        print(f"Failed to send log to Microsoft Teams webhook. Status code: {response.status_code}")
