import re
import requests
import json
# from . import validate
import validate


def fetch_the_clinical_trials_data(identifier):
    if not (isinstance(identifier, str) and re.match(r"^NCT\d{8}$", identifier.strip())):
        return {"error": "Invalid identifier format."}, 400

    url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        return {
            "error": "No clinical study was found with the provided identifier",
            "status_code":                      404,
            "message": f"No study found for identifier '{identifier}'.",
        }, 404

    cds_data = response.json().get("protocolSection", {})
    status_map = {
        "WITHDRAWN": "Withdrawn",
        "RECRUITING": "Recruiting",
        "ACTIVE_NOT_RECRUITING": "Active, not recruiting",
        "NOT_YET_RECRUITING": "Not yet recruiting",
        "SUSPENDED": "Suspended",
        "ENROLLING_BY_INVITATION": "Enrolling by invitation",
        "COMPLETED": "Completed",
        "TERMINATED": "Terminated",
    }
    raw_status = cds_data.get("statusModule", {}).get("overallStatus", "")
    identification = cds_data.get("identificationModule", {})
    conditions = cds_data.get("conditionsModule", {}).get("conditions", [])
    design = cds_data.get("designModule", {})
    arms_int = cds_data.get("armsInterventionsModule", {})
    eligibility = cds_data.get("eligibilityModule", {})
    contacts = cds_data.get("contactsLocationsModule", {})
    collaborators = cds_data.get("sponsorCollaboratorsModule", {})

    data = {
        "schema": "",
        "identificationModule": {
            "officialTitle":identification.get("officialTitle", ""),
            "acronym": "",
            "orgStudyIdInfo": {
                "orgStudyId":identification.get("orgStudyIdInfo", {}).get("id", ""),
                "orgStudyIdType":identification.get("orgStudyIdType", {}).get("info", ""),
                "orgStudyIdLink":identification.get("orgStudyIdLink", {}).get("link", ""),
                "orgStudyIdDomain": ""
            },
            "secondaryIdInfoList": [{
                "secondaryId": s.get("id", ""),
                "secondaryIdType": s.get("type", ""),
                "secondaryIdLink": s.get("link", ""),
                "secondaryIdDomain": "",
            } for s in identification.get("secondaryIdInfos", [])],},
        "statusModule": {
            "overallStatus": status_map.get(raw_status, raw_status.replace("_", " ").title()),
            "startDateStruct": cds_data.get("statusModule", {}).get("startDateStruct", {}).get("date", ""),
            "whyStopped": cds_data.get("statusModule", {}).get("whyStopped", {}).get("date", ""),
            "completionDateStruct": cds_data.get("statusModule", {}).get("completionDateStruct", {}).get("date", ""),
        },
        "sponsorCollaboratorsModule": {
            "leadSponsor": {
                "LeadSponsorName": collaborators.get("leadSponsor", {}).get("name", "")
            },
            "responsiblePartyInvestigatorFirstName": collaborators.get("responsibleParty", {}).get(
                "investigatorFirstName", ""),
            "responsiblePartyInvestigatorLastName": collaborators.get("responsibleParty", {}).get(
                "investigatorLastName", ""),
            "responsiblePartyInvestigatorTitle": collaborators.get("responsibleParty", {}).get("investigatorTitle", ""),
            "responsiblePartyInvestigatorIdentifier": collaborators.get("responsibleParty", {}).get(
                "investigatorIdentifier", ""),
            "responsiblePartyInvestigatorAffiliation": collaborators.get("responsibleParty", {}).get(
                "investigatorAffiliation", ""),
            "responsibleParty": collaborators.get("responsibleParty", {}).get("type", ""),
            "collaboratorList": [
                {
                    "collaboratorName": c.get("name", ""),
                    "collaboratorNameIdentifier": c.get("identifier", ""),
                }
                for c in collaborators.get("collaboratorList", [])
            ],
        },
        "oversightModule": {
            "oversightHasDMC": cds_data.get("oversightModule", {}).get("oversightHasDmc", ""),
            "isFDARegulatedDrug": cds_data.get("oversightModule", {}).get("isFdaRegulatedDrug", ""),
            "isFDARegulatedDevice": cds_data.get("oversightModule", {}).get("isFdaRegulatedDevice", ""),
            "humanSubjectReviewStatus": cds_data.get("oversightModule", {}).get("humanSubjectReviewStatus", "")
        },
        "descriptionModule":
            {
                "briefSummary": cds_data["descriptionModule"]["briefSummary"],
                "detailedDescription": cds_data.get("descriptionModule", {}).get("detailedDescription", ""),

             },
        "conditionsModule": {
            "conditionList": [
                {
                    "conditionName": cnd,
                    "conditionIdentifier": {
                        "conditionClassificationCode":"",
                        "conditionScheme": "",
                        "schemeURI": "",
                        "conditionURI": "",
                    },
                 } for cnd in conditions],
            "keywordList": [
                {
                    "keywordValue": kw,
                    "keywordIdentifier": "",
                 }
                for kw in cds_data.get("conditionsModule", {}).get("keywords", [])
            ],
        },
        "designModule": {
            "studyType": design.get("studyType", ""),
            "phaseList": design.get("phases", []),
            "numberArms": design.get("numberArms", ""),
            "enrollmentInfo": {
                "enrollmentCount": design.get("enrollmentInfo", {}).get("count", ""),
                "enrollmentType": design.get("enrollmentInfo", {}).get("type", "")
            },
            "isPatientRegistry": design.get("patientRegistry", False),
            "designInfo": {
                "designObservationalModelList": design.get("designInfo", {}).get("observationalModel", ""),
                "designTimePerspectiveList": design.get("designInfo", {}).get("timePerspective", "")
            },
            "bioSpec": {
                    "bioSpecRetention": design.get("bioSpecRetention", ""),
                    "bioSpecDescription": design.get("bioSpecDescription", ""),
                },
            "targetDuration": "",
        },
        "armsInterventionsModule": {
            "armGroupList": [
                {"armGroupLabel": a.get("label", ""),
                 "armGroupType": a.get("type", ""),
                 "armGroupDescription": a.get("description", ""),
                 "armGroupInterventionList": a.get("interventionNames", [])}
                for a in arms_int.get("armGroups", {})],
            "interventionList": [
                {
                 "interventionType": i.get("type", ""),
                 "interventionName": i.get("name", ""),
                 "interventionDescription": i.get("description", ""),
                 "interventionOtherNameList": i.get("armGroupLabels", "")
                } for i in arms_int.get("interventions", {})
        ],},
        "eligibilityModule": {
            "sex": eligibility.get("sex", ""),
            "genderBased": eligibility.get("genderBased", ""),
            "genderDescription": eligibility.get("genderDescription", ""),
            "minimumAge": eligibility.get("minimumAge", ""),
            "maximumAge": eligibility.get("maximumAge", ""),
            "healthyVolunteers": eligibility.get("healthyVolunteers", ""),
            "eligibilityCriteria": eligibility.get("eligibilityCriteria", ""),
            "studyPopulation": eligibility.get("studyPopulation", ""),
            "samplingMethod": eligibility.get("samplingMethod", ""),
        },
        "contactsLocationsModule": {
            "centralContactList": [
                {
                    "centralContactFirstName": c.get("name", ""),
                    "centralContactLastName": c.get("name", ""),
                    "centralContactDegree": "",
                    "centralContactIdentifier": [],
                    "centralContactAffiliation": c.get("role", ""),
                    "centralContactPhone": c.get("phone", ""),
                    "centralContactPhoneExt": c.get("phoneExt", ""),
                    "centralContactEMail": c.get("email", ""),
                 }
                for c in contacts.get("centralContacts", [])],
            "overallOfficials": [
                {
                    "overallOfficialFirstName": c.get("name", ""),
                    "overallOfficialLastName": c.get("name", ""),
                    "overallOfficialDegree": "",
                    "overallOfficialIdentifier": "",
                    "overallOfficialAffiliation": c.get("affiliation", ""),
                    "overallOfficialRole": c.get("role", ""),
                }
                for c in contacts.get("overallOfficials", [])],
            "locationList": [
                {
                    "locationFacility": c.get("facility", ""),
                    "locationStatus": c.get("status", ""),
                    "locationCity": c.get("city", ""),
                    "locationState": c.get("state", ""),
                    "locationZip": c.get("zip", ""),
                    "locationCountry": c.get("county", ""),
                    "locationContactList": c.get("contactList", ""),
                }
                for c in contacts.get("locations", [])],
        },
    }

    if not validate.validate_study_description(data):
        print("Dataset description is invalid.")
        raise ValueError("Invalid input data")

    file_name = f"clinical_study_description_{identifier}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved study description to: {file_name}")
    print(data, "kkk")
    return data


fetch_the_clinical_trials_data("NCT02901184")