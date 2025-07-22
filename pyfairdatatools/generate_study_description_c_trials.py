import re
import requests
import json
import validate

def fetch_the_clinical_trials_data(identifier):
    if not (isinstance(identifier, str) and re.match(r"^NCT\d{8}$", identifier.strip())):
        return {"error": "Invalid identifier format."}, 400

    url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        return {
            "error": "No clinical study was found with the provided identifier",
            "status_code": 404,
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
    conditions = cds_data.get("conditionsModule", {}).get("conditions", [])
    design = cds_data.get("designModule", {})
    arms_int = cds_data.get("armsInterventionsModule", {})
    eligibility = cds_data.get("eligibilityModule", {})
    ipd = cds_data.get("ipdSharingStatementModule", {})
    contacts = cds_data.get("contactsLocationsModule", {})
    data = {
        "schema": "",
        "IdentificationModule": {
            "officialTitle": cds_data.get("identificationModule", {}).get("officialTitle", ""),
            "acronym": "",
            "OrgStudyIdInfo": {
                "OorgStudyId": cds_data.get("identificationModule", {}).get("orgStudyIdInfo", {}).get("id", ""),
                "OrgStudyIdType": cds_data.get("identificationModule", {}).get("orgStudyIdType", {}).get("info", ""),
                "OrgStudyIdLink": cds_data.get("identificationModule", {}).get("orgStudyIdLink", {}).get("link", "")
            },
            "SecondaryIdInfoList": [{
                "SecondaryId":s.get("id", ""),
                "SecondaryIdType":s.get("type", ""),
                "SecondaryIdLink":s.get("link", ""),
            } for s in cds_data.get("identificationModule", {}).get("secondaryIdInfos", [])],},
        "StatusModule": {
            "OverallStatus": status_map.get(raw_status, raw_status.replace("_", " ").title()),
            "StartDateStruct": cds_data.get("statusModule", {}).get("startDateStruct", {}).get("date", ""),
            "WhyStopped": cds_data.get("statusModule", {}).get("whyStopped", {}).get("date", ""),
            "CompletionDateStruct": cds_data.get("statusModule", {}).get("completionDateStruct", {}).get("date", ""),
        },
        "SponsorCollaboratorsModule": {
            "LeadSponsor": {"LeadSponsorName": cds_data.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "")},
            "ResponsiblePartyInvestigatorFirstName": cds_data.get("sponsorCollaboratorsModule", {}).get("responsibleParty", {}).get("investigatorFirstName", ""),
            "ResponsiblePartyInvestigatorLastName": cds_data.get("sponsorCollaboratorsModule", {}).get("responsibleParty", {}).get("investigatorLastName", ""),
            "ResponsiblePartyInvestigatorTitle": cds_data.get("sponsorCollaboratorsModule", {}).get("responsibleParty", {}).get("investigatorTitle", ""),
            "ResponsiblePartyInvestigatorIdentifier": cds_data.get("sponsorCollaboratorsModule", {}).get("responsibleParty", {}).get("investigatorIdentifier", ""),
            "ResponsiblePartyInvestigatorAffiliation": cds_data.get("sponsorCollaboratorsModule", {}).get("responsibleParty", {}).get("investigatorAffiliation", ""),
            "ResponsibleParty": cds_data.get("sponsorCollaboratorsModule", {}).get("responsibleParty", {}).get("type", ""),
            "CollaboratorList": [
                {
                    "CollaboratorName": c.get("name"),
                    "CollaboratorNameIdentifier": c.get("identifier"),
                }
                for c in cds_data.get("sponsorCollaboratorsModule", {}).get("collaborators", [])
            ]
        },
        "OversightModule": {
            "OversightHasDMC": cds_data.get("oversightModule", {}).get("oversightHasDmc", ""),
            "IsFDARegulatedDrug": cds_data.get("oversightModule", {}).get("isFdaRegulatedDrug", ""),
            "IsFDARegulatedDevice": cds_data.get("oversightModule", {}).get("isFdaRegulatedDevice", ""),
            "HumanSubjectReviewStatus": cds_data.get("oversightModule", {}).get("humanSubjectReviewStatus", "")
        },
        "DescriptionModule":
            {
                "BriefSummary": cds_data["descriptionModule"]["briefSummary"],
                "DetailedDescription": cds_data.get("descriptionModule", {}).get("detailedDescription", ""),

             },
        "ConditionsModule": {
            "ConditionList": [
                {
                    "ConditionName": cnd,
                    "ConditionIdentifier": {
                        "ConditionClassificationCode":"",
                        "ConditionScheme": "",
                        "SchemeURI": "",
                        "ConditionURI": "",
                    },
                 } for cnd in conditions],
            "KeywordList": [
                {"KeywordValue": kw}
                for kw in cds_data.get("conditionsModule", {}).get("keywords", [])
            ],
        },
        "DesignModule": {
            "StudyType": design.get("studyType", ""),
            "DesignInfo": design.get("designInfo", ""),
            "DesignTimePerspectiveList": "",
            "EnrollmentInfo": design.get("enrollmentInfo", ""),
            # TODO finish all design types
        },
        "armsInterventionsModule": {
            "ArmGroupList": [
                {"ArmGroupLabel": a.get("label", ""),
                 "ArmGroupType": a.get("type", ""),
                 "ArmGroupDescription": a.get("description", ""),
                 "ArmGroupInterventionList": a.get("interventionNames", [])}
                for a in arms_int.get("armGroups", {})],
            "InterventionList": [
                {
                 "InterventionType": i.get("type", ""),
                 "InterventionName": i.get("name", ""),
                 "InterventionDescription": i.get("description", ""),
                 "InterventionArmGroupLabelList": i.get("armGroupLabels", ""),
                 "InterventionOtherNameList": ""
                } for i in arms_int.get("interventions", {})
        ],},
        "EligibilityModule": {
            "Gender": eligibility.get("sex", ""),
            "GenderBased": eligibility.get("genderBased", ""),
            "GenderDescription": eligibility.get("genderDescription", ""),
            "MinimumAge": eligibility.get("minimumAge", ""),
            "MaximumAge": eligibility.get("maximumAge", ""),
            "HealthyVolunteers": eligibility.get("healthyVolunteers", ""),
            "EligibilityCriteria": eligibility.get("eligibilityCriteria", ""),
            "StudyPopulation": eligibility.get("studyPopulation", ""),
            "SamplingMethod": eligibility.get("samplingMethod", ""),
        },
        "ContactsLocationsModule": {
            "CentralContactList": [
                {
                    "CentralContactName": c.get("name", ""),
                    "CentralContactAffiliation": c.get("role", ""),
                    "CentralContactPhone": c.get("phone", ""),
                    "CentralContactPhoneExt": c.get("phoneExt", ""),
                    "CentralContactEMail": c.get("email", ""),
                 }
                for c in contacts.get("centralContacts", [])],

            "OverallOfficials": [
                {
                    "OverallOfficialName": c.get("name", ""),
                    "OverallOfficialAffiliation": c.get("affiliation", ""),
                    "OverallOfficialRole": c.get("role", ""),
                }
                for c in contacts.get("overallOfficials", [])],
            "LocationList": [
                {
                    "LocationFacility": c.get("facility", ""),
                    "LocationStatus": c.get("status", ""),
                    "LocationCity": c.get("city", ""),
                    "LocationState": c.get("state", ""),
                    "LocationZip": c.get("zip", ""),
                    "LocationCountry": c.get("county", ""),
                    "LocationContactList": c.get("contactList", ""),
                }
                for c in contacts.get("locations", [])],
        },
        "IPDSharingStatementModule": {
            "IPDSharing": ipd.get("ipdSharing", "").capitalize(),
            "IPDSharingDescription": ipd.get("ipdSharingDescription", ""),
            "IPDSharingInfoTypeList": ipd.get("ipdSharingInfoTypeList", ""),
            "IPDSharingTimeFrame": ipd.get("ipdSharingTimeFrame", ""),
            "IPDSharingAccessCriteria": ipd.get("ipdSharingAccessCriteria", ""),
            "IPDSharingURL": ipd.get("ipdSharingURL", ""),

        },
        "ReferencesModule": {
            "ReferenceList": [],
            "SeeAlsoLinkList": [],
            "AvailIPDList": [],
        },
    }

    if not validate.validate_dataset_description(data):
        print("Dataset description is invalid.")
        raise ValueError("Invalid input data")

    StudyType = data["DesignModule"]["StudyType"]

    if StudyType == "Interventional":
        if "TargetDuration" in data["DesignModule"]:
            del data["DesignModule"]["TargetDuration"]

        if "NumberGroupsCohorts" in data["DesignModule"]:
            del data["DesignModule"]["NumberGroupsCohorts"]

        if "BioSpec" in data["DesignModule"]:
            del data["DesignModule"]["BioSpec"]

        if "StudyPopulation" in data["EligibilityModule"]:
            del data["EligibilityModule"]["StudyPopulation"]

        if "SamplingMethod" in data["EligibilityModule"]:
            del data["EligibilityModule"]["SamplingMethod"]

    if StudyType == "Observational":
        if "PhaseList" in data["DesignModule"]:
            del data["DesignModule"]["PhaseList"]

        if "NumberArms" in data["DesignModule"]:
            del data["DesignModule"]["NumberArms"]

        ArmGroupList = data["ArmsInterventionsModule"]["ArmGroupList"]

        for ArmGroup in ArmGroupList:
            if "ArmGroupType" in ArmGroup:
                del ArmGroup["ArmGroupType"]

            if "ArmGroupInterventionList" in ArmGroup:
                del ArmGroup["ArmGroupInterventionList"]

        if "HealthyVolunteers" in data["EligibilityModule"]:
            del data["EligibilityModule"]["HealthyVolunteers"]
    #
    # if file_type == "json":
    #     try:
    #         with open(file_path, "w", encoding="utf8") as f:
    #             json.dump(data, f, indent=4)
    #     except Exception as error:
    #         print(error)
    #         raise error
    #
    # elif file_type == "xml":
    #     try:
    #         with open(file_path, "w", encoding="utf8") as f:
    #             xml = dicttoxml.dicttoxml(
    #                 data,
    #                 custom_root="study_description",
    #                 attr_type=False,
    #             )
    #
    #             dom = parseString(xml)  # type: ignore
    #             f.write(dom.toprettyxml())
    #
    #     except Exception as error:
    #         print(error)
    #         raise error
    #
    # elif file_type not in ["xlsx", "csv"]:
    #     print("File type is invalid.")
    #     raise ValueError("Invalid file type")
    file_name = f"clinical_study_description_{identifier}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Saved study description to: {file_name}")
    print(data, "kkk")
    return data


fetch_the_clinical_trials_data("NCT02901184")