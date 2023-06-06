"""Unit tests for pyfairdatatools.validate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501


from pyfairdatatools.validate import (
    validate_dataset_description,
    validate_license,
    validate_participants,
    validate_readme,
)


class TestValidateDatasetDescription:
    def test_minimal_valid_dataset_description(self):
        data = {
            "Identifier": {
                "identifierValue": "10.5281/zenodo.1234567",
                "identifierType": "DOI",
            },
            "Title": [
                {
                    "titleValue": "Main Title",
                    TODO: "titleType": "blank or non existing?"
                }
            ],
            "Creator": [
                {
                    "creatorName": "Doe, John",
                    "nameType": "Personal",
                }
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

        output = validate_dataset_description(data)

        assert output is True


class TestValidateReadme:
    def test_minimal_valid_readme(self):
        data = {"Title": "Test Title"}

        output = validate_readme(data)

        assert output is True

    def test_valid_readme_with_all_fields(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "Version": "1.0.0",
            "PublicationDate": "2021-01-01",
            "About": "Test about",
            "DatasetDescription": "Test dataset description",
            "DatasetAccess": "Test dataset access",
            "StandardsFolllowed": "Test standards followed",
            "Resources": "Test resources",
            "License": "Test license",
            "HowToCite": "Test how to cite",
            "Acknowledgement": "Test acknowledgement",
        }

        output = validate_readme(data)

        assert output is True

    def test_fail_invalid_title(self):
        data = {"Title": 1}

        output = validate_readme(data)

        assert output is False

    def test_fail_invalid_identifier(self):
        data = {"Title": "Test Title", "Identifier": 1}

        output = validate_readme(data)

        assert output is False

    def test_fail_invalid_publication_date(self):
        data = {"Title": "Test Title", "PublicationDate": "Invalid"}

        output = validate_readme(data)

        assert output is False


class TestValidateLicense:
    def test_valid_license(self):
        data = "CC-BY-4.0"

        output = validate_license(data)

        assert output is True

    def test_fail_invalid_license(self):
        data = {
            "License": "Invalid",
        }

        output = validate_license(data)

        assert output is False


class TestValidateParticipants:
    def test_minimal_valid_participant(self):
        data = [
            {
                "participant_id": "sub-user1",
            }
        ]

        output = validate_participants(data)

        assert output is True

    def test_valid_participant_with_all_fields(self):
        data = [
            {
                "participant_id": "sub-user1",
                "species": "homo sapiens",
                "age": 0.5,
                "sex": "Female",
                "handedness": "Right",
                "strain": "C57BL/6J",
                "strain_rrid": "RRID:IMSR_JAX:000664",
            }
        ]

        output = validate_participants(data)

        assert output is True

    def test_invalid_participant_id(self):
        data: list[dict[str, str]] = [{}]

        output = validate_participants(data)

        assert output is False

        data = [{"participant_id": "bus-asd"}]

        output = validate_participants(data)

        assert output is False

    def test_invalid_age(self):
        data = [{"participant_id": "sub-sample1", "age": 0}]

        output = validate_participants(data)

        assert output is False

        data = [{"participant_id": "sub-sample1", "age": -5}]

        output = validate_participants(data)

        assert output is False

        data = [{"participant_id": "sub-sample1", "age": "5"}]

        output = validate_participants(data)

        assert output is False

    def test_invalid_sex(self):
        data = [{"participant_id": "sub-sample1", "sex": 0}]

        output = validate_participants(data)

        assert output is False

        data = [{"participant_id": "sub-sample1", "sex": "Invalid"}]

        output = validate_participants(data)

        assert output is False

    def test_invalid_handedness(self):
        data = [{"participant_id": "sub-sample1", "handedness": 0}]

        output = validate_participants(data)

        assert output is False

        data = [{"participant_id": "sub-sample1", "handedness": "Invalid"}]

        output = validate_participants(data)

        assert output is False
