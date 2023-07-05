import json
import os

from jsonschema import ValidationError, validate

# from . import utils


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
        os.path.join(
            os.path.dirname(__file__), "schemas", "dataset_description.schema.json"
        ),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)

        # validate the language code
        if "Language" in data:
            with open(
                os.path.join(os.path.dirname(__file__), "assets", "languages.json"),
                encoding="utf-8",
            ) as f:
                list_of_language_codes = json.load(f)

                valid = any(
                    language["code"] == data["Language"]
                    for language in list_of_language_codes
                )
                if not valid:
                    print("Language code is invalid.")
                    return False

        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)
        return False
    except Exception as error:
        print(error)
        raise error


def validate_study_description(data):  # sourcery skip: extract-method
    """Validate a study description against the schema."""
    schema = {}

    # Import the schema from the schemas folder
    with open(
        os.path.join(
            os.path.dirname(__file__), "schemas", "study_description.schema.json"
        ),
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
        os.path.join(os.path.dirname(__file__), "schemas", "readme.schema.json"),
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
    list_of_licenses = []

    # Import the license list from the assets folder
    with open(
        os.path.join(os.path.dirname(__file__), "assets", "licenses.json"),
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
        os.path.join(os.path.dirname(__file__), "schemas", "participants.schema.json"),
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


def validate_folder_structure(folder_path):
    """Validate that a folder structure is valid.

    We do this by generating a json tree of the folder and file structure and
    validating it against a schema.
    This will allow us to expand the schema in the future to include more complex
    folder structures.
    Certain folder structures (ones inside of dynamic folders) will not be able to
    be validated by this method.

    Args:
        folder_path (str): The path to the folder to validate
    Returns:
        bool: True if the folder structure is valid, False otherwise
    """

    def path_to_dict(path):
        d = {}  # type: dict

        if not os.path.exists(path):
            return d

        for x in os.listdir(path):
            key = os.path.basename(x)

            if os.path.isdir(os.path.join(path, x)):
                d[key] = path_to_dict(os.path.join(path, x))
            else:
                d[key] = "file"

        return d

    # Import the schema from the schemas folder
    with open(
        os.path.join(
            os.path.dirname(__file__), "schemas", "folder_structure.schema.json"
        ),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    folder_structure_as_dict = path_to_dict(folder_path)

    try:
        validate(instance=folder_structure_as_dict, schema=schema)

        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)
        return False
    except Exception as error:
        print(error)
        raise error
