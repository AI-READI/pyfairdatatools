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


def generate_random_identifier(k):
    """Generate a random identifier"""
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


def convert_for_datasite(data):
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

    for description in dataset_description["Description"]:
        description_obj = {
            "description": description["descriptionValue"],
            "descriptionType": description["descriptionType"],
        }
        descriptions.append(description_obj)

    for rights in dataset_description["Rights"]:
        rights_obj = {"rights": rights["rightsValue"]}
        if "rightsURI" in rights:
            rights_obj["rightsUri"] = rights["rightsURI"]
        if "rightsIdentifier" in rights:
            rights_obj["rightsIdentifier"] = rights["rightsIdentifier"]
        if "rightsIdentifierScheme" in rights:
            rights_obj["rightsIdentifierScheme"] = rights["rightsIdentifierScheme"]
        rights_list.append(rights_obj)

    for funder in dataset_description["FundingReference"]:
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

    for related_item in dataset_description["RelatedItem"]:
        if "relatedItemIdentifier" in related_item:
            related_item_identifiers = []
            for identifier in related_item["relatedItemIdentifier"]:
                identifier_obj = {
                    "relatedItemIdentifier": identifier["relatedItemIdentifierValue"],
                    "relatedItemIdentifierType": identifier[
                        "relatedItemIdentifierType"
                    ],
                }
                if "relatedMetadataScheme" in identifier:
                    identifier_obj["relatedMetadataScheme"] = identifier[
                        "relatedMetadataScheme"
                    ]
                if "schemeURI" in identifier:
                    identifier_obj["schemeUri"] = identifier["schemeURI"]
                if "schemeType" in identifier:
                    identifier_obj["schemeType"] = identifier["schemeType"]

                related_item_identifiers.append(identifier_obj)
        if "title" in related_item:
            related_item_titles = []
            for title in related_item["title"]:
                title_obj = {
                    "title": title["titleValue"]
                }
                if "titleType" in title:
                    title_obj["titleType"] = title["titleType"]
                related_item_titles.append(title_obj)
        if "creator" in related_item:
            related_item_creators = []
            for creator in related_item["creator"]:
                creator_obj = {
                    "name": creator["creatorName"],
                    "nameType": creator["nameType"],
                }
                related_item_creators.append(creator_obj)
        if "contributor" in related_item:
            related_item_contributors = []
            for contributor in related_item["contributor"]:
                contributor_obj = {
                    "name": contributor["contributorName"],
                    "contributorType": contributor["contributorType"],
                }
                if "nameType" in contributor:
                    contributor_obj["nameType"] = contributor["nameType"]
                related_item_contributors.append(contributor_obj)

        related_item_obj = {
            "relationType": related_item["relationType"],
            "relatedItemType": related_item["relatedItemType"],
        }
        if related_item_creators:
            related_item_obj["creators"] = related_item_creators
        if related_item_contributors:
            related_item_obj["contributors"] = related_item_contributors
        if related_item_titles:
            related_item_obj["titles"] = related_item_titles
        if related_item_identifiers:
            related_item_obj["relatedItemIdentifier"] = related_item_identifiers
        if "publicationYear" in related_item:
            related_item_obj["publicationYear"] = related_item["publicationYear"]
        if "volume" in related_item:
            related_item_obj["volume"] = related_item["volume"]
        if "issue" in related_item:
            related_item_obj["issue"] = related_item["issue"]
        if "number" in related_item and "numberValue" in related_item["number"]:
            related_item_obj["number"] = related_item["number"]["numberValue"]
        if "number" in related_item and "numberType" in related_item["number"]:
            related_item_obj["numberType"] = related_item["number"]["numberType"]
        if "firstPage" in related_item:
            related_item_obj["firstPage"] = related_item["firstPage"]
        if "lastPage" in related_item:
            related_item_obj["last_page"] = related_item["lastPage"]
        if "publisher" in related_item:
            related_item_obj["publisher"] = related_item["publisher"]
        if "edition" in related_item:
            related_item_obj["edition"] = related_item["edition"]

        related_items.append(related_item_obj)

    for alternate_identifier in dataset_description["AlternateIdentifier"]:
        alternate_identifiers.append(
            {
                "alternateIdentifier": alternate_identifier["alternateIdentifierValue"],
                "alternateIdentifierType": alternate_identifier[
                    "alternateIdentifierType"
                ],
            }
        )

    for date in dataset_description["Date"]:
        date_obj = {
            "date": date["dateValue"],
            "dateType": date["dateType"],
        }
        if "dateInformation" in date:
            date_obj["dateInformation"] = date["dateInformation"]
        dates.append(date_obj)

    for contributor in dataset_description["Contributor"]:
        if "affiliation" in contributor:
            contributor_affiliations = []
            for affiliation in contributor["affiliation"]:
                # TODO: VERIFY BY KEY IS AFFILIATIONVALUE AND NOT NAME
                affiliate = {
                    "name": affiliation["affiliationValue"],
                }
                if "schemeURI" in affiliation:
                    affiliate["schemeUri"] = affiliation["schemeURI"]
                if "affiliationIdentifierScheme" in affiliation:
                    affiliate["affiliationIdentifierScheme"] = affiliation[
                        "affiliationIdentifierScheme"
                    ]
                if "affiliationIdentifier" in affiliation:
                    affiliate["affiliationIdentifier"] = affiliation[
                        "affiliationIdentifier"
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

    for subject in dataset_description["Subject"]:
        subject_obj = {}
        if "classificationCode" in subject:
            subject_obj["classificationCode"] = subject["classificationCode"]
        if "subjectScheme" in subject:
            subject_obj["subjectScheme"] = subject["subjectScheme"]
        if "schemeURI" in subject:
            subject_obj["schemeUri"] = subject["schemeURI"]
        subject_obj["subject"] = subject["subjectValue"]
        subjects.append(subject_obj)

    for title in dataset_description["Title"]:
        title_obj = {"title": title["titleValue"]}
        if "titleType" in title:
            title_obj["titleType"] = title["titleType"]
        titles.append(title_obj)

    for creator in dataset_description["Creator"]:
        if "affiliation" in creator:
            creator_affiliations = []
            for affiliation in creator["affiliation"]:
                affiliate = {
                    "name": affiliation["affiliationValue"],
                }
                if "schemeURI" in affiliation:
                    affiliate["schemeUri"] = affiliation["schemeURI"]
                if "affiliationIdentifierScheme" in affiliation:
                    affiliate["affiliationIdentifierScheme"] = affiliation[
                        "affiliationIdentifierScheme"
                    ]
                if "affiliationIdentifier" in affiliation:
                    affiliate["affiliationIdentifier"] = affiliation[
                        "affiliationIdentifier"
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

    for funding_reference in dataset_description["FundingReference"]:
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
                "publisher": {"name": dataset_description["Publisher"]},
                "publicationYear": dataset_description["PublicationYear"],
                "subjects": subjects,
                "contributors": dataset_description["Contributor"],
                "dates": dates,
                "alternateIdentifiers": alternate_identifiers,
                "language": dataset_description["Language"],
                "types": dataset_description["ResourceType"],
                "relatedItems": related_items,
                "rightsList": rights_list,
                "description": descriptions,
                "version": dataset_description["Version"],
                "fundingReferences": funding_references,
                "url": "https://staging.fairhub.io/datasets/2",
            },
        }
    }

    if len(dataset_description["RelatedIdentifier"]) > 0:
        payload["data"]["attributes"]["relatedIdentifiers"] = dataset_description[
            "RelatedIdentifier"
        ]
    if len(dataset_description["Size"]) > 0:
        payload["data"]["attributes"]["sizes"] = dataset_description["Size"]

    return payload
