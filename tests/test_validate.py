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
                "subjectScheme": "MeSH",
                "schemeURI": "https://www.nlm.nih.gov/mesh/",
                "valueURI": "https://www.nlm.nih.gov/mesh/1234567",
                "classificationCode": "E11.9",
            }
        ],
        "managingOrganisation": {
            "name": "Test Organisation",
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
                "rightsIdentifier": "CC0-1.0",
                "rightsIdentifierScheme": "SPDX",
                "schemeURI": "https://spdx.org/licenses/",
            }
        ],
        "publisher": {
            "publisherName": "Test Publisher",
            "publisherIdentifier": "04z8jg394",
            "publisherIdentifierScheme": "ROR",
            "schemeURI": "https://www.crossref.org/",
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


# class TestValidateStudyDescription:
#     """Unit tests for validate_study_description function."""

#     observational_study_valid_data: Dict[str, Any] = {
#         "IdentificationModule": {
#             "OrgStudyIdInfo": {
#                 "OrgStudyId": "RandomStudyId",
#                 "OrgStudyIdType": "Registry Identifier",
#                 "OrgStudyIdDomain": "ClinicalTrials.gov",
#                 "OrgStudyIdLink": "https://clinicaltrials.gov/ct2/show/NCT00000000",
#             },
#             "SecondaryIdInfoList": [
#                 {
#                     "SecondaryId": "SomeID",
#                     "SecondaryIdType": "Other Identifier",
#                     "SecondaryIdDomain": "Other",
#                     "SecondaryIdLink": "https://example.com",
#                 }
#             ],
#         },
#         "StatusModule": {
#             "OverallStatus": "Suspended",
#             "WhyStopped": "Study stopped due to lack of funding",
#             "StartDateStruct": {
#                 "StartDate": "July 07, 2023",
#                 "StartDateType": "Actual",
#             },
#             "CompletionDateStruct": {
#                 "CompletionDate": "July 08, 2024",
#                 "CompletionDateType": "Actual",
#             },
#         },
#         "SponsorCollaboratorsModule": {
#             "ResponsibleParty": {
#                 "ResponsiblePartyType": "Principal Investigator",
#                 "ResponsiblePartyInvestigatorFullName": "Harper Spiller",
#                 "ResponsiblePartyInvestigatorTitle": "Principal Investigator",
#                 "ResponsiblePartyInvestigatorAffiliation": "White Lotus",
#             },
#             "LeadSponsor": {"LeadSponsorName": "Harper Spiller"},
#             "CollaboratorList": [
#                 {"CollaboratorName": "Nicole Mossbacher"},
#                 {"CollaboratorName": "Olivia Mossbacher"},
#             ],
#         },
#         "OversightModule": {
#             "OversightHasDMC": "No",
#         },
#         "DescriptionModule": {
#             "BriefSummary": "This is a brief summary",
#             "DetailedDescription": "This is a detailed description",
#         },
#         "ConditionsModule": {
#             "ConditionList": ["Condition 1", "Condition 2"],
#             "KeywordList": ["Keyword 1", "Keyword 2"],
#         },
#         "DesignModule": {
#             "StudyType": "Observational",
#             "DesignInfo": {
#                 "DesignObservationalModelList": ["Cohort"],
#                 "DesignTimePerspectiveList": ["Prospective"],
#             },
#             "BioSpec": {
#                 "BioSpecRetention": "Samples With DNA",
#                 "BioSpecDescription": "This is a description of the biospecs",
#             },
#             "EnrollmentInfo": {
#                 "EnrollmentCount": "34",
#                 "EnrollmentType": "Anticipated",
#             },
#             "TargetDuration": "4 Years",
#             "NumberGroupsCohorts": "1",
#         },
#         "ArmsInterventionsModule": {
#             "ArmGroupList": [
#                 {"ArmGroupLabel": "Arm 1", "ArmGroupDescription": "Experimental"}
#             ],
#             "InterventionList": [
#                 {
#                     "InterventionType": "Drug",
#                     "InterventionName": "Drug 1",
#                     "InterventionDescription": "description of the intervention",
#                     "InterventionArmGroupLabelList": ["Arm 1"],
#                     "InterventionOtherNameList": ["Other Name 1"],
#                 },
#             ],
#         },
#         "EligibilityModule": {
#             "Gender": "All",
#             "GenderBased": "No",
#             "MinimumAge": "18 Years",
#             "MaximumAge": "65 Years",
#             "EligibilityCriteria": "This is the eligibility criteria",
#             "StudyPopulation": "This is the study population",
#             "SamplingMethod": "Non-Probability Sample",
#         },
#         "ContactsLocationsModule": {
#             "CentralContactList": [
#                 {
#                     "CentralContactName": "Ethan Spiller",
#                     "CentralContactAffiliation": "White Lotus",
#                     "CentralContactPhone": "805-555-5555",
#                     "CentralContactPhoneExt": "123",
#                     "CentralContactEMail": "e.spiller@hbo.com",
#                 }
#             ],
#             "OverallOfficialList": [
#                 {
#                     "OverallOfficialName": "Daphne Sullivan",
#                     "OverallOfficialAffiliation": "White Lotus",
#                     "OverallOfficialRole": "Study Principal Investigator",
#                 }
#             ],
#             "LocationList": [
#                 {
#                     "LocationFacility": "White Lotus",
#                     "LocationStatus": "Recruiting",
#                     "LocationCity": "Kihei",
#                     "LocationState": "Hawaii",
#                     "LocationZip": "96753",
#                     "LocationCountry": "United States",
#                 }
#             ],
#         },
#         "IPDSharingStatementModule": {
#             "IPDSharing": "Yes",
#             "IPDSharingDescription": "description of the IPD sharing statement",
#             "IPDSharingInfoTypeList": [
#                 "Study Protocol",
#                 "Statistical Analysis Plan (SAP)",
#             ],
#             "IPDSharingTimeFrame": "Beginning 9 Months and ending 36 months",
#             "IPDSharingAccessCriteria": "This is the IPD sharing access criteria",
#             "IPDSharingURL": "https://example.com",
#         },
#         "ReferencesModule": {
#             "ReferenceList": [
#                 {
#                     "ReferenceID": "12345678",
#                     "ReferenceType": "Yes",
#                     "ReferenceCitation": "This is a reference citation",
#                 }
#             ],
#             "SeeAlsoLinkList": [
#                 {
#                     "SeeAlsoLinkLabel": "This is a link label",
#                     "SeeAlsoLinkURL": "https://example.com",
#                 }
#             ],
#             "AvailIPDList": [
#                 {
#                     "AvailIPDId": "123456",
#                     "AvailIPDType": "Clinical Study Report",
#                     "AvailIPDURL": "https://example.com",
#                     "AvailIPDComment": "This is the avail IPD access criteria",
#                 }
#             ],
#         },
#     }

#     interventional_study_valid_data: Dict[str, Any] = {
#         "IdentificationModule": {
#             "OrgStudyIdInfo": {
#                 "OrgStudyId": "RandomStudyId",
#                 "OrgStudyIdType": "Registry Identifier",
#                 "OrgStudyIdDomain": "ClinicalTrials.gov",
#                 "OrgStudyIdLink": "https://clinicaltrials.gov/ct2/show/NCT00000000",
#             },
#             "SecondaryIdInfoList": [
#                 {
#                     "SecondaryId": "SomeID",
#                     "SecondaryIdType": "Other Identifier",
#                     "SecondaryIdDomain": "Other",
#                     "SecondaryIdLink": "https://example.com",
#                 }
#             ],
#         },
#         "StatusModule": {
#             "OverallStatus": "Suspended",
#             "WhyStopped": "Study stopped due to lack of funding",
#             "StartDateStruct": {
#                 "StartDate": "July 07, 2023",
#                 "StartDateType": "Actual",
#             },
#             "CompletionDateStruct": {
#                 "CompletionDate": "July 08, 2024",
#                 "CompletionDateType": "Actual",
#             },
#         },
#         "SponsorCollaboratorsModule": {
#             "ResponsibleParty": {
#                 "ResponsiblePartyType": "Principal Investigator",
#                 "ResponsiblePartyInvestigatorFullName": "Harper Spiller",
#                 "ResponsiblePartyInvestigatorTitle": "Principal Investigator",
#                 "ResponsiblePartyInvestigatorAffiliation": "White Lotus",
#             },
#             "LeadSponsor": {"LeadSponsorName": "Harper Spiller"},
#             "CollaboratorList": [
#                 {"CollaboratorName": "Nicole Mossbacher"},
#                 {"CollaboratorName": "Olivia Mossbacher"},
#             ],
#         },
#         "OversightModule": {
#             "OversightHasDMC": "No",
#         },
#         "DescriptionModule": {
#             "BriefSummary": "This is a brief summary",
#             "DetailedDescription": "This is a detailed description",
#         },
#         "ConditionsModule": {
#             "ConditionList": ["Condition 1", "Condition 2"],
#             "KeywordList": ["Keyword 1", "Keyword 2"],
#         },
#         "DesignModule": {
#             "StudyType": "Interventional",
#             "DesignInfo": {
#                 "DesignAllocation": "Randomized",
#                 "DesignInterventionModel": "Prevention",
#                 "DesignInterventionModelDescription": "description",
#                 "DesignPrimaryPurpose": "Parallel Assignment",
#                 "DesignMaskingInfo": {
#                     "DesignMasking": "Blinded (no details)",
#                     "DesignMaskingDescription": "description of the design masking",
#                     "DesignWhoMaskedList": ["Participant", "Care Provider"],
#                 },
#             },
#             "PhaseList": ["Phase 1/2"],
#             "EnrollmentInfo": {
#                 "EnrollmentCount": "34",
#                 "EnrollmentType": "Anticipated",
#             },
#             "NumberArms": "1",
#         },
#         "ArmsInterventionsModule": {
#             "ArmGroupList": [
#                 {
#                     "ArmGroupLabel": "Arm 1",
#                     "ArmGroupType": "Placebo Comparator",
#                     "ArmGroupDescription": "Experimental",
#                     "ArmGroupInterventionList": ["Drug 1"],
#                 }
#             ],
#             "InterventionList": [
#                 {
#                     "InterventionType": "Drug",
#                     "InterventionName": "Drug 1",
#                     "InterventionDescription": "description of the intervention",
#                     "InterventionArmGroupLabelList": ["Arm 1"],
#                     "InterventionOtherNameList": ["Other Name 1"],
#                 },
#             ],
#         },
#         "EligibilityModule": {
#             "Gender": "All",
#             "GenderBased": "No",
#             "MinimumAge": "18 Years",
#             "MaximumAge": "65 Years",
#             "HealthyVolunteers": "No",
#             "EligibilityCriteria": "This is the eligibility criteria",
#         },
#         "ContactsLocationsModule": {
#             "CentralContactList": [
#                 {
#                     "CentralContactName": "Ethan Spiller",
#                     "CentralContactAffiliation": "White Lotus",
#                     "CentralContactPhone": "805-555-5555",
#                     "CentralContactPhoneExt": "123",
#                     "CentralContactEMail": "e.spiller@hbo.com",
#                 }
#             ],
#             "OverallOfficialList": [
#                 {
#                     "OverallOfficialName": "Daphne Sullivan",
#                     "OverallOfficialAffiliation": "White Lotus",
#                     "OverallOfficialRole": "Study Principal Investigator",
#                 }
#             ],
#             "LocationList": [
#                 {
#                     "LocationFacility": "White Lotus",
#                     "LocationStatus": "Recruiting",
#                     "LocationCity": "Kihei",
#                     "LocationState": "Hawaii",
#                     "LocationZip": "96753",
#                     "LocationCountry": "United States",
#                 }
#             ],
#         },
#         "IPDSharingStatementModule": {
#             "IPDSharing": "Yes",
#             "IPDSharingDescription": "description of the IPD sharing statement",
#             "IPDSharingInfoTypeList": [
#                 "Study Protocol",
#                 "Statistical Analysis Plan (SAP)",
#             ],
#             "IPDSharingTimeFrame": "Beginning 9 Months and ending 36 months ",
#             "IPDSharingAccessCriteria": "This is the IPD sharing access criteria",
#             "IPDSharingURL": "https://example.com",
#         },
#         "ReferencesModule": {
#             "ReferenceList": [
#                 {
#                     "ReferenceID": "12345678",
#                     "ReferenceType": "Yes",
#                     "ReferenceCitation": "This is a reference citation",
#                 }
#             ],
#             "SeeAlsoLinkList": [
#                 {
#                     "SeeAlsoLinkLabel": "This is a link label",
#                     "SeeAlsoLinkURL": "https://example.com",
#                 }
#             ],
#             "AvailIPDList": [
#                 {
#                     "AvailIPDId": "123456",
#                     "AvailIPDType": "Clinical Study Report",
#                     "AvailIPDURL": "https://example.com",
#                     "AvailIPDComment": "This is the avail IPD access criteria",
#                 }
#             ],
#         },
#     }

#     def test_observational_valid_study_description(self):
#         """Test valid observational study description."""
#         data = deepcopy(self.observational_study_valid_data)

#         output = validate_study_description(data)

#         assert output is True

#     def test_interventional_valid_study_description(self):
#         """Test valid interventional study description."""
#         data = deepcopy(self.interventional_study_valid_data)

#         output = validate_study_description(data)

#         assert output is True

#     def test_invalid_identification_module(self):
#         """Test invalid identification module."""
#         data = deepcopy(self.observational_study_valid_data)

#         data["IdentificationModule"]["OrgStudyIdInfo"][
#             "OrgStudyIdType"
#         ] = "Registry Identifier"

#         del data["IdentificationModule"]["OrgStudyIdInfo"]["OrgStudyIdDomain"]

#         output = validate_study_description(data)

#         assert output is False

#         data = deepcopy(self.observational_study_valid_data)

#         # sourcery skip: no-loop-in-tests
#         for item in data["IdentificationModule"]["SecondaryIdInfoList"]:
#             item["SecondaryIdType"] = "Other Identifier"
#             del item["SecondaryIdDomain"]

#         output = validate_study_description(data)

#         assert output is False

#     def test_invalid_status_module(self):
#         """Test invalid status module."""
#         data = deepcopy(self.observational_study_valid_data)

#         data["StatusModule"]["OverallStatus"] = "Terminated"

#         del data["StatusModule"]["WhyStopped"]

#         output = validate_study_description(data)

#         assert output is False

#     def test_invalid_sponsor_collaborators_module(self):
#         """Test invalid sponsor collaborators module."""
#         data = deepcopy(self.observational_study_valid_data)

#         data["SponsorCollaboratorsModule"]["ResponsibleParty"][
#             "ResponsiblePartyType"
#         ] = "Sponsor-Investigator"

#         del data["SponsorCollaboratorsModule"]["ResponsibleParty"][
#             "ResponsiblePartyInvestigatorFullName"
#         ]

#         output = validate_study_description(data)

#         assert output is False

#         data = deepcopy(self.observational_study_valid_data)

#         data["SponsorCollaboratorsModule"]["ResponsibleParty"][
#             "ResponsiblePartyType"
#         ] = "Sponsor-Investigator"

#         del data["SponsorCollaboratorsModule"]["ResponsibleParty"][
#             "ResponsiblePartyInvestigatorTitle"
#         ]

#         output = validate_study_description(data)

#         assert output is False

#         data = deepcopy(self.observational_study_valid_data)

#         data["SponsorCollaboratorsModule"]["ResponsibleParty"][
#             "ResponsiblePartyType"
#         ] = "Sponsor-Investigator"

#         del data["SponsorCollaboratorsModule"]["ResponsibleParty"][
#             "ResponsiblePartyInvestigatorAffiliation"
#         ]

#         output = validate_study_description(data)

#         assert output is False

#     def test_invalid_arms_interventions_module(self):
#         """Test invalid arms interventions module."""
#         data = deepcopy(self.interventional_study_valid_data)

#         for item in data["ArmsInterventionsModule"]["ArmGroupList"]:
#             del item["ArmGroupType"]

#         output = validate_study_description(data)

#         assert output is False

#     def test_invalid_eligibilty_module(self):
#         """Test invalid eligibility module."""
#         data = deepcopy(self.interventional_study_valid_data)

#         del data["EligibilityModule"]["HealthyVolunteers"]

#         output = validate_study_description(data)

#         assert output is False

#         data = deepcopy(self.observational_study_valid_data)

#         del data["EligibilityModule"]["SamplingMethod"]

#         output = validate_study_description(data)

#         assert output is False

#         data = deepcopy(self.observational_study_valid_data)

#         del data["EligibilityModule"]["StudyPopulation"]

#         output = validate_study_description(data)

#         assert output is False

#     def test_invalid_contacts_locations_module(self):
#         """Test invalid contacts locations module."""
#         data = deepcopy(self.observational_study_valid_data)

#         del data["ContactsLocationsModule"]["CentralContactList"]

#         output = validate_study_description(data)

#         # should fail because LocationContactList is
#         # required if CentralContactList is not present
#         assert output is False


# class TestValidateReadme:
#     """Unit tests for validate_readme function."""

#     def test_minimal_valid_readme(self):

#         data = {"Title": "Test Title"}

#         output = validate_readme(data)

#         assert output is True

#     def test_valid_readme_with_all_fields(self):
#         data = {
#             "Title": "Test Title",
#             "Identifier": "10.5281/zenodo.1234567",
#             "Version": "1.0.0",
#             "PublicationDate": "2021-01-01",
#             "About": "Test about",
#             "DatasetDescription": "Test dataset description",
#             "DatasetAccess": "Test dataset access",
#             "StandardsFolllowed": "Test standards followed",
#             "Resources": "Test resources",
#             "License": "Test license",
#             "HowToCite": "Test how to cite",
#             "Acknowledgement": "Test acknowledgement",
#         }

#         output = validate_readme(data)

#         assert output is True

#     def test_fail_invalid_title(self):
#         data = {"Title": 1}

#         output = validate_readme(data)

#         assert output is False

#     def test_fail_invalid_identifier(self):
#         data = {"Title": "Test Title", "Identifier": 1}

#         output = validate_readme(data)

#         assert output is False

#     def test_fail_invalid_publication_date(self):
#         data = {"Title": "Test Title", "PublicationDate": "Invalid"}

#         output = validate_readme(data)

#         assert output is False


# class TestValidateLicense:
#     """Unit tests for validate_license function."""

#     def test_valid_license(self):
#         """Test valid license."""
#         data = "CC-BY-4.0"

#         output = validate_license(data)

#         assert output is True

#     def test_fail_invalid_license(self):
#         """Test invalid license."""
#         data = {
#             "License": "Invalid",
#         }

#         output = validate_license(data)

#         assert output is False


# class TestValidateParticipants:
#     """Unit tests for validate_participants function."""

#     def test_minimal_valid_participant(self):
#         """Test minimal valid participant."""
#         data = [
#             {
#                 "participant_id": "sub-user1",
#             }
#         ]

#         output = validate_participants(data)

#         assert output is True

#     def test_valid_participant_with_all_fields(self):
#         """Test valid participant with all fields."""
#         data = [
#             {
#                 "participant_id": "sub-user1",
#                 "species": "homo sapiens",
#                 "age": 0.5,
#                 "sex": "Female",
#                 "handedness": "Right",
#                 "strain": "C57BL/6J",
#                 "strain_rrid": "RRID:IMSR_JAX:000664",
#             }
#         ]

#         output = validate_participants(data)

#         assert output is True

#     def test_invalid_participant_id(self):
#         data: list[dict[str, str]] = [{}]

#         output = validate_participants(data)

#         assert output is False

#         data = [{"participant_id": "bus-asd"}]

#         output = validate_participants(data)

#         assert output is False

#     def test_invalid_age(self):
#         data = [{"participant_id": "sub-sample1", "age": 0}]

#         output = validate_participants(data)

#         assert output is False

#         data = [{"participant_id": "sub-sample1", "age": -5}]

#         output = validate_participants(data)

#         assert output is False

#         data = [{"participant_id": "sub-sample1", "age": "5"}]

#         output = validate_participants(data)

#         assert output is False

#     def test_invalid_sex(self):
#         data = [{"participant_id": "sub-sample1", "sex": 0}]

#         output = validate_participants(data)

#         assert output is False

#         data = [{"participant_id": "sub-sample1", "sex": "Invalid"}]

#         output = validate_participants(data)

#         assert output is False

#     def test_invalid_handedness(self):
#         data = [{"participant_id": "sub-sample1", "handedness": 0}]

#         output = validate_participants(data)

#         assert output is False

#         data = [{"participant_id": "sub-sample1", "handedness": "Invalid"}]

#         output = validate_participants(data)

#         assert output is False


# class TestValidateDatatypeDescription:
#     def test_invalid_datatype_description(self):
#         data = ["ekg", "redcap_data", "oct", "invalid"]

#         output = validate_datatype_dictionary(data)

#         assert output is False

#     def test_valid_datatype_description(self):
#         data = ["ekg", "redcap_data", "oct"]

#         output = validate_datatype_dictionary(data)

#         assert output is True
