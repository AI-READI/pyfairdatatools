import json
import os

import yaml
from jsonschema import ValidationError, validate
import logging
import sys
import re
import csv

SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)

logging.Logger.success = success

# Color Formatter
class ColorFormatter(logging.Formatter):

    COLORS = {
        logging.DEBUG: "\033[90m",     # Gray
        logging.INFO: "\033[94m",      # Blue
        logging.WARNING: "\033[93m",   # Yellow
        logging.ERROR: "\033[91m",     # Red
        logging.CRITICAL: "\033[95m",  # Magenta
        SUCCESS: "\033[92m",           # Green
    }

    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        msg = super().format(record)
        return f"{color}{msg}{self.RESET}"

# Logger Setup
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter("%(levelname)s ▶ %(message)s"))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers.clear()
logger.addHandler(handler)


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
        print(f" Validation Error: {e.message}")
        print(f"→ Field Path: {'.'.join(str(p) for p in e.path)}")
        print(f"→ Schema Rule Path: {'.'.join(str(p) for p in e.schema_path)}")
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

    with open(
        os.path.join(os.path.dirname(__file__), "schemas", "participants.schema.json"),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    # Allow person_id as an alternative to participant_id
    if "items" in schema and "required" in schema["items"]:
        if "participant_id" in schema["items"]["properties"]:
            schema["items"]["properties"]["participant_id"].pop("pattern", None)
        if "person_id" not in schema["items"]["properties"]:
            schema["items"]["properties"]["person_id"] = schema["items"]["properties"]["participant_id"].copy()

        for participant in data:
            if "person_id" in participant and "participant_id" not in participant:
                participant["participant_id"] = participant["person_id"]
            if "age" in participant and participant["age"]:
                participant["age"] = float(participant["age"])

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


def validate_file_path(file_path, preexisting_file=False, writable=False):
    """Validate a file path. Checks if the file exists, is a file, and is writable."""
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

    if writable and not os.access(file_path, os.W_OK):  # ← DÜZELTİLDİ: 'not' eklendi
        print("File path is not writable.")
        raise PermissionError("Permission denied")

    return True


REQUIRED_FILES = [
    "dataset_description.json",
    "CHANGELOG.md",
    "LICENSE.txt",
    "README.md",
    "participants.json",
    "participants.tsv"
]

OPTIONAL_FILES = [
    "readme.md",
    "changelog.md",
    "study_description.txt",
    "license.txt",
]

ALLOWED_TEXT_EXTS = {".md", ".txt", ".rst"}

NAME_PATTERN = re.compile(r'^[a-z0-9._-]+$')

WINDOWS_RESERVED = {
    "con", "prn", "aux", "nul",
    "com1","com2","com3","com4","com5","com6","com7","com8","com9",
    "lpt1","lpt2","lpt3","lpt4","lpt5","lpt6","lpt7","lpt8","lpt9"
}

ALLOWED_UPPERCASE_FILES = {
    "readme.md", "readme.txt", "readme.rst",
    "changelog.md", "changelog.txt", "changelog.rst",
    "license.md", "license.txt", "license.rst", "license",
}


def validate_names(root):

    errors = []
    warnings = []

    for dirpath, dirnames, filenames in os.walk(root):

        for name in dirnames + filenames:

            full = os.path.join(dirpath, name)
            base = os.path.splitext(name)[0].lower()
            name_lower = name.lower()

            # Spaces
            if " " in name:
                errors.append(f"Space in name: {full}")

            # Uppercase - but allow certain conventional files
            if any(c.isupper() for c in name):
                if name_lower not in ALLOWED_UPPERCASE_FILES:
                    errors.append(f"Uppercase in name: {full}")

            # Invalid chars - skip check for allowed uppercase files
            if name_lower not in ALLOWED_UPPERCASE_FILES:  # ← YENİ SATIR
                if not NAME_PATTERN.match(name):
                    errors.append(f"Invalid characters: {full}")

            # Hidden files
            if name.startswith("."):
                warnings.append(f"Hidden file/folder: {full}")

            # Windows reserved
            if base in WINDOWS_RESERVED:
                errors.append(f"Windows reserved name: {full}")

            # Long name
            if len(name) > 150:
                warnings.append(f"Very long name: {full}")

    return errors, warnings


def validate_folder_structure(folder_path):

    logger.info("Starting folder structure validation...")

    if not os.path.isdir(folder_path):
        logger.error("Folder not found: %s", folder_path)
        return False

    name_errors, name_warnings = validate_names(folder_path)

    for w in name_warnings:
        logger.warning(w)

    if name_errors:
        for e in name_errors:
            logger.error(e)
        return False

    # SCHEMA CHECK
    def path_to_dict(path):
        d = {}
        for x in os.listdir(path):
            p = os.path.join(path, x)
            if os.path.isdir(p):
                d[x] = path_to_dict(p)
            else:
                d[x] = "file"
        return d

    try:
        with open(
            os.path.join(os.path.dirname(__file__), "schemas", "folder_structure.schema.json"),
            encoding="utf-8"
        ) as f:
            schema = json.load(f)

        tree = path_to_dict(folder_path)
        validate(instance=tree, schema=schema)
        logger.info("Folder structure matches schema")

    except ValidationError as e:
        logger.error("FAILED: Folder structure invalid (%s)", e.message)
        return False
    except Exception as e:
        logger.error("Schema error: %s", e)
        return False

    # FILE VALIDATION
    files = os.listdir(folder_path)
    all_valid = True

    # ── Required files ──────────────────────────────────────────────────────────
    for fname in REQUIRED_FILES:
        if fname not in files:
            logger.error("Missing required file: %s", fname)
            return False
        logger.info("Found required file: %s", fname)

    # ── dataset_description.json ───────────────────────────────────────────────
    dd_path = os.path.join(folder_path, "dataset_description.json")
    logger.info("Validating dataset_description.json...")
    try:
        with open(dd_path, encoding="utf-8") as f:
            dd_data = json.load(f)
        if validate_dataset_description(dd_data):
            logger.success("dataset_description.json is valid")
        else:
            logger.error("dataset_description.json failed validation")
            all_valid = False
    except json.JSONDecodeError as e:
        logger.error("dataset_description.json is not valid JSON: %s", e)
        all_valid = False
    except Exception as e:  # ← YENİ EKLENEN EXCEPTION HANDLER
        logger.error("Error reading dataset_description.json: %s", e)
        all_valid = False

    for fname in files:
        name_lower = fname.lower()
        file_path = os.path.join(folder_path, fname)
        _, ext = os.path.splitext(fname)
        ext = ext.lower()

        # readme
        if name_lower.startswith("readme") and ext in ALLOWED_TEXT_EXTS:
            logger.info("Validating %s...", fname)
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                readme_data = {}
                current_key = None
                current_value = []

                for line in content.split("\n"):
                    stripped = line.strip()
                    if stripped.startswith("#"):
                        if current_key:
                            readme_data[current_key] = "\n".join(current_value).strip()
                        current_key = stripped.lstrip("#").strip()
                        current_value = []
                    elif current_key:
                        current_value.append(stripped)

                if current_key:
                    readme_data[current_key] = "\n".join(current_value).strip()

                if validate_readme(readme_data):
                    logger.success("%s is valid", fname)
                else:
                    logger.error("%s failed validation", fname)
                    all_valid = False
            except Exception as e:
                logger.error("Error reading %s: %s", fname, e)
                all_valid = False

        # study_description
        elif name_lower.startswith("study_description") and ext in ALLOWED_TEXT_EXTS:
            logger.info("Validating %s...", fname)
            try:
                with open(file_path, encoding="utf-8") as f:
                    study_data = json.load(f)
                if validate_study_description(study_data):
                    logger.success("%s is valid", fname)
                else:
                    logger.error("%s failed validation", fname)
                    all_valid = False
            except json.JSONDecodeError as e:
                logger.error("%s is not valid JSON: %s", fname, e)
                all_valid = False
            except Exception as e:  # ← YENİ EKLENEN EXCEPTION HANDLER
                logger.error("Error reading %s: %s", fname, e)
                all_valid = False

        # changelog — no dedicated validator, just check extension
        elif name_lower.startswith("changelog"):
            if ext not in ALLOWED_TEXT_EXTS:
                logger.error("Invalid extension for %s", fname)
                all_valid = False
            else:
                logger.info("Found changelog file: %s (no schema validator)", fname)

        # license
        elif name_lower.startswith("license"):
            logger.info("Validating license in %s...", fname)
            try:
                with open(file_path, encoding="utf-8") as f:
                    license_text = f.read().strip()
                if validate_license(license_text):
                    logger.success("%s has a valid license identifier", fname)
                else:
                    logger.error("%s has an invalid license identifier: '%s'", fname, license_text)
                    all_valid = False
            except Exception as e:
                logger.error("Error reading %s: %s", fname, e)
                all_valid = False

    # participants files (anywhere in the folder tree) ───────────────────────
    for dirpath, _, filenames in os.walk(folder_path):
        for fname in filenames:
            if fname.lower().startswith("participants") and fname.lower().endswith(".tsv"):
                file_path = os.path.join(dirpath, fname)
                logger.info("Validating participants file: %s...", file_path)
                try:
                    with open(file_path, encoding="utf-8") as f:
                        reader = csv.DictReader(f, delimiter="\t")
                        participants_data = list(reader)
                    if validate_participants(participants_data):
                        logger.success("%s is valid", file_path)
                    else:
                        logger.error("%s failed validation", file_path)
                        all_valid = False
                except Exception as e:
                    logger.error("Error reading %s: %s", file_path, e)
                    all_valid = False
    # ── DONE ───────────────────────────────────────────────────────────────────
    if all_valid:
        logger.success("All files fully validated")
    else:
        logger.error("Validation completed with errors")

    return all_valid


validate_folder_structure("tests")