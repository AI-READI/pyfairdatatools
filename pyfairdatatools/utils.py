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
    related_items = []
    funding_references = []
    rights_list = []
    descriptions = []

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
        if "rightsIdentifier" in rights and "rightsIdentifierValue" in rights["rightsIdentifier"]:
            rights_obj["rightsIdentifier"] = rights["rightsIdentifier"]["rightsIdentifierValue"]
        if "rightsIdentifier" in rights and "rightsIdentifierScheme" in rights["rightsIdentifier"]:
            rights_obj["rightsIdentifierScheme"] = rights["rightsIdentifier"]["rightsIdentifierScheme"]
        if "rightsIdentifier" in rights and "schemeURI" in rights["rightsIdentifier"]:
            rights_obj["schemeUri"] = rights["rightsIdentifier"]["schemeURI"]
        rights_list.append(rights_obj)

    for funder in data["fundingReference"]:
        funder_obj = {
            "funderName": funder["funderName"],
            "funderIdentifier": funder["funderIdentifier"]["funderIdentifierValue"],
            "awardNumber": funder["awardNumber"]["awardNumberValue"],
        }
        if "awardURI" in funder["awardNumber"]:
            funder_obj["awardUri"] = funder["awardNumber"]["awardURI"]
        if "awardTitle" in funder["awardNumber"]:
            funder_obj["awardTitle"] = funder["awardNumber"]["awardTitle"]
        if "funderIentifierType" in funder["funderIdentifier"]:
            funder_obj["funderIdentifierType"] = funder["funderIdentifier"][
                "funderIdentifierType"
            ]
        funding_references.append(funder_obj)

    # for related_item in data["RelatedItem"]:
    #     if "relatedItemIdentifier" in related_item:
    #         related_item_identifiers = []
    #         for identifier in related_item["relatedItemIdentifier"]:
    #             identifier_obj = {
    #                 "relatedItemIdentifier": identifier["relatedItemIdentifierValue"],
    #                 "relatedItemIdentifierType": identifier[
    #                     "relatedItemIdentifierType"
    #                 ],
    #             }
    #             if "relatedMetadataScheme" in identifier:
    #                 identifier_obj["relatedMetadataScheme"] = identifier[
    #                     "relatedMetadataScheme"
    #                 ]
    #             if "schemeURI" in identifier:
    #                 identifier_obj["schemeUri"] = identifier["schemeURI"]
    #             if "schemeType" in identifier:
    #                 identifier_obj["schemeType"] = identifier["schemeType"]

    #             related_item_identifiers.append(identifier_obj)
    #     if "title" in related_item:
    #         related_item_titles = []
    #         for title in related_item["title"]:
    #             title_obj = {"title": title["titleValue"]}
    #             if "titleType" in title:
    #                 title_obj["titleType"] = title["titleType"]
    #             related_item_titles.append(title_obj)
    #     if "creator" in related_item:
    #         related_item_creators = []
    #         for creator in related_item["creator"]:
    #             creator_obj = {
    #                 "name": creator["creatorName"],
    #                 "nameType": creator["nameType"],
    #             }
    #             related_item_creators.append(creator_obj)
    #     if "contributor" in related_item:
    #         related_item_contributors = []
    #         for contributor in related_item["contributor"]:
    #             contributor_obj = {
    #                 "name": contributor["contributorName"],
    #                 "contributorType": contributor["contributorType"],
    #             }
    #             if "nameType" in contributor:
    #                 contributor_obj["nameType"] = contributor["nameType"]
    #             related_item_contributors.append(contributor_obj)

    #     related_item_obj = {
    #         "relationType": related_item["relationType"],
    #         "relatedItemType": related_item["relatedItemType"],
    #     }
    #     if related_item_creators:
    #         related_item_obj["creators"] = related_item_creators
    #     if related_item_contributors:
    #         related_item_obj["contributors"] = related_item_contributors
    #     if related_item_titles:
    #         related_item_obj["titles"] = related_item_titles
    #     if related_item_identifiers:
    #         related_item_obj["relatedItemIdentifier"] = related_item_identifiers
    #     if "publicationYear" in related_item:
    #         related_item_obj["publicationYear"] = related_item["publicationYear"]
    #     if "volume" in related_item:
    #         related_item_obj["volume"] = related_item["volume"]
    #     if "issue" in related_item:
    #         related_item_obj["issue"] = related_item["issue"]
    #     if "number" in related_item and "numberValue" in related_item["number"]:
    #         related_item_obj["number"] = related_item["number"]["numberValue"]
    #     if "number" in related_item and "numberType" in related_item["number"]:
    #         related_item_obj["numberType"] = related_item["number"]["numberType"]
    #     if "firstPage" in related_item:
    #         related_item_obj["firstPage"] = related_item["firstPage"]
    #     if "lastPage" in related_item:
    #         related_item_obj["last_page"] = related_item["lastPage"]
    #     if "publisher" in related_item:
    #         related_item_obj["publisher"] = related_item["publisher"]
    #     if "edition" in related_item:
    #         related_item_obj["edition"] = related_item["edition"]

    #     related_items.append(related_item_obj)

    for alternate_identifier in data["alternateIdentifier"]:
        alternate_identifiers.append(
            {
                "alternateIdentifier": alternate_identifier["alternateIdentifierValue"],
                "alternateIdentifierType": alternate_identifier[
                    "alternateIdentifierType"
                ],
            }
        )

    for date in data["date"]:
        date_obj = {
            "date": date["dateValue"],
            "dateType": date["dateType"],
        }
        if "dateInformation" in date:
            date_obj["dateInformation"] = date["dateInformation"]
        dates.append(date_obj)

    for contributor in data["contributor"]:
        if "affiliation" in contributor:
            contributor_affiliations = []
            for affiliation in contributor["affiliation"]:
                # TODO: VERIFY BY KEY IS AFFILIATIONVALUE AND NOT NAME
                affiliate = {
                    "name": affiliation["affiliationName"],
                }
                if "affiliationIdentifier" in affiliation and "schemeURI" in affiliation["affiliationIdentifier"]:
                    affiliate["schemeUri"] = affiliation["affiliationIdentifier"]["schemeURI"]
                if "affiliationIdentifier" in affiliation and "affiliationIdentifierScheme" in affiliation["affiliationIdentifier"]:
                    affiliate["affiliationIdentifierScheme"] = affiliation["affiliationIdentifier"][
                        "affiliationIdentifierScheme"
                    ]
                if "affiliationIdentifier" in affiliation and "affiliationIdentifierValue" in affiliation["affiliationIdentifier"]:
                    affiliate["affiliationIdentifier"] = affiliation["affiliationIdentifier"][
                        "affiliationIdentifierValue"
                    ]

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
                if "affiliationIdentifier" in affiliation and "schemeURI" in affiliation:
                    affiliate["schemeUri"] = affiliation["affiliationIdentifier"]["schemeURI"]
                if "affiliationIdentifier" in affiliation and "affiliationIdentifierScheme" in affiliation:
                    affiliate["affiliationIdentifierScheme"] = affiliation["affiliationIdentifier"][
                        "affiliationIdentifierScheme"
                    ]
                if "affiliationIdentifier" in affiliation and "affiliationIdentifier" in affiliation:
                    affiliate["affiliationIdentifier"] = affiliation["affiliationIdentifier"][
                        "affiliationIdentifierValue"
                    ]

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
            funder_obj["funderIdentifierType"] = funding_reference["funderIdentifier"][
                "funderIdentifierType"
            ]

    payload = {
        "data": {
            "type": "dois",
            "attributes": {
                "event": "publish",
                "doi": doi,
                "creators": creators,
                "titles": titles,
                "publisher": {"name": data["publisher"]},
                "publicationYear": data["publicationYear"],
                "subjects": subjects,
                "contributors": contributors,
                "dates": dates,
                "alternateIdentifiers": alternate_identifiers,
                "language": data["language"],
                "types": data["resourceType"],
                # "relatedItems": related_items,
                "rightsList": rights_list,
                "description": descriptions,
                "version": data["version"],
                "fundingReferences": funding_references,
                "url": "https://staging.fairhub.io/datasets/2",
            },
        }
    }

    if len(data["relatedIdentifier"]) > 0:
        payload["data"]["attributes"]["relatedIdentifiers"] = data["relatedIdentifier"]
    if len(data["size"]) > 0:
        payload["data"]["attributes"]["sizes"] = data["size"]

    return payload
