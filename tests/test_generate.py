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
            "schema": "https://schema.aireadi.org/v0.1.0/dataset_description.json",
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
        "schema": "https://schema.aireadi.org/v0.1.0/study_description.json",
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

        file = tmp_path / "study_description.json"
        file_type = "json"

        generate_study_description(data, file, file_type)

        with open(file, "r", encoding="utf8") as f:
            imported_data = json.load(f)

        assert imported_data == data

        file = tmp_path / "study_description.xml"
        file_type = "xml"

        # generate_study_description(data, file, file_type)

        # TODO: add validation of the XML file

    def test_interventional_study_description(self, tmp_path):
        data = {
            "schema": "https://schema.aireadi.org/v0.1.0/study_description.json",
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
