import os

import requests
import validators
from validators import ValidationFailure


def feet_to_meters(feet):
    """Convert feet to meters."""
    try:
        value = float(feet)
    except ValueError as error:
        print(f"Could not convert {feet} to float")
        raise ValueError(f"Invalid input: {feet}") from error

    return (0.3048 * value * 10000.0 + 0.5) / 10000.0


def requestJSON(url):
    try:
        response = requests.request("GET", url, headers={}, data={}, timeout=5)

        return response.json()
    except Exception as e:
        raise e


def validate_file_path(file_path, preexisting_file=False, writable=False):
    if file_path == "":
        print("File path is empty.")
        raise ValueError("Invalid input")

    if preexisting_file:
        if not os.path.exists(file_path):
            print("File path does not exist.")
            raise FileNotFoundError("File not found")

        if not os.path.isfile(file_path):
            print("File path is not a file.")
            raise ValueError("Invalid input")

    if writable and os.access(file_path, os.W_OK):
        print("File path is not writable.")
        raise PermissionError("Permission denied")

    return True


def validate_url(url_string):
    result = validators.url(url_string)

    return False if isinstance(result, ValidationFailure) else result
