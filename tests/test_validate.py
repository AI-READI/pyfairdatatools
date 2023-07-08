"""Unit tests for pyfairdatatools.validate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501
from copy import deepcopy

from pyfairdatatools.validate import (
    validate_dataset_description,
    validate_license,
    validate_participants,
    validate_readme,
    validate_study_description,
)


class TestValidateDatasetDescription:
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

    def test_minimal_valid_dataset_description(self):
        data = deepcopy(self.minimal_valid_data)

        output = validate_dataset_description(data)

        assert output is True

    def test_identifier(self):
        data = deepcopy(self.minimal_valid_data)

        data["Identifier"] = {
            "identifierValue": "",
        }

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Identifier"] = {
            "identifierValue": "invalid",
        }

        output = validate_dataset_description(data)
        assert output is False

    def test_title(self):
        data = deepcopy(self.minimal_valid_data)

        data["Title"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Title"] = [{"titleValue": "Test", "titleType": ""}]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Title"] = [
            {"titleValue": "Test"},
            {"titleValue": "Test", "titleType": "Invalid"},
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_version(self):
        data = deepcopy(self.minimal_valid_data)

        data["Version"] = ""

        output = validate_dataset_description(data)
        assert output is False

    def test_alternate_identifier(self):
        data = deepcopy(self.minimal_valid_data)

        data["AlternateIdentifier"] = [
            {"alternateIdentifierValue": "", "alternateIdentifierType": "DOI"}
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["AlternateIdentifier"] = [
            {
                "alternateIdentifierValue": "10.5281/zenodo.7942786",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["AlternateIdentifier"] = [
            {
                "alternateIdentifierValue": "10.5281/zenodo.7942786",
                "alternateIdentifierType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_creator(self):
        data = deepcopy(self.minimal_valid_data)

        data["Creator"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
                "affiliation": {
                    "affiliationIdentifier": "Org1",
                    "affiliationIdentifierScheme": "",
                },
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
                "affiliation": {
                    "affiliationIdentifier": "Org1",
                    "affiliationIdentifierScheme": "ROR",
                    "SchemeURI": "",
                },
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_contributor(self):
        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "invalid",
                "contributorName": "Doe, John",
                "nameType": "Personal",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "nameIdentifier": [],
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "nameIdentifier": [
                    {
                        "nameIdentifierValue": "123456789",
                    }
                ],
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "nameIdentifier": [
                    {
                        "nameIdentifierValue": "123456789",
                        "nameIdentifierScheme": "ROR",
                        "schemeURI": "",
                    }
                ],
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "affiliation": {
                    "affiliationIdentifier": "Org1",
                    "affiliationIdentifierScheme": "",
                },
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "affiliation": {
                    "affiliationIdentifier": "Org1",
                    "affiliationIdentifierScheme": "ROR",
                    "SchemeURI": "",
                },
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_publication_year(self):
        data = deepcopy(self.minimal_valid_data)

        data["PublicationYear"] = "98"

        output = validate_dataset_description(data)
        assert output is False

    def test_date(self):
        data = deepcopy(self.minimal_valid_data)

        data["Date"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Date"] = [
            {"dateValue": "2004-03-02", "dateType": "invalid", "dateInformation": ""}
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_language(self):
        data = deepcopy(self.minimal_valid_data)

        data["Language"] = "en-US"

        output = validate_dataset_description(data)
        assert output is True

        data = deepcopy(self.minimal_valid_data)

        data["Language"] = ""

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.minimal_valid_data)

        data["Language"] = ["invalid"]

        output = validate_dataset_description(data)
        assert output is False


class TestValidateStudyDescription:
    minimal_valid_data = {
        "IdentificationModule": {
            "OrgStudyIdInfo": {
                "OrgStudyId": "RandomStudyId",
                "OrgStudyIdType": "NIH Grant Number",
            }
        },
        "StatusModule": {
            "OverallStatus": "Recruiting",
            "StartDateStruct": {
                "StartDate": "July 07, 2023",
                "StartDateType": "Actual",
            },
        },
        "DesignModule": {
            "StudyType": "Observational",
            "DesignInfo": {
                "DesignObservationalModelList": ["Cohort"],
                "DesignTimePerspectiveList": ["Prospective"],
            },
            "EnrollmentInfo": {
                "EnrollmentCount": "34",
                "EnrollmentType": "Anticipated",
            },
            "TargetDuration": "4 Years",
            "NumberGroupsCohorts": "1",
        },
        "SponsorCollaboratorsModule": {
            "ResponsibleParty": {"ResponsiblePartyType": "Sponsor"},
            "LeadSponsor": {"LeadSponsorName": "Harper Spiller"},
        },
        "DescriptionModule": {
            "BriefSummary": "This is a brief summary",
        },
        "ConditionsModule": {"ConditionList": ["Condition 1", "Condition 2"]},
        "EligibilityModule": {
            "Gender": "All",
            "GenderBased": "No",
            "MinimumAge": "18 Years",
            "MaximumAge": "65 Years",
            "EligibilityCriteria": "This is the eligibility criteria",
            "StudyPopulation": "This is the study population",
            "SamplingMethod": "Non-Probability Sample",
        },
        "ContactsLocationsModule": {
            "CentralContactList": [
                {
                    "CentralContactName": "Ethan Spiller",
                    "CentralContactAffiliation": "White Lotus",
                    "CentralContactPhone": "805-555-5555",
                    "CentralContactEMail": "e.spiller@hbo.com",
                }
            ],
            "OverallOfficialList": [
                {
                    "OverallOfficialName": "Daphne Sullivan",
                    "OverallOfficialAffiliation": "White Lotus",
                    "OverallOfficialRole": "Study Principal Investigator",
                }
            ],
            "LocationList": [
                {
                    "LocationFacility": "White Lotus",
                    "LocationStatus": "Recruiting",
                    "LocationCity": "Taormina",
                    "LocationCountry": "Italy",
                }
            ],
        },
    }

    def test_minimal_valid_study_description(self):
        data = deepcopy(self.minimal_valid_data)

        output = validate_study_description(data)

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
