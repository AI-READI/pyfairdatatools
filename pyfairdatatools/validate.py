import json
from os import path

from jsonschema import ValidationError, validate

from . import utils


def validate_dataset_description(data):  # sourcery skip: extract-method
    """Validate a dataset description against the schema.

    Args:
        data (dict): The dataset description to validate
    Returns:
        bool: True if the dataset description is valid, False otherwise
    """
    schema = {}

    # Import the schema from the schemas folder
    with open(
        path.join(path.dirname(__file__), "schemas", "dataset_description.schema.json"),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)

        # validate the language code
        # with open(
        #     path.join(path.dirname(__file__), "assets", "languages.json"),
        #     encoding="utf-8",
        # ) as f:
        #     list_of_language_codes = json.load(f)

        #     valid = any(
        #         language["code"] == data["language"]
        #         for language in list_of_language_codes
        #     )
        #     if not valid:
        #         print("Language code is invalid.")
        #         return False

        # validate the ORCID
        # for creator in data["Creator"]:
        #     if "ORCID" in creator:
        #         base_digits = creator["ORCID"].replace("-", "")[:-1]

        #         total = 0
        #         for digit in base_digits:
        #             total = (total + int(digit)) * 2

        #         remainder = total % 11
        #         result = (12 - remainder) % 11

        #         check_digit = "X" if result == 10 else str(result)

        #         if check_digit != creator["ORCID"][-1]:
        #             print("ORCID is invalid.")
        #             return False

        # validate the rights uri
        # if (
        #     "Rights" in data
        #     and "RightsURI" in data["Rights"]  # noqa: W503
        #     and not utils.validate_url(data["Rights"]["RightsURI"])  # noqa: W503
        # ):
        #     print("Rights identifier is invalid.")
        #     return False

        # validate the license identifier
        # if (
        #     "Rights" in data
        #     and "RightsIdentifier" in data["Rights"]  # noqa: W503
        #     and not validate_license(data["Rights"]["RightsIdentifier"])  # noqa: W503
        # ):
        #     print("License identifier is invalid.")
        #     return False

        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)
        return False
    except Exception as error:
        print(error)
        raise error


def validate_readme(data):
    """Validate a readme against the schema.

    Args:
        data (dict): The readme to validate
    Returns:
        bool: True if the readme is valid, False otherwise
    """
    schema = {}

    # Import the schema from the schemas folder
    with open(
        path.join(path.dirname(__file__), "schemas", "readme.schema.json"),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)
        return False
    except Exception as error:
        print(error)
        raise error


def validate_license(identifier):
    """Validate a license identifier against a list of valid  identifiers.

    Args:
        identifier (str): The license identifier to validate
    Returns:
        bool: True if the license identifier is valid, False otherwise
    """

    # Import the license list from the assets folder
    with open(
        path.join(path.dirname(__file__), "assets", "licenses.json"),
        encoding="utf-8",
    ) as f:
        list_of_licenses = json.load(f)["licenses"]

    return any(
        "licenseId" in item and identifier == item["licenseId"]
        for item in list_of_licenses
    )


def validate_participants(data):
    """Validate a participants file against the schema.

    Args:
        data (dict): The participants file to validate
    Returns:
        bool: True if the participants file is valid, False otherwise
    """
    schema = {}

    # Import the schema from the schemas folder
    with open(
        path.join(path.dirname(__file__), "schemas", "participants.schema.json"),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)

        # TODO: validate species
        # TODO: validate strain
        # TODO: validate strain_rrid

        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)
        return False
    except Exception as error:
        print(error)
        raise error
