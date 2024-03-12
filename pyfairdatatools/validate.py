import json
import os

import yaml
from jsonschema import ValidationError, validate

# from . import utils


def validate_dataset_description(data, verbose=False):  # sourcery skip: extract-method
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
        if "language" in data:
            with open(
                os.path.join(os.path.dirname(__file__), "assets", "languages.json"),
                encoding="utf-8",
            ) as f:
                list_of_language_codes = json.load(f)

                valid = any(
                    language["code"] == data["language"]
                    for language in list_of_language_codes
                )
                if not valid:
                    print("language code is invalid.")
                    return False

        if "relatedIdentifier" in data:
            related_identifiers = data["relatedIdentifier"]

            for related_identifier in related_identifiers:
                if related_identifier["relationType"] in [
                    "IsMetadataFor",
                    "HasMetadata",
                ]:
                    if "relatedMetadataScheme" not in related_identifier:
                        print(
                            "relatedMetadataScheme is required for IsMetadataFor and HasMetadata relation types."
                        )
                        return False

                    if "schemeURI" not in related_identifier:
                        print(
                            "schemeURI is required for IsMetadataFor and HasMetadata relation types."
                        )
                        return False

                    if "schemeType" not in related_identifier:
                        print(
                            "schemeType is required for IsMetadataFor and HasMetadata relation types."
                        )
                        return False

        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)

        # return e.message

        return False
    except Exception as error:
        print(error)
        raise error


def validate_study_description(data):  # sourcery skip: extract-method, low-code-quality
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

        statusModule = data["statusModule"]

        overallStatus = statusModule["overallStatus"]

        if overallStatus in ["Withdrawn", "Terminated", "Suspended"]:
            if "whyStopped" not in statusModule:
                print(
                    "whyStopped is required for Withdrawn, Terminated, and Suspended overallStatus."
                )
                return False

        studyType = data["designModule"]["studyType"]

        if studyType == "Interventional":
            armGroupList = data["armsInterventionsModule"]["armGroupList"]

            for armGroup in armGroupList:
                if "armGroupType" not in armGroup:
                    print(
                        "armGroupType is required is required for interventional studies."  # pylint: disable=line-too-long
                    )
                    return False

        elif studyType == "Observational":
            # check if the StudyPopulation key exists and is not empty
            if "studyPopulation" not in data["eligibilityModule"]:
                print("studyPopulation is required for observational studies.")
                return False

            studyPopulation = data["eligibilityModule"]["studyPopulation"]

            if studyPopulation is None or studyPopulation == "":
                print(
                    "A value for studyPopulation is required for observational studies."
                )
                return False

            # check if the SamplingMethod key exists
            if "samplingMethod" not in data["eligibilityModule"]:
                print("samplingMethod is required for observational studies.")
                return False

        if (
            "centralContactList" not in data["contactsLocationsModule"]
            or len(data["contactsLocationsModule"]["centralContactList"]) == 0
        ):
            locationList = data["contactsLocationsModule"]["locationList"]

            for location in locationList:
                if (
                    "locationContactList" not in location
                    or len(location["locationContactList"]) == 0
                ):
                    print(
                        "locationContactList is required if no Central Contact is provided."  # pylint: disable=line-too-long
                    )
                    return False

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


def validate_datatype_dictionary(data):
    """Validate a datatype description against the scheme.

    Args:
        data (list): The datatype description to validate
    Returns:
        bool: True if the datatype description is valid, False otherwise
    """
    # Import the yaml file from the schemas folder
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "assets",
            "datatype_dictionary.yaml",
        ),
        encoding="utf-8",
    ) as f:
        schema = yaml.safe_load(f)

    try:
        # create a list of code_name and aliases from schema to validate against
        code_name_list = [
            code_name["code_name"] for code_name in schema["datatype_dictionary"]
        ]
        code_name_list += [
            alias
            for code_name in schema["datatype_dictionary"]
            if "aliases" in code_name
            for alias in code_name["aliases"]
        ]

        for entry in data:
            if entry not in code_name_list:
                print(f"code_name {entry} is not a valid code_name or alias.")
                return False

        return True
    except ValidationError as e:
        print(e.schema["error_msg"] if "error_msg" in e.schema else e.message)
        return False
    except Exception as error:
        print(error)
        raise error
