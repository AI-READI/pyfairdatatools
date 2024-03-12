"""Unit tests for pyfairdatatools.validate module."""

# pylint: disable=too-many-lines
from copy import deepcopy
from typing import Any, Dict

from pyfairdatatools.validate import (
    validate_dataset_description,
    validate_datatype_dictionary,
    validate_license,
    validate_participants,
    validate_readme,
    validate_study_description,
)


class TestValidateDatasetDescription:
    """Unit tests for validate_dataset_description function."""

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
            "rorId": "https://ror.org/123456789",
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
        "format": ["application/pdf", "text/csv", "dicom", "nifti"],
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

    def test_valid_dataset_description(self):
        """Test valid dataset description."""
        data = deepcopy(self.valid_data)

        try:
            output = validate_dataset_description(data)
        except Exception as e:  # pylint: disable=broad-except
            print(e)
            output = False

        assert output

    def test_identifier(self):
        """Test identifier validation."""
        data = deepcopy(self.valid_data)

        data["identifier"] = {
            "identifierValue": "",
        }

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["identifier"] = {
            "identifierValue": "invalid",
        }

        output = validate_dataset_description(data)
        assert output is False

    def test_title(self):
        """Test title validation."""
        data = deepcopy(self.valid_data)

        data["title"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["title"] = [{"titleValue": "Test", "titleType": ""}]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["title"] = [
            {"titleValue": "Test"},
            {"titleValue": "Test", "titleType": "Invalid"},
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_version(self):
        """Test version validation."""
        data = deepcopy(self.valid_data)

        data["version"] = ""

        output = validate_dataset_description(data)
        assert output is False

    def test_alternate_identifier(self):
        """Test alternate identifier validation."""
        data = deepcopy(self.valid_data)

        data["alternateIdentifier"] = [
            {"alternateIdentifierValue": "", "alternateIdentifierType": "DOI"}
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["alternateIdentifier"] = [
            {
                "alternateIdentifierValue": "10.5281/zenodo.7942786",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["alternateIdentifier"] = [
            {
                "alternateIdentifierValue": "10.5281/zenodo.7942786",
                "alternateIdentifierType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_creator(self):
        """Test creator validation."""
        data = deepcopy(self.valid_data)

        data["creator"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["creator"] = [
            {
                "creatorName": "Doe, John",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
                "affiliation": {},
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["creator"] = [
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

        data = deepcopy(self.valid_data)

        data["creator"] = [
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
        """Test contributor validation."""
        data = deepcopy(self.valid_data)

        data["contributor"] = [
            {
                "contributorType": "invalid",
                "contributorName": "Doe, John",
                "nameType": "Personal",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "nameIdentifier": [],
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["contributor"] = [
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

        data = deepcopy(self.valid_data)

        data["contributor"] = [
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

        data = deepcopy(self.valid_data)

        data["contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Personal",
                "affiliation": {},
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["contributor"] = [
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

        data = deepcopy(self.valid_data)

        data["contributor"] = [
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

    def test_related_identifier(self):
        """Test related identifier validation."""
        data = deepcopy(self.valid_data)

        data["relatedIdentifier"] = [
            {
                "relatedIdentifierValue": "",
                "relatedIdentifierType": "DOI",
                "relationType": "HasMetadata",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["relatedIdentifier"] = [
            {
                "relatedIdentifierValue": "10.5281/zenodo.7942786",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["relatedIdentifier"] = [
            {
                "relatedIdentifierValue": "10.5281/zenodo.7942786",
                "relatedIdentifierType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_publication_year(self):
        """Test publication year validation."""
        data = deepcopy(self.valid_data)

        data["publicationYear"] = "98"

        output = validate_dataset_description(data)
        assert output is False

    def test_date(self):
        """Test date validation."""
        data = deepcopy(self.valid_data)

        data["date"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["date"] = [
            {"dateValue": "2004-03-02", "dateType": "invalid", "dateInformation": ""}
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_language(self):
        """Test language validation."""
        data = deepcopy(self.valid_data)

        data["language"] = "en-US"

        output = validate_dataset_description(data)
        assert output is True

        data = deepcopy(self.valid_data)

        data["language"] = ""

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["language"] = ["invalid"]

        output = validate_dataset_description(data)
        assert output is False


class TestValidateStudyDescription:
    """Unit tests for validate_study_description function."""

    observational_study_valid_data: Dict[str, Any] = {
        "identificationModule": {
            "officialTitle": "Test Title",
            "acronym": "TT",
            "orgStudyIdInfo": {
                "orgStudyId": "RandomStudyId",
                "orgStudyIdType": "Registry Identifier",
                "orgStudyIdDomain": "ClinicalTrials.gov",
                "orgStudyIdLink": "https://clinicaltrials.gov/ct2/show/NCT00000000",
            },
            "secondaryIdInfoList": [
                {
                    "secondaryId": "SomeID",
                    "secondaryIdType": "Other Identifier",
                    "secondaryIdDomain": "Other",
                    "secondaryIdLink": "https://example.com",
                }
            ],
        },
        "statusModule": {
            "overallStatus": "Suspended",
            "whyStopped": "Study stopped due to lack of funding",
            "startDateStruct": {
                "startDate": "2023-06",
                "startDateType": "Actual",
            },
            "completionDateStruct": {
                "completionDate": "2024-06",
                "completionDateType": "Actual",
            },
        },
        "sponsorCollaboratorsModule": {
            "responsibleParty": {
                "responsiblePartyType": "Principal Investigator",
                "responsiblePartyInvestigatorFirstName": "Harper",
                "responsiblePartyInvestigatorLastName": "Spiller",
                "responsiblePartyInvestigatorTitle": "Principal Investigator",
                "responsiblePartyInvestigatorAffiliation": {
                    "responsiblePartyInvestigatorAffiliationName": "White Lotus",
                },
            },
            "leadSponsor": {"leadSponsorName": "Harper Spiller"},
            "collaboratorList": [
                {"collaboratorName": "Nicole Mossbacher"},
                {"collaboratorName": "Olivia Mossbacher"},
            ],
        },
        "oversightModule": {
            "isFDARegulatedDrug": "No",
            "isFDARegulatedDevice": "No",
            "humanSubjectReviewStatus": "Request not yet submitted",
            "oversightHasDMC": "No",
        },
        "descriptionModule": {
            "briefSummary": "This is a brief summary",
            "detailedDescription": "This is a detailed description",
        },
        "conditionsModule": {
            "conditionList": [
                {"conditionName": "Condition 1"},
                {"conditionName": "Condition 2"},
            ],
            "keywordList": [
                {"keywordValue": "Keyword 1"},
                {"keywordValue": "Keyword 2"},
            ],
        },
        "designModule": {
            "studyType": "Observational",
            "designInfo": {
                "designObservationalModelList": ["Cohort"],
                "designTimePerspectiveList": ["Prospective"],
            },
            "bioSpec": {
                "bioSpecRetention": "Samples With DNA",
                "bioSpecDescription": "This is a description of the biospecs",
            },
            "enrollmentInfo": {
                "enrollmentCount": "34",
                "enrollmentType": "Anticipated",
            },
            "targetDuration": "4 Years",
            "numberGroupsCohorts": "1",
            "isPatientRegistry": "Yes",
        },
        "armsInterventionsModule": {
            "armGroupList": [
                {"armGroupLabel": "Arm 1", "armGroupDescription": "Experimental"}
            ],
            "interventionList": [
                {
                    "interventionType": "Drug",
                    "interventionName": "Drug 1",
                    "interventionDescription": "description of the intervention",
                    "interventionOtherNameList": ["Other Name 1"],
                },
            ],
        },
        "eligibilityModule": {
            "sex": "All",
            "genderBased": "No",
            "minimumAge": "18 Years",
            "maximumAge": "65 Years",
            "eligibilityCriteria": {
                "eligibilityCriteriaInclusion": ["crietia 1", "crietia 2"],
                "eligibilityCriteriaExclusion": ["crietia 1", "crietia 2"],
            },
            "studyPopulation": "This is the study population",
            "healthyVolunteers": "No",
            "samplingMethod": "Non-Probability Sample",
        },
        "contactsLocationsModule": {
            "centralContactList": [
                {
                    "centralContactFirstName": "Ethan",
                    "centralContactLastName": "Spiller",
                    "centralContactAffiliation": {
                        "centralContactAffiliationName": "White Lotus",
                    },
                    "centralContactPhone": "805-555-5555",
                    "centralContactPhoneExt": "123",
                    "centralContactEMail": "e.spiller@hbo.com",
                }
            ],
            "overallOfficialList": [
                {
                    "overallOfficialFirstName": "Daphne",
                    "overallOfficialLastName": "Sullivan",
                    "overallOfficialAffiliation": {
                        "overallOfficialAffiliationName": "White Lotus",
                    },
                    "overallOfficialRole": "Study Principal Investigator",
                }
            ],
            "locationList": [
                {
                    "locationFacility": "White Lotus",
                    "locationStatus": "Recruiting",
                    "locationCity": "Kihei",
                    "locationState": "Hawaii",
                    "locationZip": "96753",
                    "locationCountry": "United States",
                }
            ],
        },
    }

    interventional_study_valid_data: Dict[str, Any] = {
        "identificationModule": {
            "officialTitle": "Test Title",
            "acronym": "TT",
            "orgStudyIdInfo": {
                "orgStudyId": "RandomStudyId",
                "orgStudyIdType": "Registry Identifier",
                "orgStudyIdDomain": "ClinicalTrials.gov",
                "orgStudyIdLink": "https://clinicaltrials.gov/ct2/show/NCT00000000",
            },
            "secondaryIdInfoList": [
                {
                    "secondaryId": "SomeID",
                    "secondaryIdType": "Other Identifier",
                    "secondaryIdDomain": "Other",
                    "secondaryIdLink": "https://example.com",
                }
            ],
        },
        "statusModule": {
            "overallStatus": "Suspended",
            "whyStopped": "Study stopped due to lack of funding",
            "startDateStruct": {
                "startDate": "2023-06",
                "startDateType": "Actual",
            },
            "completionDateStruct": {
                "completionDate": "2024-06",
                "completionDateType": "Actual",
            },
        },
        "sponsorCollaboratorsModule": {
            "responsibleParty": {
                "responsiblePartyType": "Principal Investigator",
                "responsiblePartyInvestigatorFirstName": "Harper",
                "responsiblePartyInvestigatorLastName": "Spiller",
                "responsiblePartyInvestigatorTitle": "Principal Investigator",
                "responsiblePartyInvestigatorAffiliation": {
                    "responsiblePartyInvestigatorAffiliationName": "White Lotus",
                },
            },
            "leadSponsor": {"leadSponsorName": "Harper Spiller"},
            "collaboratorList": [
                {"collaboratorName": "Nicole Mossbacher"},
                {"collaboratorName": "Olivia Mossbacher"},
            ],
        },
        "oversightModule": {
            "isFDARegulatedDrug": "No",
            "isFDARegulatedDevice": "No",
            "humanSubjectReviewStatus": "Request not yet submitted",
            "oversightHasDMC": "No",
        },
        "descriptionModule": {
            "briefSummary": "This is a brief summary",
            "detailedDescription": "This is a detailed description",
        },
        "conditionsModule": {
            "conditionList": [
                {"conditionName": "Condition 1"},
                {"conditionName": "Condition 2"},
            ],
            "keywordList": [
                {"keywordValue": "Keyword 1"},
                {"keywordValue": "Keyword 2"},
            ],
        },
        "designModule": {
            "studyType": "Interventional",
            "designInfo": {
                "designAllocation": "Randomized",
                "designInterventionModel": "Prevention",
                "designInterventionModelDescription": "description",
                "designPrimaryPurpose": "Parallel Assignment",
                "designMaskingInfo": {
                    "designMasking": "Blinded (no details)",
                    "designMaskingDescription": "description of the design masking",
                    "designWhoMaskedList": ["Participant", "Care Provider"],
                },
            },
            "phaseList": ["Phase 1/2"],
            "enrollmentInfo": {
                "enrollmentCount": "34",
                "enrollmentType": "Anticipated",
            },
            "numberArms": "1",
        },
        "armsInterventionsModule": {
            "armGroupList": [
                {
                    "armGroupLabel": "Arm 1",
                    "armGroupType": "Placebo Comparator",
                    "armGroupDescription": "Experimental",
                    "armGroupInterventionList": ["Drug 1"],
                }
            ],
            "interventionList": [
                {
                    "interventionType": "Drug",
                    "interventionName": "Drug 1",
                    "interventionDescription": "description of the intervention",
                    "interventionOtherNameList": ["Other Name 1"],
                },
            ],
        },
        "eligibilityModule": {
            "sex": "All",
            "genderBased": "No",
            "minimumAge": "18 Years",
            "maximumAge": "65 Years",
            "healthyVolunteers": "No",
            "eligibilityCriteria": {
                "eligibilityCriteriaInclusion": ["crietia 1", "crietia 2"],
                "eligibilityCriteriaExclusion": ["crietia 1", "crietia 2"],
            },
        },
        "contactsLocationsModule": {
            "centralContactList": [
                {
                    "centralContactFirstName": "Ethan",
                    "centralContactLastName": "Spiller",
                    "centralContactAffiliation": {
                        "centralContactAffiliationName": "White Lotus",
                    },
                    "centralContactPhone": "805-555-5555",
                    "centralContactPhoneExt": "123",
                    "centralContactEMail": "e.spiller@hbo.com",
                }
            ],
            "overallOfficialList": [
                {
                    "overallOfficialFirstName": "Daphne",
                    "overallOfficialLastName": "Sullivan",
                    "overallOfficialAffiliation": {
                        "overallOfficialAffiliationName": "White Lotus",
                    },
                    "overallOfficialRole": "Study Principal Investigator",
                }
            ],
            "locationList": [
                {
                    "locationFacility": "White Lotus",
                    "locationStatus": "Recruiting",
                    "locationCity": "Kihei",
                    "locationState": "Hawaii",
                    "locationZip": "96753",
                    "locationCountry": "United States",
                }
            ],
        },
    }

    def test_observational_valid_study_description(self):
        """Test valid observational study description."""
        data = deepcopy(self.observational_study_valid_data)

        output = validate_study_description(data)

        assert output is True

    def test_interventional_valid_study_description(self):
        """Test valid interventional study description."""
        data = deepcopy(self.interventional_study_valid_data)

        output = validate_study_description(data)

        assert output is True

    def test_invalid_identification_module(self):
        """Test invalid identification module."""
        data = deepcopy(self.observational_study_valid_data)

        data["identificationModule"]["orgStudyIdInfo"][
            "orgStudyIdType"
        ] = "Registry Identifier"

        del data["identificationModule"]["orgStudyIdInfo"]["orgStudyIdDomain"]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        # sourcery skip: no-loop-in-tests
        for item in data["identificationModule"]["secondaryIdInfoList"]:
            item["secondaryIdType"] = "Other Identifier"
            del item["secondaryIdDomain"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_status_module(self):
        """Test invalid status module."""
        data = deepcopy(self.observational_study_valid_data)

        data["statusModule"]["overallStatus"] = "Terminated"

        del data["statusModule"]["whyStopped"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_sponsor_collaborators_module(self):
        """Test invalid sponsor collaborators module."""
        data = deepcopy(self.observational_study_valid_data)

        data["sponsorCollaboratorsModule"]["responsibleParty"][
            "responsiblePartyType"
        ] = "Sponsor-Investigator"

        del data["sponsorCollaboratorsModule"]["responsibleParty"][
            "responsiblePartyInvestigatorFirstName"
        ]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        data["sponsorCollaboratorsModule"]["responsibleParty"][
            "responsiblePartyType"
        ] = "Sponsor-Investigator"

        del data["sponsorCollaboratorsModule"]["responsibleParty"][
            "responsiblePartyInvestigatorTitle"
        ]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        data["sponsorCollaboratorsModule"]["responsibleParty"][
            "responsiblePartyType"
        ] = "Sponsor-Investigator"

        del data["sponsorCollaboratorsModule"]["responsibleParty"][
            "responsiblePartyInvestigatorAffiliation"
        ]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_arms_interventions_module(self):
        """Test invalid arms interventions module."""
        data = deepcopy(self.interventional_study_valid_data)

        for item in data["armsInterventionsModule"]["armGroupList"]:
            del item["armGroupType"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_eligibilty_module(self):
        """Test invalid eligibility module."""
        data = deepcopy(self.interventional_study_valid_data)

        del data["eligibilityModule"]["healthyVolunteers"]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        del data["eligibilityModule"]["samplingMethod"]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        del data["eligibilityModule"]["studyPopulation"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_contacts_locations_module(self):
        """Test invalid contacts locations module."""
        data = deepcopy(self.observational_study_valid_data)

        del data["contactsLocationsModule"]["centralContactList"]

        output = validate_study_description(data)

        # should fail because LocationContactList is
        # required if CentralContactList is not present
        assert output is False


class TestValidateReadme:
    """Unit tests for validate_readme function."""

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
    """Unit tests for validate_license function."""

    def test_valid_license(self):
        """Test valid license."""
        data = "CC-BY-4.0"

        output = validate_license(data)

        assert output is True

    def test_fail_invalid_license(self):
        """Test invalid license."""
        data = {
            "License": "Invalid",
        }

        output = validate_license(data)

        assert output is False


class TestValidateParticipants:
    """Unit tests for validate_participants function."""

    def test_minimal_valid_participant(self):
        """Test minimal valid participant."""
        data = [
            {
                "participant_id": "sub-user1",
            }
        ]

        output = validate_participants(data)

        assert output is True

    def test_valid_participant_with_all_fields(self):
        """Test valid participant with all fields."""
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


class TestValidateDatatypeDescription:
    def test_invalid_datatype_description(self):
        data = ["ekg", "redcap_data", "oct", "invalid"]

        output = validate_datatype_dictionary(data)

        assert output is False

    def test_valid_datatype_description(self):
        data = ["ekg", "redcap_data", "oct"]

        output = validate_datatype_dictionary(data)

        assert output is True
