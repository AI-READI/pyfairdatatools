import os

from pyfairdatatools.generate import generate_dataset_description

minimal_valid_data = {
    "Identifier": {
        "identifierValue": "10.5281/zenodo.1234567",
        "identifierType": "DOI",
    },
    "Title": [
        {
            "titleValue": "Main Title",
        }
    ],
    "Creator": [
        {
            "creatorName": "Doe, John",
            "nameType": "Personal",
        },
        {
            "creatorName": "Doe, John1",
            "nameType": "Personal",
        },
    ],
    "PublicationYear": "2023",
    "ResourceType": {
        "resourceTypeValue": "Diabetes",
        "resourceTypeGeneral": "Dataset",
    },
    "DatasetRecordKeys": {"keysType": "Anonymised"},
    "DatasetDeIdentLevel": {
        "deIdentType": "NoDeIdentification",
        "deIdentDirect": True,
        "deIdentHIPAA": True,
        "deIdentDates": True,
        "deIdentNonarr": True,
        "deIdentKAnon": True,
    },
    "DatasetConsent": {
        "consentType": "NoRestriction",
        "consentNoncommercial": True,
        "consentGeogRestrict": True,
        "consentResearchType": True,
        "consentGeneticOnly": True,
        "consentNoMethods": True,
    },
    "ManagingOrganisation": {
        "name": "Test Organisation",
    },
    "AccessType": "PublicOnScreenAccess",
    "AccessDetails": {"description": "Some description"},
    "Publisher": "GitHub",
}


def test_main():
    output_path = os.path.join(
        os.getcwd(), "tests", "output", "test_dataset_description.xml"
    )

    generate_dataset_description(
        data=minimal_valid_data, file_path=output_path, file_type="xml"
    )


test_main()
