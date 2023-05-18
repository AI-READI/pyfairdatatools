"""Unit tests for pyfairdatatools.validate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

from pyfairdatatools.validate import validate_dataset_description, validate_readme


class TestValidateDatasetDescription:
    def test_minimal_valid_dataset_description(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
        }

        output = validate_dataset_description(data)

        assert output is True

    def test_full_valid_dataset_description(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Subject": ["keyword1"],
            "Description": "Test description",
            "Language": "en",
            "StudyTitle": "Test study title",
            "StudyID": "Test study ID",
            "Creator": [
                {
                    "ContributorName": "Test contributor name",
                    "NameType": "Personal",
                    "Affiliation": "Test affiliation",
                    "ContributorType": "ContactPerson",
                    "ORCID": "0000-0002-1825-0097",
                }
            ],
            "RelatedItem": [
                {
                    "RelatedItemIdentifier": "10.5281/zenodo.1234567",
                    "RelatedItemIdentifierType": "DOI",
                    "RelatedItemType": "Collection",
                    "RelationType": "IsPartOf",
                }
            ],
            "FundingReference": [
                {
                    "FunderName": "Test funder name",
                    "FunderIdentifier": "10.13039/501100000000",
                    "FunderIdentifierType": "Crossref Funder ID",
                }
            ],
            "Version": "1.0",
            "Date": "2020-01-01",
            "AccessType": 13,
            "Rights": {
                "RightsURI": "https://creativecommons.org/licenses/by/4.0/",
                "RightsIdentifier": "cc-by-4.0",
                "RightsIdentifierScheme": "SPDX",
                "schemeURI": "https://spdx.org/licenses/",
            },
        }

        output = validate_dataset_description(data)

        assert output is True

    def test_fail_missing_title(self):
        data = {
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_missing_identifier(self):
        data = {
            "Title": "Test Title",
            "IdentifierType": "DOI",
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_missing_identifier_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_identifier_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "Invalid",
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_identifier(self):
        data = {
            "Title": "Test Title",
            "Identifier": "Invalid",
            "IdentifierType": "DOI",
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_subject(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Subject": [],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_description(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Description": 0,
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_language(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Language": 0,
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_study_title(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "StudyTitle": 0,
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_study_id(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "StudyID": 0,
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_creator_name_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Creator": [
                {
                    "ContributorName": "Test contributor name",
                    "NameType": "Invalid",
                    "Affiliation": "Test affiliation",
                    "ContributorType": "ContactPerson",
                    "ORCID": "0000-0002-1825-0097",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_creator_contributor_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Creator": [
                {
                    "ContributorName": "Test contributor name",
                    "NameType": "Personal",
                    "Affiliation": "Test affiliation",
                    "ContributorType": "Invalid",
                    "ORCID": "0000-0002-1825-0097",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_related_item_identifier(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "RelatedItem": [
                {
                    "RelatedItemIdentifier": "Invalid",
                    "RelatedItemIdentifierType": "DOI",
                    "RelatedItemType": "Collection",
                    "RelationType": "IsPartOf",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_related_item_identifier_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "RelatedItem": [
                {
                    "RelatedItemIdentifier": "10.5281/zenodo.1234567",
                    "RelatedItemIdentifierType": "Invalid",
                    "RelatedItemType": "Collection",
                    "RelationType": "IsPartOf",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_related_item_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "RelatedItem": [
                {
                    "RelatedItemIdentifier": "10.5281/zenodo.1234567",
                    "RelatedItemIdentifierType": "DOI",
                    "RelatedItemType": "Invalid",
                    "RelationType": "IsPartOf",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_relation_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "RelatedItem": [
                {
                    "RelatedIdentifier": "10.5281/zenodo.1234567",
                    "RelatedIdentifierType": "DOI",
                    "RelatedItemType": "Collection",
                    "RelationType": "Invalid",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_funding_reference_identifier_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "FundingReference": [
                {
                    "FunderName": "Test funder name",
                    "FunderIdentifier": "10.13039/501100000780",
                    "FunderIdentifierType": "Invalid",
                }
            ],
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_date(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Date": "Invalid",
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_access_type(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "AccessType": 1,
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_rights_uri(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Rights": {
                "RightsURI": "Invalid",
            },
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_rights_identifier_scheme(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Rights": {
                "RightsIdentifier": "https://creativecommons.org/licenses/by/4.0/",
                "RightsIdentifierScheme": "Invalid",
            },
        }

        output = validate_dataset_description(data)

        assert output is False

    def test_fail_invalid_rights_scheme_uri(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
            "Rights": {
                "RightsIdentifier": "https://creativecommons.org/licenses/by/4.0/",
                "RightsIdentifierScheme": "URI",
                "RightsSchemeURI": "Invalid",
            },
        }

        output = validate_dataset_description(data)

        assert output is False


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
