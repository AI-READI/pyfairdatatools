import requests
import json
# from . import validate
import validate
import re


def fetch_the_clinical_trials_data(ct_identifier):
    if not (isinstance(ct_identifier, str) and re.match(r"^NCT\d{8}$", ct_identifier.strip())):
        print("Invalid identifier, exiting function.")
        return

    url = f"https://classic.clinicaltrials.gov/api/v2/studies/{ct_identifier}"
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        return {
            "error": "No clinical study was found with the provided identifier",
            "status_code":                      404,
            "message": f"No study found for identifier '{ct_identifier}'.",
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
    #Assign criteria for the eligibility
    full_criteria = eligibility.get("eligibilityCriteria", "").strip()
    inclusion = []
    exclusion = []

    if "Inclusion Criteria:" in full_criteria:
        inclusion_text = full_criteria.split("Inclusion Criteria:")[-1].split("Exclusion Criteria:")[0].strip()
        inclusion = [line.strip() for line in inclusion_text.splitlines() if line.strip()]

    if "Exclusion Criteria:" in full_criteria:
        exclusion_text = full_criteria.split("Exclusion Criteria:")[-1].strip()
        exclusion = [line.strip() for line in exclusion_text.splitlines() if line.strip()]

    data = {
        "schema": "",
        "identificationModule": {
            "officialTitle":identification.get("officialTitle", ""),
            "acronym": "",
            "orgStudyIdInfo": {
                "orgStudyId":identification.get("orgStudyIdInfo", {}).get("id", ""),
                "orgStudyIdType":identification.get("orgStudyIdType", {}).get("info", "Other Identifier"),
                "orgStudyIdDomain": identification.get("orgStudyIdDomain", {}).get("link", "clinicaltrials.gov")
            },
            "secondaryIdInfoList": [{
                "secondaryId": s.get("id", ""),
                "secondaryIdType": s.get("type", ""),
                "secondaryIdLink": s.get("link", ""),
                "secondaryIdDomain": s.get("domain", "nih.gov"),
            } for s in identification.get("secondaryIdInfos", [])],
        },
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
            },
            "responsibleParty": {
                "responsiblePartyType": collaborators.get("responsibleParty", {}).get("type", "")
                .replace("_", " ").title(),
            },
            "collaboratorList": [
                {
                    "collaboratorName": c.get("name", ""),
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
        "descriptionModule": {
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
            "phaseList": [re.sub(r'(\d+)', r' \1', p).title() for p in design.get("phases", [])],
            "numberArms": design.get("numberArms", "0"),
            "enrollmentInfo": {
                "enrollmentCount": str(design.get("enrollmentInfo", {}).get("count", "")),
                "enrollmentType": design.get("enrollmentInfo", {}).get("type", "").capitalize(),
            },
            "isPatientRegistry":  bool_to_yes_no(design.get("patientRegistry")),
            "bioSpec": {
                    "bioSpecRetention": design.get("bioSpecRetention", "None Retained"),
                    "bioSpecDescription": design.get("bioSpecDescription", "None Retained"),
                },
            "designInfo": {
                    "designAllocation": design.get("designInfo", {}).get("allocation", "").replace("_", "-", 1)
                    .replace("_", " ").replace("-", " ").title(),
                    "designInterventionModel": design.get("designInfo", {}).get("interventionModel", "")
                    .replace("_", "-", 1).replace("_", " ").replace("-", " ").title(),
                    "designPrimaryPurpose": design.get("designInfo", {}).get("primaryPurpose", "")
                .replace("_", "-", 1).replace("_", " ").replace("-", " ").title(),
                    "designMaskingInfo": design.get("designInfo", {}).get("maskingInfo", {}).get("masking", "")
                    .replace("_", "-", 1).replace("_", " ").replace("-", " ").title(),
                "designObservationalModelList": [design.get("designInfo", {}).get("observationalModel", "").replace("_",
                     "-").capitalize()],
                "designTimePerspectiveList": [
                    design.get("designInfo", {}).get("timePerspective", "").replace("_", "-").capitalize()]
            },
        },
        "armsInterventionsModule": {
            "armGroupList": [
                {"armGroupLabel": a.get("label", ""),
                 "armGroupType": a.get("type", "").replace("_", "-", 1).replace("_", " ").replace("-", " ").title(),
                 "armGroupDescription": a.get("description", ""),
                 "armGroupInterventionList": a.get("interventionNames", [])}
                for a in arms_int.get("armGroups", {})],
            "interventionList": [
                {
                 "interventionType": i.get("type", "").replace("_", "-", 1).replace("_", " ").replace("-", " ").title(),
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
                for c in contacts.get("centralContacts", [])],
            "overallOfficialList": [
                {
                    "overallOfficialFirstName": c.get("name", ""),
                    "overallOfficialLastName": c.get("name", ""),
                    "overallOfficialAffiliation": {
                        "overallOfficialAffiliationName": c.get("name", ""),
                        "overallOfficialAffiliationIdentifier": c.get("identifier", "")
                    },
                    "overallOfficialRole": c.get("role", ""),

                }
                for c in contacts.get("overallOfficials", [{}])],
            "locationList": [
                {
                    "locationFacility": c.get("facility", ""),
                    "locationStatus": c.get("status", "Not yet recruiting"),
                    "locationCity": c.get("city", ""),
                    "locationCountry": c.get("county", ""),

                    "locationState": c.get("state", ""),
                    "locationZip": c.get("zip", ""),
                    "locationContactList": c.get("contactList", ""),
                    "locationIdentifier": c.get("identifier", ""),
                }
                for c in contacts.get("locations", [])],
        },
    }
    # Handling optional leadsponsor fields
    lead = collaborators.get("leadSponsor", {})
    identifier = lead.get("identifier")

    # convert an identification type
    info_type_list = data["identificationModule"]["secondaryIdInfoList"]
    if not info_type_list:
        data["identificationModule"].pop("secondaryIdInfoList", None)
    else:
        for item in info_type_list:
            if item.get("secondaryIdType") == "NIH":
                item["secondaryIdType"] = "U.S. National Institutes of Health (NIH) Grant/Contract Award Number"

    # Add optional sponsor identifier
    if identifier:
        data["leadSponsorIdentifier"] = {
            "leadSponsorIdentifierValue": identifier.get("value", ""),
            "leadSponsorIdentifierScheme": identifier.get("scheme", ""),
            "schemeURI": identifier.get("scheme", ""),
        }

    # Fix optional responsible party type for the sponsors
    rp = collaborators.get("responsibleParty", {})
    rpd = data["sponsorCollaboratorsModule"]["responsibleParty"]
    for k, v in [
        ("investigatorFullName", ["responsiblePartyInvestigatorFirstName", "responsiblePartyInvestigatorLastName"]),
        ("investigatorTitle", "responsiblePartyInvestigatorTitle")]:
        x = rp.get(k)
        if x: [rpd.update({i: x}) for i in (v if isinstance(v, list) else [v])]

    # Affiliation object handling
    aff = rp.get("investigatorAffiliation")
    if aff:
        rpd["responsiblePartyInvestigatorAffiliation"] = {
            "responsiblePartyInvestigatorAffiliationName": aff,
            **({"responsiblePartyInvestigatorAffiliationIdentifier": rp["investigatorAffiliationIdentifier"]}
               if "investigatorAffiliationIdentifier" in rp else {})
        }

    # Identifier object
    x = rp.get("investigatorIdentifier")
    if x:
        rpd["responsiblePartyInvestigatorIdentifier"] = [{
            "responsiblePartyInvestigatorIdentifierValue": x,
            "responsiblePartyInvestigatorIdentifierScheme": x,
            "schemeURI": x,
        }]

    status_module = data.setdefault("statusModule", {})
    completion_date_struct = status_module.setdefault("completionDateStruct", {})

    if completion_date_struct.get("completionDateType") == "Estimated":
        completion_date_struct["completionDateType"] = "Anticipated"

    # design enrollment info
    enrollment_info = data.setdefault("designModule", {}).setdefault("enrollmentInfo", {})
    if enrollment_info.get("enrollmentType") == "Estimated":
        enrollment_info["enrollmentType"] = "Anticipated"

    if data.get("statusModule", {}).get("completionDateStruct", {}).get("completionDateType") == "Estimated":
        data["statusModule"]["completionDateStruct"]["completionDateType"] = "Anticipated"

    if "whyStopped" in cds_data.get("statusModule", {}):
        data.setdefault("statusModule", {})["whyStopped"] = cds_data["statusModule"]["whyStopped"]

    if "keywordList" in cds_data.get("conditionsModule", {}):
        data.setdefault("conditionsModule", {})["keywords"] = cds_data["conditionsModule"]["keywordList"]

    for d in ["detailedDescription"]:
        if d in cds_data.get("descriptionModule", {}):
            data.setdefault("descriptionModule", {})[d] = cds_data["descriptionModule"][d]

    if "orgStudyIdLink" in identification.get("orgStudyIdInfo", {}):
        data["identificationModule"]["orgStudyIdInfo"]["orgStudyIdLink"] = identification["orgStudyIdInfo"][
            "orgStudyIdLink"]

    if "targetDuration" in design:
        data["designModule"]["targetDuration"] = design["targetDuration"]
    #Design assignment
    study_type = data["designModule"].get("studyType", "")

    if study_type == "Interventional":
        design_info = data.get("designModule", {}).get("designInfo", {})
        for key in ["designTimePerspectiveList", "designObservationalModelList"]:
            design_info.pop(key, None)

        bio_spec = data.get("designModule", {}).get("bioSpec", {})
        for key in ["bioSpecRetention", "bioSpecDescription"]:
            bio_spec.pop(key, None)

    if study_type == "Observational":
        design_info = data.get("designModule", {}).get("designInfo", {})
        for key in ["designAllocation", "designInterventionModel", "designPrimaryPurpose", "designMaskingInfo"]:
            design_info.pop(key, None)

    # add optional collab element
    collab_info = collaborators.get("collaboratorList", {})
    identifier = collab_info.get("collaboratorNameIdentifier")

    if (
            isinstance(identifier, dict)
            and "collaboratorNameIdentifierValue" in identifier
            and "collaboratorNameIdentifierScheme" in identifier
    ):
        data.setdefault("collaboratorModule", {}).setdefault("collaboratorList", {})[
            "collaboratorNameIdentifier"] = identifier

    # Eligibility
    for k in ["genderDescription", "studyPopulation", "samplingMethod"]:
        if k in eligibility:
            v = eligibility[k]
            if k == "samplingMethod":
                v = {"NON_PROBABILITY_SAMPLE": "Non-Probability Sample",
                     "PROBABILITY_SAMPLE": "Probability Sample"}.get(v, v)
            data["eligibilityModule"][k] = v

    # convert an overall officials type
    oo_list = data["contactsLocationsModule"]["overallOfficialList"]
    if not oo_list:
        data["contactsLocationsModule"].pop("overallOfficialList", None)
    else:
        role_map = {
            "PRINCIPAL_INVESTIGATOR": "Study Principal Investigator",
            "CHAIR": "Study Chair",
            "DIRECTOR": "Study Director"
        }

        for o in oo_list:
            raw_role = o.get("overallOfficialRole", "").upper()
            o["overallOfficialRole"] = role_map.get(raw_role, "Study Principal Investigator")

    cc_list = data["contactsLocationsModule"]["centralContactList"]
    if not cc_list:
        data["contactsLocationsModule"].pop("centralContactList", None)


    file_name = f"clinical_study_description_{ct_identifier}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved study description to: {file_name}")
    return data
