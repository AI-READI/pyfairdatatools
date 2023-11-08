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

        Contributors = data["Contributor"]

        for Contributor in Contributors:
            if "affilation" in Contributor:
                affiliations = Contributor["affilation"]

                for affiliation in affiliations:
                    if (
                        "affiliationValue" not in affiliation
                        and "affiliationIdentifier" not in affiliation
                    ):
                        print("affiliationValue or affiliationIdentifier is required.")
                        return False

                    if "affiliationIdentifier" in affiliation:
                        if "affiliationIdentifierScheme" not in affiliation:
                            print(
                                "affiliationIdentifierScheme is required if affiliationIdentifier is provided."  # pylint: disable=line-too-long
                            )
                            return False

        Creators = data["Creator"]

        for Creator in Creators:
            if "affilation" in Creator:
                affiliations = Creator["affilation"]

                for affiliation in affiliations:
                    if (
                        "affiliationValue" not in affiliation
                        and "affiliationIdentifier" not in affiliation
                    ):
                        print("affiliationValue or affiliationIdentifier is required.")
                        return False

                    if "affiliationIdentifier" in affiliation:
                        if "affiliationIdentifierScheme" not in affiliation:
                            print(
                                "affiliationIdentifierScheme is required if affiliationIdentifier is provided."  # pylint: disable=line-too-long
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

        OrgStudyIdType = data["IdentificationModule"]["OrgStudyIdInfo"][
            "OrgStudyIdType"
        ]

        if OrgStudyIdType in [
            "Other Grant/Funding Number",
            "Registry Identifier",
            "Other Identifier",
        ]:
            # check if the OrgStudyIdDomain key exists and is not empty
            if "OrgStudyIdDomain" not in data["IdentificationModule"]["OrgStudyIdInfo"]:
                print("OrgStudyIdDomain is required.")
                return False

            OrgStudyIdDomain = data["IdentificationModule"]["OrgStudyIdInfo"][
                "OrgStudyIdDomain"
            ]

            if OrgStudyIdDomain is None or OrgStudyIdDomain == "":
                print("A value for OrgStudyIdDomain is required.")
                return False

        if "SecondaryIdInfoList" in data["IdentificationModule"]:
            SecondaryIdInfoList = data["IdentificationModule"]["SecondaryIdInfoList"]

            for SecondaryIdInfo in SecondaryIdInfoList:
                SecondaryIdType = SecondaryIdInfo["SecondaryIdType"]

                if SecondaryIdType in [
                    "Other Grant/Funding Number",
                    "Registry Identifier",
                    "Other Identifier",
                ]:
                    # check if the SecondaryIdDomain key exists and is not empty
                    if "SecondaryIdDomain" not in SecondaryIdInfo:
                        print("SecondaryIdDomain is required.")
                        return False

                    SecondaryIdDomain = SecondaryIdInfo["SecondaryIdDomain"]

                    if SecondaryIdDomain is None or SecondaryIdDomain == "":
                        print("A value for SecondaryIdDomain is required")
                        return False

        OverallStatus = data["StatusModule"]["OverallStatus"]

        if OverallStatus in ["Suspended", "Completed", "Terminated"]:
            # check if the WhyStopped key exists and is not empty
            if "WhyStopped" not in data["StatusModule"]:
                print("WhyStopped is required.")
                return False

            WhyStopped = data["StatusModule"]["WhyStopped"]

            if WhyStopped is None or WhyStopped == "":
                print("A value for WhyStopped is required.")
                return False

        ResponsiblePartyType = data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyType"
        ]

        if ResponsiblePartyType in ["Principal Investigator", "Sponsor-Investigator"]:
            # check if the ResponsiblePartyInvestigatorFullName key exists
            # and is not empty
            if (
                "ResponsiblePartyInvestigatorFullName"
                not in data["SponsorCollaboratorsModule"]["ResponsibleParty"]
            ):
                print("ResponsiblePartyInvestigatorFullName is required.")
                return False

            ResponsiblePartyInvestigatorFullName = data["SponsorCollaboratorsModule"][
                "ResponsibleParty"
            ]["ResponsiblePartyInvestigatorFullName"]

            if (
                ResponsiblePartyInvestigatorFullName is None
                or ResponsiblePartyInvestigatorFullName == ""
            ):
                print("A value for ResponsiblePartyInvestigatorFullName is required.")
                return False

            # check if the ResponsiblePartyInvestigatorTitle key exists and is not empty
            if (
                "ResponsiblePartyInvestigatorTitle"
                not in data["SponsorCollaboratorsModule"]["ResponsibleParty"]
            ):
                print("ResponsiblePartyInvestigatorTitle is required.")
                return False

            ResponsiblePartyInvestigatorTitle = data["SponsorCollaboratorsModule"][
                "ResponsibleParty"
            ]["ResponsiblePartyInvestigatorTitle"]

            if (
                ResponsiblePartyInvestigatorTitle is None
                or ResponsiblePartyInvestigatorTitle == ""
            ):
                print("A value for ResponsiblePartyInvestigatorTitle is required.")
                return False

            # check if the ResponsiblePartyInvestigatorAffiliation key exists
            # and is not empty
            if (
                "ResponsiblePartyInvestigatorAffiliation"
                not in data["SponsorCollaboratorsModule"]["ResponsibleParty"]
            ):
                print("ResponsiblePartyInvestigatorAffiliation is required.")
                return False

            ResponsiblePartyInvestigatorAffiliation = data[
                "SponsorCollaboratorsModule"
            ]["ResponsibleParty"]["ResponsiblePartyInvestigatorAffiliation"]

            if (
                ResponsiblePartyInvestigatorAffiliation is None
                or ResponsiblePartyInvestigatorAffiliation == ""
            ):
                print(
                    "A value for ResponsiblePartyInvestigatorAffiliation is required."
                )
                return False

        StudyType = data["DesignModule"]["StudyType"]

        if StudyType == "Interventional":
            ArmGroupList = data["ArmsInterventionsModule"]["ArmGroupList"]

            for ArmGroup in ArmGroupList:
                if "ArmGroupType" not in ArmGroup:
                    print(
                        "ArmGroupType is required is required for interventional studies."  # pylint: disable=line-too-long
                    )
                    return False

            # check if the HealthyVolunteers key exists
            if "HealthyVolunteers" not in data["EligibilityModule"]:
                print("HealthyVolunteers is required for interventional studies.")
                return False

        if StudyType == "Observational":
            # check if the StudyPopulation key exists and is not empty
            if "StudyPopulation" not in data["EligibilityModule"]:
                print("StudyPopulation is required for observational studies.")
                return False

            StudyPopulation = data["EligibilityModule"]["StudyPopulation"]

            if StudyPopulation is None or StudyPopulation == "":
                print(
                    "A value for StudyPopulation is required for observational studies."
                )
                return False

            # check if the SamplingMethod key exists
            if "SamplingMethod" not in data["EligibilityModule"]:
                print("SamplingMethod is required for observational studies.")
                return False

        if ("CentralContactList" not in data["ContactsLocationsModule"]) or (
            "CentralContactList" in data["ContactsLocationsModule"]
            and len(data["ContactsLocationsModule"]["CentralContactList"]) == 0
        ):
            LocationList = data["ContactsLocationsModule"]["LocationList"]

            for Location in LocationList:
                if (
                    "LocationContactList" not in Location
                    or len(Location["LocationContactList"]) == 0
                ):
                    print(
                        "LocationContactList is required if no Central Contact is provided."  # pylint: disable=line-too-long
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
