import os

import requests
import random
import validators
from validators import ValidationFailure
import string


def feet_to_meters(feet):
    """Convert feet to meters."""
    try:
        value = float(feet)
    except ValueError as error:
        print(f"Could not convert {feet} to float")
        raise ValueError(f"Invalid input: {feet}") from error

    return (0.3048 * value * 10000.0 + 0.5) / 10000.0


def requestJSON(url):
    """Make a GET request to a URL and return the JSON response."""
    try:
        response = requests.request("GET", url, headers={}, data={}, timeout=5)

        return response.json()
    except Exception as e:
        raise e


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

    if writable and os.access(file_path, os.W_OK):
        print("File path is not writable.")
        raise PermissionError("Permission denied")

    return True


def validate_url(url_string):
    """Validate a URL string"""
    result = validators.url(url_string)

    return False if isinstance(result, ValidationFailure) else result


def generate_random_identifier(k):
    """Generate a random identifier"""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


def convert_for_datacite(data):
    """Converts a dictionary to a format that is compatible with the DOI registration payload"""
    doi = f"10.82914/fairhub.{generate_random_identifier(7)}"
    creators = []
    titles = []
    subjects = []
    contributors = []
    dates = []
    alternate_identifiers = []
    funding_references = []
    rights_list = []
    descriptions = []
    identifiers_list = []
    related_identifiers = []

    resource_type = {
        "resourceTypeGeneral": data["resourceType"]["resourceTypeGeneral"],
        "resourceType": data["resourceType"]["resourceTypeValue"],
    }

    identifier_obj = {
        "identifier": data["identifier"]["identifierValue"],
        "identifierType": data["identifier"]["identifierType"],
    }
    identifiers_list.append(identifier_obj)

    if "relatedIdentifier" in data:
        for related_identifier in data["relatedIdentifier"]:
            related_id_obj = {
                "relatedIdentifier": related_identifier["relatedIdentifierValue"],
                "relatedIdentifierType": related_identifier["relatedIdentifierType"],
                "relationType": related_identifier["relationType"],
            }
            if "relatedMetadataScheme" in related_identifier:
                related_id_obj["relatedMetadataScheme"] = related_identifier[
                    "relatedMetadataScheme"
                ]

            if "schemeURI" in related_identifier:
                related_id_obj["schemeUri"] = related_identifier["schemeURI"]

            if "schemeType" in related_identifier:
                related_id_obj["schemeType"] = related_identifier["schemeType"]

            if "resourceTypeGeneral" in related_identifier:
                related_id_obj["resourceTypeGeneral"] = related_identifier[
                    "resourceTypeGeneral"
                ]

            related_identifiers.append(related_id_obj)

    if "description" in data:
        for description in data["description"]:
            description_obj = {
                "description": description["descriptionValue"],
                "descriptionType": description["descriptionType"],
            }
            descriptions.append(description_obj)

    for rights in data["rights"]:
        rights_obj = {"rights": rights["rightsName"]}
        if "rightsURI" in rights:
            rights_obj["rightsUri"] = rights["rightsURI"]
        if (
            "rightsIdentifier" in rights
            and "rightsIdentifierValue" in rights["rightsIdentifier"]
        ):
            rights_obj["rightsIdentifier"] = rights["rightsIdentifier"][
                "rightsIdentifierValue"
            ]
        if (
            "rightsIdentifier" in rights
            and "rightsIdentifierScheme" in rights["rightsIdentifier"]
        ):
            rights_obj["rightsIdentifierScheme"] = rights["rightsIdentifier"][
                "rightsIdentifierScheme"
            ]
        if "rightsIdentifier" in rights and "schemeURI" in rights["rightsIdentifier"]:
            rights_obj["schemeUri"] = rights["rightsIdentifier"]["schemeURI"]
        rights_list.append(rights_obj)

    if "alternateIdentifier" in data:
        for alternate_identifier in data["alternateIdentifier"]:
            alternate_identifiers.append(
                {
                    "alternateIdentifier": alternate_identifier[
                        "alternateIdentifierValue"
                    ],
                    "alternateIdentifierType": alternate_identifier[
                        "alternateIdentifierType"
                    ],
                }
            )

    if "date" in data:
        for date in data["date"]:
            date_obj = {
                "date": date["dateValue"],
                "dateType": date["dateType"],
            }
            if "dateInformation" in date:
                date_obj["dateInformation"] = date["dateInformation"]
            dates.append(date_obj)

    if "contributor" in data:
        for contributor in data["contributor"]:
            if "affiliation" in contributor:
                contributor_affiliations = []
                for affiliation in contributor["affiliation"]:
                    # TODO: VERIFY BY KEY IS AFFILIATIONVALUE AND NOT NAME
                    affiliate = {
                        "name": affiliation["affiliationName"],
                    }
                    if (
                        "affiliationIdentifier" in affiliation
                        and "schemeURI" in affiliation["affiliationIdentifier"]
                    ):
                        affiliate["schemeUri"] = affiliation["affiliationIdentifier"][
                            "schemeURI"
                        ]
                    if (
                        "affiliationIdentifier" in affiliation
                        and "affiliationIdentifierScheme"
                        in affiliation["affiliationIdentifier"]
                    ):
                        affiliate["affiliationIdentifierScheme"] = affiliation[
                            "affiliationIdentifier"
                        ]["affiliationIdentifierScheme"]
                    if (
                        "affiliationIdentifier" in affiliation
                        and "affiliationIdentifierValue"
                        in affiliation["affiliationIdentifier"]
                    ):
                        affiliate["affiliationIdentifier"] = affiliation[
                            "affiliationIdentifier"
                        ]["affiliationIdentifierValue"]

                    contributor_affiliations.append(affiliate)
            if "nameIdentifier" in contributor:
                name_identifiers = []
                for name_identifier in contributor["nameIdentifier"]:
                    name_identifier = {
                        "nameIdentifier": name_identifier["nameIdentifierValue"],
                        "nameIdentifierScheme": name_identifier["nameIdentifierScheme"],
                    }
                    if "schemeURI" in name_identifier:
                        name_identifier["schemeURI"] = name_identifier["schemeURI"]
                    name_identifiers.append(name_identifier)

            contributor_obj = {
                "name": contributor["contributorName"],
                "nameType": contributor["nameType"],
                "contributorType": contributor["contributorType"],
            }
            if contributor_affiliations:
                contributor_obj["affiliation"] = contributor_affiliations
            if name_identifiers:
                contributor_obj["nameIdentifiers"] = name_identifiers

            contributors.append(contributor_obj)

    if "subject" in data:
        for subject in data["subject"]:
            subject_obj = {}
            if "classificationCode" in subject:
                subject_obj["classificationCode"] = subject["classificationCode"]
            if "subjectScheme" in subject:
                subject_obj["subjectScheme"] = subject["subjectScheme"]
            if "schemeURI" in subject:
                subject_obj["schemeUri"] = subject["schemeURI"]
            subject_obj["subject"] = subject["subjectValue"]
            subjects.append(subject_obj)

    for title in data["title"]:
        title_obj = {"title": title["titleValue"]}
        if "titleType" in title:
            title_obj["titleType"] = title["titleType"]
        titles.append(title_obj)

    for creator in data["creator"]:
        if "affiliation" in creator:
            creator_affiliations = []
            for affiliation in creator["affiliation"]:
                affiliate = {
                    "name": affiliation["affiliationName"],
                }
                if (
                    "affiliationIdentifier" in affiliation
                    and "schemeURI" in affiliation
                ):
                    affiliate["schemeUri"] = affiliation["affiliationIdentifier"][
                        "schemeURI"
                    ]
                if (
                    "affiliationIdentifier" in affiliation
                    and "affiliationIdentifierScheme" in affiliation
                ):
                    affiliate["affiliationIdentifierScheme"] = affiliation[
                        "affiliationIdentifier"
                    ]["affiliationIdentifierScheme"]
                if (
                    "affiliationIdentifier" in affiliation
                    and "affiliationIdentifier" in affiliation
                ):
                    affiliate["affiliationIdentifier"] = affiliation[
                        "affiliationIdentifier"
                    ]["affiliationIdentifierValue"]

                creator_affiliations.append(affiliate)
        if "nameIdentifier" in creator:
            name_identifiers = []
            for name_identifier in creator["nameIdentifier"]:
                name_identifier = {
                    "nameIdentifier": name_identifier["nameIdentifierValue"],
                    "nameIdentifierScheme": name_identifier["nameIdentifierScheme"],
                }
                if "schemeURI" in name_identifier:
                    name_identifier["schemeURI"] = name_identifier["schemeURI"]
                name_identifiers.append(name_identifier)

        creator_obj = {
            "name": creator["creatorName"],
            "nameType": creator["nameType"],
        }
        if creator_affiliations:
            creator_obj["affiliation"] = creator_affiliations
        if name_identifiers:
            creator_obj["nameIdentifiers"] = name_identifiers

        creators.append(creator_obj)

    if "fundingReference" in data:
        for funding_reference in data["fundingReference"]:
            funder_obj = {"funderName": funding_reference["funderName"]}
            if (
                "funderIdentifier" in funding_reference
                and "funderIdentifierValue" in funding_reference["funderIdentifier"]
            ):
                funder_obj["funderIdentifer"] = funding_reference["funderIdentifier"][
                    "funderIdentifierValue"
                ]
            if (
                "funderIdentifier" in funding_reference
                and "funderIdentifierType" in funding_reference["funderIdentifier"]
            ):
                funder_obj["funderIdentifierType"] = funding_reference[
                    "funderIdentifier"
                ]["funderIdentifierType"]

            if "awardNumber" in funding_reference:
                funder_obj["awardNumber"] = funding_reference["awardNumber"][
                    "awardNumberValue"
                ]
                if "awardURI" in funding_reference["awardNumber"]:
                    funder_obj["awardURI"] = funding_reference["awardNumber"][
                        "awardURI"
                    ]
            if "awardTitle" in funding_reference["awardNumber"]:
                funder_obj["awardTitle"] = funding_reference["awardNumber"][
                    "awardTitle"
                ]
            funding_references.append(funder_obj)

    payload = {
        "data": {
            "type": "dois",
            "attributes": {
                "event": "publish",
                "doi": doi,
                "identifiers": identifiers_list,
                "creators": creators,
                "titles": titles,
                "publisher": {"name": data["publisher"]["publisherName"]},
                "publicationYear": data["publicationYear"],
                "rightsList": rights_list,
                "types": resource_type,
                "version": data["version"],
                "url": "https://staging.fairhub.io/datasets/3",
            },
        }
    }

    if "relatedIdentifier" in data and len(data["relatedIdentifier"]) > 0:
        payload["data"]["attributes"]["relatedIdentifiers"] = data["relatedIdentifier"]
    if "size" in data and len(data["size"]) > 0:
        payload["data"]["attributes"]["sizes"] = data["size"]
    if "format" in data and len(data["format"]) > 0:
        payload["data"]["attributes"]["formats"] = data["format"]
    if "language" in data and len(data["language"]) > 0:
        payload["data"]["attributes"]["language"] = data["language"]

    if len(descriptions) > 0:
        payload["data"]["attributes"]["description"] = descriptions
    if len(alternate_identifiers) > 0:
        payload["data"]["attributes"]["alternateIdentifiers"] = alternate_identifiers
    if len(funding_references) > 0:
        payload["data"]["attributes"]["fundingReferences"] = funding_references
    if len(contributors) > 0:
        payload["data"]["attributes"]["contributors"] = contributors
    if len(subjects) > 0:
        payload["data"]["attributes"]["subjects"] = subjects
    if len(dates) > 0:
        payload["data"]["attributes"]["dates"] = dates
    if len(related_identifiers) > 0:
        payload["data"]["attributes"]["relatedIdentifiers"] = related_identifiers

    return payload
