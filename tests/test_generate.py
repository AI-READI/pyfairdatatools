"""Unit tests for pyfairdatatools.generate module."""

# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

import json
from os import path

from pyfairdatatools.generate import (
    generate_changelog_file,
    generate_dataset_description,
    generate_datatype_file,
    generate_license_file,
    generate_readme,
    generate_study_description,
)


class TestGenerateDatasetDescription:
    def test_valid_dataset_description(self, tmp_path):
        data = {
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

        # TODO: Add XML validation


class TestGenerateStudyDescription:
    def test_observational_study_description(self, tmp_path):
        data = {
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

        file = tmp_path / "study_description.json"
        file_type = "json"

        generate_study_description(data, file, file_type)

        with open(file, "r", encoding="utf8") as f:
            imported_data = json.load(f)

        assert imported_data == data

        file = tmp_path / "study_description.xml"
        file_type = "xml"

        generate_study_description(data, file, file_type)

        # TODO: add validation of the XML file

    def test_interventional_study_description(self, tmp_path):
        data = {
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

        file = tmp_path / "study_description.json"
        file_type = "json"

        generate_study_description(data, file, file_type)

        with open(file, "r", encoding="utf8") as f:
            imported_data = json.load(f)

        assert imported_data == data

        file = tmp_path / "study_description.xml"
        file_type = "xml"

        generate_study_description(data, file, file_type)

        # TODO: add validation of the XML file


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


class TestGenerateDatatypeDescription:
    def test_valid_datatype_description(self, tmp_path):
        data = [
            "ecg",
            "eye_fundus_photography_data",
            "flio_data",
            "phyisical_activity_monitoring_data",
        ]

        file = tmp_path / "datatype_description.yaml"
        file_type = "yaml"

        generate_datatype_file(data=data, file_path=file, file_type=file_type)

        assert path.exists(file) is True
