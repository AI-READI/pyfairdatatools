"""Unit tests for pyfairdatatools.generate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

import json
from os import path

from pyfairdatatools.generate import (
    generate_changelog_file,
    generate_dataset_description,
    generate_license_file,
    generate_readme,
    generate_study_description,
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
