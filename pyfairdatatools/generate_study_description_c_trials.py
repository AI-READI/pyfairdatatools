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
    oversight = cds_data.get("oversightModule", {})

    def bool_to_yes_no(value):
        return "Yes" if value is True else "No" if value is False else ""

    full_criteria = eligibility.get("eligibilityCriteria", "").strip()
    inclusion = exclusion = ""

    if "Inclusion Criteria:" in full_criteria:
        inclusion = full_criteria.split("Inclusion Criteria:")[-1].split("Exclusion Criteria:")[0].strip()
    if "Exclusion Criteria:" in full_criteria:
        exclusion = full_criteria.split("Exclusion Criteria:")[-1].strip()

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
            } for s in identification.get("secondaryIdInfos", [{}])],},
        "statusModule": {
            "overallStatus": status_map.get(raw_status, raw_status.replace("_", " ").title()),
            "startDateStruct": {
               "startDate": cds_data.get("statusModule", {}).get("startDateStruct", {}).get("date", ""),
                "startDateType": cds_data.get("statusModule", {}).get("startDateStruct", {}).get("type", "").capitalize()
            },
            "completionDateStruct": {
               "completionDate" : cds_data.get("statusModule", {}).get("completionDateStruct", {}).get("date", ""),
               "completionDateType" : cds_data.get("statusModule", {}).get("completionDateStruct", {}).get("type", "").capitalize(),
            },
        },
        "sponsorCollaboratorsModule": {
            "leadSponsor": {
                "leadSponsorName": collaborators.get("leadSponsor", {}).get("name", ""),
                "leadSponsorIdentifier": collaborators.get("leadSponsor", {}).get("identifier", "")
            },
            "responsibleParty": {
                "responsiblePartyType": collaborators.get("responsibleParty", {}).get("type", "")
                .replace("_", " ").title(),
                # "responsiblePartyInvestigatorFirstName": collaborators.get("responsibleParty", {}).get(
                #     "investigatorFullName", ""),
                # "responsiblePartyInvestigatorLastName": collaborators.get("responsibleParty", {}).get(
                #     "investigatorFullName", ""),
                # "responsiblePartyInvestigatorTitle": collaborators.get("responsibleParty", {}).get("investigatorTitle", ""),
                # "responsiblePartyInvestigatorIdentifier": collaborators.get("responsibleParty", {}).get(
                #     "investigatorIdentifier", ""),
                # "responsiblePartyInvestigatorAffiliation": collaborators.get("responsibleParty", {}).get(
                #     "investigatorAffiliation", ""),
            },
            "collaboratorList": [
                {
                    "collaboratorName": c.get("name", ""),
                    "collaboratorNameIdentifier": c.get("identifier", ""),
                }
                for c in collaborators.get("collaborators", [{}])
            ],
        },
        "oversightModule": {
            "oversightHasDMC": bool_to_yes_no(oversight.get("oversightHasDmc")),
            "isFDARegulatedDrug": bool_to_yes_no(oversight.get("isFdaRegulatedDrug")),
            "isFDARegulatedDevice": bool_to_yes_no(oversight.get("isFdaRegulatedDevice")),
            "humanSubjectReviewStatus": oversight.get("humanSubjectReviewStatus", "Request not yet submitted")
        },
        "descriptionModule":
            {
                "briefSummary": cds_data["descriptionModule"]["briefSummary"],

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
        },
        "designModule": {
            "studyType": design.get("studyType", "").capitalize(),
            "phaseList": design.get("phases", []),
            "numberArms": design.get("numberArms", "0"),
            "enrollmentInfo": {
                "enrollmentCount": design.get("enrollmentInfo", {}).get("count", ""),
                "enrollmentType": design.get("enrollmentInfo", {}).get("type", "")
            },
            "isPatientRegistry":  bool_to_yes_no(design.get("patientRegistry")),
            "bioSpec": {
                    "bioSpecRetention": design.get("bioSpecRetention", ""),
                    "bioSpecDescription": design.get("bioSpecDescription", ""),
                },
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
                } for i in arms_int.get("interventions", [{}])
        ],},
        "eligibilityModule": {
            "sex": eligibility.get("sex", "").capitalize(),
            "genderBased": eligibility.get("genderBased", "No"),
            "minimumAge": eligibility.get("minimumAge", ""),
            "maximumAge": eligibility.get("maximumAge", ""),
            "healthyVolunteers": bool_to_yes_no(eligibility.get("healthyVolunteers")),
            "eligibilityCriteria": {
                "eligibilityCriteriaInclusion": inclusion,
                "eligibilityCriteriaExclusion": exclusion,
            },
        },
        "contactsLocationsModule": {
            "centralContactList": [
                {
                    "centralContactFirstName": c.get("name", ""),
                    "centralContactLastName": c.get("name", ""),
                    "centralContactAffiliation": c.get("role", ""),
                    "centralContactEMail": c.get("email", ""),
                 }
                for c in contacts.get("centralContacts", [{}])],
            "overallOfficialList": [
                {
                    "overallOfficialFirstName": c.get("name", ""),
                    "overallOfficialLastName": c.get("name", ""),
                    "overallOfficialAffiliation": c.get("affiliation", ""),
                    "overallOfficialRole": c.get("role", ""),

                }
                for c in contacts.get("overallOfficials", [{}])],
            "locationList": [
                {
                    "locationFacility": c.get("facility", ""),
                    "locationStatus": c.get("status", ""),
                    "locationCity": c.get("city", ""),
                    "locationCountry": c.get("county", ""),

                    "locationState": c.get("state", ""),
                    "locationZip": c.get("zip", ""),
                    "locationContactList": c.get("contactList", ""),
                    "locationIdentifier": c.get("identifier", ""),
                }
                for c in contacts.get("locations", [{}])],
        },
    }

    if not data.get("schema"):
        data["schema"] = "https://schema.aireadi.org/v0.1.0/study_description.json"

    status_module = data.setdefault("statusModule", {})
    completion_date_struct = status_module.setdefault("completionDateStruct", {})

    if completion_date_struct.get("completionDateType") == "Estimated":
        completion_date_struct["completionDateType"] = "Anticipated"

    if data.get("statusModule", {}).get("completionDateType") == "Estimated":
        data["statusModule"]["completionDateType"] = "Anticipated"

    if "whyStopped" in cds_data.get("statusModule", {}):
        data.setdefault("statusModule", {})["whyStopped"] = cds_data["statusModule"]["whyStopped"]

    if "keywordList" in cds_data.get("conditionsModule", {}):
        data.setdefault("conditionsModule", {})["keywords"] = cds_data["conditionsModule"]["keywordList"]

    for d in ["detailedDescription"]:
        if d in cds_data.get("descriptionModule", {}):
            data.setdefault("descriptionModule", {})[d] = cds_data["descriptionModule"][d]

    for d in ["targetDuration"]:
        if d in design:
            data["designModule"][d] = design[d]

    fields = {
        "Interventional": ["designMaskingInfo", "designPrimaryPurpose", "designInterventionModel", "designAllocation"],
        "Observational": ["designObservationalModelList", "designTimePerspectiveList"]
    }
    for f in fields.get(data["designModule"]["studyType"], []):
        data["designModule"].setdefault("designInfo", {}).setdefault(f, "")

    for k in ["genderDescription", "studyPopulation", "samplingMethod"]:
        if k in eligibility:
            v = eligibility[k]
            if k == "samplingMethod":
                v = {"NON_PROBABILITY_SAMPLE": "Non-Probability Sample",
                     "PROBABILITY_SAMPLE": "Probability Sample"}.get(v, v)
            data["eligibilityModule"][k] = v

    try:
        if not validate.validate_study_description(data):
            print("Study description is invalid.")
    except ValueError as ve:
        print("Validation errors:")
        raise

    file_name = f"clinical_study_description_{identifier}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved study description to: {file_name}")
    return data


fetch_the_clinical_trials_data("NCT04091373")
#  NCT04091373 NCT06002048