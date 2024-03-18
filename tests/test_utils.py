"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

# import os

import pytest
from copy import deepcopy
from typing import Any, Dict

from pyfairdatatools.utils import feet_to_meters, requestJSON, validate_file_path, convert_for_datacite


class TestDescribeFeetToMeters:
    def test_when_integer(self):
        converted = feet_to_meters(42)
        assert converted == 12.80165

    def test_when_string(self):
        with pytest.raises(ValueError):
            feet_to_meters("hello")


class TestRequestJSON:
    def test_when_valid_url(self):
        response = requestJSON("https://dummyjson.com/test")
        assert response["status"] == "ok"

    def test_when_invalid_url(self):
        with pytest.raises(Exception):
            requestJSON("https://dummyjson.com/invalid")


class TestValidateFilePath:
    def test_when_valid_path(self):
        assert validate_file_path("pyfairdatatools/README.md") == True

    def test_when_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            validate_file_path("pyfairdatatools/invalid.md", preexisting_file=True)

    # def test_when_invalid_writable(self):
    #     with pytest.raises(PermissionError):
    #         root_file_path = os.path.join(os.path.abspath(os.sep), "README.md")
    #         print(root_file_path)
    #         validate_file_path(root_file_path, writable=True)


class TestConvertToDatacite:
    """Test the convert_to_datacite function."""
    valid_data: Dict[str, Any] = {
        "identifier": {
            "identifierValue": "10.5281/zenodo.1234567",
            "identifierType": "DOI",
        },
        "title": [
            {
                "titleValue": "Main Title",
            },
            {
                "titleValue": "Subtitle",
                "titleType": "Subtitle",
            },
        ],
        "version": "1.0.0",
        "alternateIdentifier": [
            {
                "alternateIdentifierValue": "10.5281/zenodo.1234567",
                "alternateIdentifierType": "DOI",
            }
        ],
        "creator": [
            {
                "creatorName": "Doe, John",
                "nameType": "Personal",
                "nameIdentifier": [
                    {
                        "nameIdentifierValue": "0000-0001-2345-6789",
                        "nameIdentifierScheme": "ORCID",
                        "schemeURI": "https://orcid.org",
                    }
                ],
                "affiliation": [
                    {
                        "affiliationName": "White Lotus",
                        "affiliationIdentifier": {
                            "affiliationIdentifierValue": "https://ror.org/123456789",
                            "affiliationIdentifierScheme": "ROR",
                            "schemeURI": "https://ror.org",
                        },
                    }
                ],
            },
            {
                "creatorName": "White Lotus Research",
                "nameType": "Organizational",
                "nameIdentifier": [
                    {
                        "nameIdentifierValue": "0000-0001-2345-6789",
                        "nameIdentifierScheme": "ROR",
                        "schemeURI": "https://ror.org",
                    }
                ],
            },
        ],
        "contributor": [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "nameIdentifier": [
                    {
                        "nameIdentifierValue": "0000-0001-2345-6789",
                        "nameIdentifierScheme": "ORCID",
                        "schemeURI": "https://orcid.org",
                    }
                ],
                "affiliation": [
                    {
                        "affiliationName": "White Lotus",
                        "affiliationIdentifier": {
                            "affiliationIdentifierValue": "https://ror.org/123456789",
                            "affiliationIdentifierScheme": "ROR",
                            "schemeURI": "https://ror.org",
                        },
                    }
                ],
            },
            {
                "contributorType": "HostingInstitution",
                "contributorName": "White Lotus Research",
                "nameType": "Organizational",
                "nameIdentifier": [
                    {
                        "nameIdentifierValue": "0000-0001-2345-6789",
                        "nameIdentifierScheme": "ROR",
                        "schemeURI": "https://ror.org",
                    }
                ],
            },
        ],
        "publicationYear": "2023",
        "date": [
            {
                "dateValue": "2023-01-01",
                "dateType": "Collected",
                "dateInformation": "Some information",
            }
        ],
        "resourceType": {
            "resourceTypeValue": "Diabetes",
            "resourceTypeGeneral": "Dataset",
        },
        "datasetDeIdentLevel": {
            "deIdentType": "NoDeIdentification",
            "deIdentDirect": True,
            "deIdentHIPAA": True,
            "deIdentDates": True,
            "deIdentNonarr": True,
            "deIdentKAnon": True,
            "deIdentDetails": "Some details",
        },
        "datasetConsent": {
            "consentType": "NoRestriction",
            "consentNoncommercial": True,
            "consentGeogRestrict": True,
            "consentResearchType": True,
            "consentGeneticOnly": True,
            "consentNoMethods": True,
            "consentsDetails": "Some details",
        },
        "description": [
            {"descriptionValue": "Some description", "descriptionType": "Abstract"},
            {"descriptionValue": "Some description", "descriptionType": "Methods"},
        ],
        "language": "en",
        "relatedIdentifier": [
            {
                "relatedIdentifierValue": "10.5281/zenodo.1234567",
                "relatedIdentifierType": "DOI",
                "relationType": "IsCitedBy",
                "relatedMetadataScheme": "DataCite",
                "schemeURI": "https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf",  # noqa: E501 pylint: disable=line-too-long
                "schemeType": "DOI",
                "resourceTypeGeneral": "Dataset",
            }
        ],
        "subject": [
            {
                "subjectValue": "Diabetes",
                "subjectIdentifier": {
                    "classificationCode": "E11.9",
                    "subjectScheme": "MeSH",
                    "schemeURI": "https://www.nlm.nih.gov/mesh/",
                    "valueURI": "https://www.nlm.nih.gov/mesh/1234567",
                },
            }
        ],
        "managingOrganization": {
            "name": "Test Organization",
            "managingOrganizationIdentifier": {
                "managingOrganizationIdentifierValue": "04z8jg394",
                "managingOrganizationScheme": "ROR",
                "schemeURI": "https://www.crossref.org/",
            },
        },
        "accessType": "PublicOnScreenAccess",
        "accessDetails": {
            "description": "Some description",
            "url": "https://example.com",
            "urlLastChecked": "2021-01-01",
        },
        "rights": [
            {
                "rightsName": "CC0-1.0",
                "rightsURI": "https://creativecommons.org/publicdomain/zero/1.0/",
                "rightsIdentifier": {
                    "rightsIdentifierValue": "CC0-1.0",
                    "rightsIdentifierScheme": "SPDX",
                    "schemeURI": "https://spdx.org/licenses/",
                },
            }
        ],
        "publisher": {
            "publisherName": "Test Publisher",
            "publisherIdentifier": {
                "publisherIdentifierValue": "04z8jg394",
                "publisherIdentifierScheme": "ROR",
                "schemeURI": "https://www.crossref.org/",
            },
        },
        "size": ["15 pages", "15 MB"],
        "format": ["application/pdf", "text/xml", "MOPG", "nifti"],
        "fundingReference": [
            {
                "funderName": "Test Funder",
                "funderIdentifier": {
                    "funderIdentifierValue": "1234567",
                    "funderIdentifierType": "Crossref Funder ID",
                    "schemeURI": "https://doi.org/10.13039/501100001711",
                },
                "awardNumber": {
                    "awardNumberValue": "1234567",
                    "awardURI": "https://doi.org/10.13039/501100001711",
                },
                "awardTitle": "Test Award",
            }
        ],
    }

    def test_when_valid_data(self):
        data = deepcopy(self.valid_data)
        
        output = convert_for_datacite(data)

        assert output is not None