"""Unit tests for pyfairdatatools.validate module."""
# pylint: disable=too-many-lines
from copy import deepcopy
from typing import Any, Dict

from pyfairdatatools.validate import (
    validate_dataset_description,
    validate_license,
    validate_participants,
    validate_readme,
    validate_study_description,
)


class TestValidateDatasetDescription:
    valid_data: Dict[str, Any] = {
        "Identifier": {
            "identifierValue": "10.5281/zenodo.1234567",
            "identifierType": "DOI",
        },
        "Title": [
            {
                "titleValue": "Main Title",
            },
            {
                "titleValue": "Subtitle",
                "titleType": "Subtitle",
            },
        ],
        "Version": "1.0.0",
        "AlternateIdentifier": [
            {
                "alternateIdentifierValue": "10.5281/zenodo.1234567",
                "alternateIdentifierType": "DOI",
            }
        ],
        "Creator": [
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
                        "affiliationValue": "White Lotus",
                        "affiliationIdentifier": "https://ror.org/123456789",
                        "affiliationIdentifierScheme": "ROR",
                        "schemeURI": "https://ror.org",
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
        "Contributor": [
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
                        "affiliationValue": "White Lotus",
                        "affiliationIdentifier": "https://ror.org/123456789",
                        "affiliationIdentifierScheme": "ROR",
                        "schemeURI": "https://ror.org",
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
        "PublicationYear": "2023",
        "Date": [
            {
                "dateValue": "2023-01-01",
                "dateType": "Collected",
                "dateInformation": "Some information",
            }
        ],
        "ResourceType": {
            "resourceTypeValue": "Diabetes",
            "resourceTypeGeneral": "Dataset",
        },
        "DatasetRecordKeys": {"keysType": "Anonymised", "keysDetails": "Some details"},
        "DatasetDeIdentLevel": {
            "deIdentType": "NoDeIdentification",
            "deIdentDirect": True,
            "deIdentHIPAA": True,
            "deIdentDates": True,
            "deIdentNonarr": True,
            "deIdentKAnon": True,
            "deIdentDetails": "Some details",
        },
        "DatasetConsent": {
            "consentType": "NoRestriction",
            "consentNoncommercial": True,
            "consentGeogRestrict": True,
            "consentResearchType": True,
            "consentGeneticOnly": True,
            "consentNoMethods": True,
            "consentsDetails": "Some details",
        },
        "Description": [
            {"descriptionValue": "Some description", "descriptionType": "Abstract"},
            {"descriptionValue": "Some description", "descriptionType": "Methods"},
        ],
        "Language": "en",
        "RelatedIdentifier": [
            {
                "relatedIdentifierValue": "10.5281/zenodo.1234567",
                "relatedIdentifierType": "DOI",
                "relationType": "HasMetadata",
                "relatedMetadataScheme": "DataCite",
                "schemeURI": "https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf",
                "schemeType": "DOI",
                "resourceTypeGeneral": "Dataset",
            }
        ],
        "Subject": [
            {
                "subjectValue": "Diabetes",
                "subjectScheme": "MeSH",
                "schemeURI": "https://www.nlm.nih.gov/mesh/",
                "valueURI": "https://www.nlm.nih.gov/mesh/1234567",
                "classificationCode": "E11.9",
            }
        ],
        "ManagingOrganisation": {
            "name": "Test Organisation",
            "rorId": "https://ror.org/123456789",
        },
        "AccessType": "PublicOnScreenAccess",
        "AccessDetails": {
            "description": "Some description",
            "url": "https://example.com",
            "urlLastChecked": "2021-01-01",
        },
        "Rights": [
            {
                "rightsValue": "CC0-1.0",
                "rightsURI": "https://creativecommons.org/publicdomain/zero/1.0/",
                "rightsIdentifier": "CC0-1.0",
                "rightsIdentifierScheme": "SPDX",
            }
        ],
        "Publisher": "GitHub",
        "Size": ["15 pages", "15 MB"],
        "FundingReference": [
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
        "RelatedItem": [
            {
                "relatedItemType": "Book",
                "relationType": "IsMetadataFor",
                "relatedItemIdentifier": [
                    {
                        "relatedItemIdentifierValue": "10.5281/zenodo.1234567",
                        "relatedItemIdentifierType": "DOI",
                        "relatedMetadataScheme": "DataCite",
                        "schemeURI": "https://schema.datacite.org/meta/kernel-4.3/doc/DataCite-MetadataKernel_v4.3.pdf",
                        "schemeType": "DDT",
                    }
                ],
                "creator": [
                    {
                        "creatorName": "Doe, John",
                        "nameType": "Personal",
                    }
                ],
                "title": [
                    {
                        "titleValue": "Test title",
                    }
                ],
                "publicationYear": "2021",
                "volume": "1",
                "issue": "1",
                "number": {"numberValue": "1", "numberType": "Article"},
                "firstPage": "1",
                "lastPage": "15",
                "publisher": "Test Publisher",
                "edition": "1",
                "contributor": [
                    {
                        "contributorType": "Editor",
                        "contributorName": "Doe, John",
                        "nameType": "Personal",
                    }
                ],
            }
        ],
    }

    def test_valid_dataset_description(self):
        data = deepcopy(self.valid_data)

        try:
            output = validate_dataset_description(data)
        except Exception as e:
            print(e)
            output = False

        assert output is True

    def test_identifier(self):
        data = deepcopy(self.valid_data)

        data["Identifier"] = {
            "identifierValue": "",
        }

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Identifier"] = {
            "identifierValue": "invalid",
        }

        output = validate_dataset_description(data)
        assert output is False

    def test_title(self):
        data = deepcopy(self.valid_data)

        data["Title"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Title"] = [{"titleValue": "Test", "titleType": ""}]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Title"] = [
            {"titleValue": "Test"},
            {"titleValue": "Test", "titleType": "Invalid"},
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_version(self):
        data = deepcopy(self.valid_data)

        data["Version"] = ""

        output = validate_dataset_description(data)
        assert output is False

    def test_alternate_identifier(self):
        data = deepcopy(self.valid_data)

        data["AlternateIdentifier"] = [
            {"alternateIdentifierValue": "", "alternateIdentifierType": "DOI"}
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["AlternateIdentifier"] = [
            {
                "alternateIdentifierValue": "10.5281/zenodo.7942786",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["AlternateIdentifier"] = [
            {
                "alternateIdentifierValue": "10.5281/zenodo.7942786",
                "alternateIdentifierType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_creator(self):
        data = deepcopy(self.valid_data)

        data["Creator"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Creator"] = [
            {
                "creatorName": "Doe, John",
                "nameType": "Invalid",
                "affiliation": {},
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

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

        data = deepcopy(self.valid_data)

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
        data = deepcopy(self.valid_data)

        data["Contributor"] = [
            {
                "contributorType": "invalid",
                "contributorName": "Doe, John",
                "nameType": "Personal",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Contributor"] = [
            {
                "contributorType": "ContactPerson",
                "contributorName": "Doe, John",
                "nameType": "Invalid",
            }
        ]

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

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

        data = deepcopy(self.valid_data)

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

        data = deepcopy(self.valid_data)

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

        data = deepcopy(self.valid_data)

        data["Contributor"] = [
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

        data = deepcopy(self.valid_data)

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
        data = deepcopy(self.valid_data)

        data["PublicationYear"] = "98"

        output = validate_dataset_description(data)
        assert output is False

    def test_date(self):
        data = deepcopy(self.valid_data)

        data["Date"] = []

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Date"] = [
            {"dateValue": "2004-03-02", "dateType": "invalid", "dateInformation": ""}
        ]

        output = validate_dataset_description(data)
        assert output is False

    def test_language(self):
        data = deepcopy(self.valid_data)

        data["Language"] = "en-US"

        output = validate_dataset_description(data)
        assert output is True

        data = deepcopy(self.valid_data)

        data["Language"] = ""

        output = validate_dataset_description(data)
        assert output is False

        data = deepcopy(self.valid_data)

        data["Language"] = ["invalid"]

        output = validate_dataset_description(data)
        assert output is False


class TestValidateStudyDescription:
    observational_study_valid_data: Dict[str, Any] = {
        "IdentificationModule": {
            "OrgStudyIdInfo": {
                "OrgStudyId": "RandomStudyId",
                "OrgStudyIdType": "Registry Identifier",
                "OrgStudyIdDomain": "ClinicalTrials.gov",
                "OrgStudyIdLink": "https://clinicaltrials.gov/ct2/show/NCT00000000",
            },
            "SecondaryIdInfoList": [
                {
                    "SecondaryId": "SomeID",
                    "SecondaryIdType": "Other Identifier",
                    "SecondaryIdDomain": "Other",
                    "SecondaryIdLink": "https://example.com",
                }
            ],
        },
        "StatusModule": {
            "OverallStatus": "Suspended",
            "WhyStopped": "Study stopped due to lack of funding",
            "StartDateStruct": {
                "StartDate": "July 07, 2023",
                "StartDateType": "Actual",
            },
            "CompletionDateStruct": {
                "CompletionDate": "July 08, 2024",
                "CompletionDateType": "Actual",
            },
        },
        "SponsorCollaboratorsModule": {
            "ResponsibleParty": {
                "ResponsiblePartyType": "Principal Investigator",
                "ResponsiblePartyInvestigatorFullName": "Harper Spiller",
                "ResponsiblePartyInvestigatorTitle": "Principal Investigator",
                "ResponsiblePartyInvestigatorAffiliation": "White Lotus",
            },
            "LeadSponsor": {"LeadSponsorName": "Harper Spiller"},
            "CollaboratorList": [
                {"CollaboratorName": "Nicole Mossbacher"},
                {"CollaboratorName": "Olivia Mossbacher"},
            ],
        },
        "OversightModule": {
            "OversightHasDMC": "No",
        },
        "DescriptionModule": {
            "BriefSummary": "This is a brief summary",
            "DetailedDescription": "This is a detailed description",
        },
        "ConditionsModule": {
            "ConditionList": ["Condition 1", "Condition 2"],
            "KeywordList": ["Keyword 1", "Keyword 2"],
        },
        "DesignModule": {
            "StudyType": "Observational",
            "DesignInfo": {
                "DesignObservationalModelList": ["Cohort"],
                "DesignTimePerspectiveList": ["Prospective"],
            },
            "BioSpec": {
                "BioSpecRetention": "Samples With DNA",
                "BioSpecDescription": "This is a description of the biospecs",
            },
            "EnrollmentInfo": {
                "EnrollmentCount": "34",
                "EnrollmentType": "Anticipated",
            },
            "TargetDuration": "4 Years",
            "NumberGroupsCohorts": "1",
        },
        "ArmsInterventionsModule": {
            "ArmGroupList": [
                {"ArmGroupLabel": "Arm 1", "ArmGroupDescription": "Experimental"}
            ],
            "InterventionList": [
                {
                    "InterventionType": "Drug",
                    "InterventionName": "Drug 1",
                    "InterventionDescription": "description of the intervention",
                    "InterventionArmGroupLabelList": ["Arm 1"],
                    "InterventionOtherNameList": ["Other Name 1"],
                },
            ],
        },
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
                    "CentralContactPhoneExt": "123",
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
                    "LocationCity": "Kihei",
                    "LocationState": "Hawaii",
                    "LocationZip": "96753",
                    "LocationCountry": "United States",
                }
            ],
        },
        "IPDSharingStatementModule": {
            "IPDSharing": "Yes",
            "IPDSharingDescription": "description of the IPD sharing statement",
            "IPDSharingInfoTypeList": [
                "Study Protocol",
                "Statistical Analysis Plan (SAP)",
            ],
            "IPDSharingTimeFrame": "Beginning 9 Months and ending 36 months",
            "IPDSharingAccessCriteria": "This is the IPD sharing access criteria",
            "IPDSharingURL": "https://example.com",
        },
        "ReferencesModule": {
            "ReferenceList": [
                {
                    "ReferenceID": "12345678",
                    "ReferenceType": "Yes",
                    "ReferenceCitation": "This is a reference citation",
                }
            ],
            "SeeAlsoLinkList": [
                {
                    "SeeAlsoLinkLabel": "This is a link label",
                    "SeeAlsoLinkURL": "https://example.com",
                }
            ],
            "AvailIPDList": [
                {
                    "AvailIPDId": "123456",
                    "AvailIPDType": "Clinical Study Report",
                    "AvailIPDURL": "https://example.com",
                    "AvailIPDComment": "This is the avail IPD access criteria",
                }
            ],
        },
    }

    interventional_study_valid_data: Dict[str, Any] = {
        "IdentificationModule": {
            "OrgStudyIdInfo": {
                "OrgStudyId": "RandomStudyId",
                "OrgStudyIdType": "Registry Identifier",
                "OrgStudyIdDomain": "ClinicalTrials.gov",
                "OrgStudyIdLink": "https://clinicaltrials.gov/ct2/show/NCT00000000",
            },
            "SecondaryIdInfoList": [
                {
                    "SecondaryId": "SomeID",
                    "SecondaryIdType": "Other Identifier",
                    "SecondaryIdDomain": "Other",
                    "SecondaryIdLink": "https://example.com",
                }
            ],
        },
        "StatusModule": {
            "OverallStatus": "Suspended",
            "WhyStopped": "Study stopped due to lack of funding",
            "StartDateStruct": {
                "StartDate": "July 07, 2023",
                "StartDateType": "Actual",
            },
            "CompletionDateStruct": {
                "CompletionDate": "July 08, 2024",
                "CompletionDateType": "Actual",
            },
        },
        "SponsorCollaboratorsModule": {
            "ResponsibleParty": {
                "ResponsiblePartyType": "Principal Investigator",
                "ResponsiblePartyInvestigatorFullName": "Harper Spiller",
                "ResponsiblePartyInvestigatorTitle": "Principal Investigator",
                "ResponsiblePartyInvestigatorAffiliation": "White Lotus",
            },
            "LeadSponsor": {"LeadSponsorName": "Harper Spiller"},
            "CollaboratorList": [
                {"CollaboratorName": "Nicole Mossbacher"},
                {"CollaboratorName": "Olivia Mossbacher"},
            ],
        },
        "OversightModule": {
            "OversightHasDMC": "No",
        },
        "DescriptionModule": {
            "BriefSummary": "This is a brief summary",
            "DetailedDescription": "This is a detailed description",
        },
        "ConditionsModule": {
            "ConditionList": ["Condition 1", "Condition 2"],
            "KeywordList": ["Keyword 1", "Keyword 2"],
        },
        "DesignModule": {
            "StudyType": "Interventional",
            "DesignInfo": {
                "DesignAllocation": "Randomized",
                "DesignInterventionModel": "Prevention",
                "DesignInterventionModelDescription": "description",
                "DesignPrimaryPurpose": "Parallel Assignment",
                "DesignMaskingInfo": {
                    "DesignMasking": "Blinded (no details)",
                    "DesignMaskingDescription": "description of the design masking",
                    "DesignWhoMaskedList": ["Participant", "Care Provider"],
                },
            },
            "PhaseList": ["Phase 1/2"],
            "EnrollmentInfo": {
                "EnrollmentCount": "34",
                "EnrollmentType": "Anticipated",
            },
            "NumberArms": "1",
        },
        "ArmsInterventionsModule": {
            "ArmGroupList": [
                {
                    "ArmGroupLabel": "Arm 1",
                    "ArmGroupType": "Placebo Comparator",
                    "ArmGroupDescription": "Experimental",
                    "ArmGroupInterventionList": ["Drug 1"],
                }
            ],
            "InterventionList": [
                {
                    "InterventionType": "Drug",
                    "InterventionName": "Drug 1",
                    "InterventionDescription": "description of the intervention",
                    "InterventionArmGroupLabelList": ["Arm 1"],
                    "InterventionOtherNameList": ["Other Name 1"],
                },
            ],
        },
        "EligibilityModule": {
            "Gender": "All",
            "GenderBased": "No",
            "MinimumAge": "18 Years",
            "MaximumAge": "65 Years",
            "HealthyVolunteers": "No",
            "EligibilityCriteria": "This is the eligibility criteria",
        },
        "ContactsLocationsModule": {
            "CentralContactList": [
                {
                    "CentralContactName": "Ethan Spiller",
                    "CentralContactAffiliation": "White Lotus",
                    "CentralContactPhone": "805-555-5555",
                    "CentralContactPhoneExt": "123",
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
                    "LocationCity": "Kihei",
                    "LocationState": "Hawaii",
                    "LocationZip": "96753",
                    "LocationCountry": "United States",
                }
            ],
        },
        "IPDSharingStatementModule": {
            "IPDSharing": "Yes",
            "IPDSharingDescription": "description of the IPD sharing statement",
            "IPDSharingInfoTypeList": [
                "Study Protocol",
                "Statistical Analysis Plan (SAP)",
            ],
            "IPDSharingTimeFrame": "Beginning 9 Months and ending 36 months ",
            "IPDSharingAccessCriteria": "This is the IPD sharing access criteria",
            "IPDSharingURL": "https://example.com",
        },
        "ReferencesModule": {
            "ReferenceList": [
                {
                    "ReferenceID": "12345678",
                    "ReferenceType": "Yes",
                    "ReferenceCitation": "This is a reference citation",
                }
            ],
            "SeeAlsoLinkList": [
                {
                    "SeeAlsoLinkLabel": "This is a link label",
                    "SeeAlsoLinkURL": "https://example.com",
                }
            ],
            "AvailIPDList": [
                {
                    "AvailIPDId": "123456",
                    "AvailIPDType": "Clinical Study Report",
                    "AvailIPDURL": "https://example.com",
                    "AvailIPDComment": "This is the avail IPD access criteria",
                }
            ],
        },
    }

    def test_observational_valid_study_description(self):
        data = deepcopy(self.observational_study_valid_data)

        output = validate_study_description(data)

        assert output is True

    def test_interventional_valid_study_description(self):
        data = deepcopy(self.interventional_study_valid_data)

        output = validate_study_description(data)

        assert output is True

    def test_invalid_identification_module(self):
        data = deepcopy(self.observational_study_valid_data)

        data["IdentificationModule"]["OrgStudyIdInfo"][
            "OrgStudyIdType"
        ] = "Registry Identifier"

        del data["IdentificationModule"]["OrgStudyIdInfo"]["OrgStudyIdDomain"]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        for item in data["IdentificationModule"]["SecondaryIdInfoList"]:
            item["SecondaryIdType"] = "Other Identifier"
            del item["SecondaryIdDomain"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_status_module(self):
        data = deepcopy(self.observational_study_valid_data)

        data["StatusModule"]["OverallStatus"] = "Terminated"

        del data["StatusModule"]["WhyStopped"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_sponsor_collaborators_module(self):
        data = deepcopy(self.observational_study_valid_data)

        data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyType"
        ] = "Sponsor-Investigator"

        del data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyInvestigatorFullName"
        ]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyType"
        ] = "Sponsor-Investigator"

        del data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyInvestigatorTitle"
        ]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyType"
        ] = "Sponsor-Investigator"

        del data["SponsorCollaboratorsModule"]["ResponsibleParty"][
            "ResponsiblePartyInvestigatorAffiliation"
        ]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_arms_interventions_module(self):
        data = deepcopy(self.interventional_study_valid_data)

        for item in data["ArmsInterventionsModule"]["ArmGroupList"]:
            del item["ArmGroupType"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_eligibilty_module(self):
        data = deepcopy(self.interventional_study_valid_data)

        del data["EligibilityModule"]["HealthyVolunteers"]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        del data["EligibilityModule"]["SamplingMethod"]

        output = validate_study_description(data)

        assert output is False

        data = deepcopy(self.observational_study_valid_data)

        del data["EligibilityModule"]["StudyPopulation"]

        output = validate_study_description(data)

        assert output is False

    def test_invalid_contacts_locations_module(self):
        data = deepcopy(self.observational_study_valid_data)

        del data["ContactsLocationsModule"]["CentralContactList"]

        output = validate_study_description(data)

        # should fail because LocationContactList is
        # required if CentralContactList is not present
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
