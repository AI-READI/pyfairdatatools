"""Unit tests for pyfairdatatools.generate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

import json
from os import path

from pyfairdatatools.generate import (
    generate_changelog_file,
    generate_dataset_description,
    generate_license_file,
    generate_readme,
)


class TestGenerateDatasetDescription:
    def test_minimal_valid_dataset_description(self, tmp_path):
        data = {
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

        file = tmp_path / "dataset_description.json"
        file_type = "json"

        generate_dataset_description(data, file, file_type)

        assert path.exists(file) is True

        with open(file, "r", encoding="utf8") as f:
            imported_data = json.load(f)

        assert imported_data == data

        file = tmp_path / "dataset_description.xml"
        file_type = "xml"

        generate_dataset_description(data, file, file_type)


class TestGenerateReadme:
    def test_minimal_valid_readme(self, tmp_path):
        data = {
            "Title": "Test Title",
        }

        file = tmp_path / "readme.md"
        file_type = "md"

        print(file)

        generate_readme(data, file, file_type)

        assert path.exists(file) is True


class TestGenerateChangelog:
    def test_minimal_valid_changelog(self, tmp_path):
        data = "Test Changelog"

        file = tmp_path / "changelog.md"
        file_type = "md"

        print(file)

        generate_changelog_file(data, file, file_type)

        assert path.exists(file) is True


class TestGenerateLicense:
    def test_valid_license_with_data(self, tmp_path):
        data = "Test License"

        file = tmp_path / "license.md"
        file_type = "md"

        print(file)

        generate_license_file(file_path=file, file_type=file_type, data=data)

        assert path.exists(file) is True

    def test_valid_license_with_identifier(self, tmp_path):
        identifier = "MIT"

        file = tmp_path / "license.md"
        file_type = "md"

        print(file)

        generate_license_file(
            file_path=file, file_type=file_type, identifier=identifier
        )

        assert path.exists(file) is True
