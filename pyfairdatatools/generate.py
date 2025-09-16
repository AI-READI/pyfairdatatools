import json
from os import makedirs, path
from string import Template
from typing import Any, Dict, List
from xml.dom.minidom import parseString
import re
import dicttoxml
import yaml
import requests
from . import utils, validate


def generate_dataset_description(data, file_path, file_type):
    """Generate a dataset description file.

    Args:
        data (dict): The dataset description to generate
        file_path (str): The path to the folder to save the dataset description in
        file_type (str): The type of file to save the dataset description as
    Returns:
        A dataset description file
    """
    ALLOWED_FILE_TYPES = ["json", "xml"]

    try:
        if file_type not in ALLOWED_FILE_TYPES:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

        if not utils.validate_file_path(file_path, writable=True):
            print("File path is invalid.")
            raise ValueError("Invalid file path")

        if not validate.validate_dataset_description(data):
            print("Dataset description is invalid.")
            raise ValueError("Invalid input data")

        if not path.exists(path.dirname(file_path)):
            makedirs(path.dirname(file_path))

        relatedIdentifier = data["relatedIdentifier"]

        for identifier in relatedIdentifier:
            relation_type = identifier["relationType"]

            if relation_type not in ["HasMetadata", "IsMetadataFor"]:
                if "relatedMetadataScheme" in identifier:
                    del identifier["relatedMetadataScheme"]

                if "schemeURI" in identifier:
                    del identifier["schemeURI"]

                if "schemeType" in identifier:
                    del identifier["schemeType"]

        if file_type == "json":
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    json.dump(data, f, indent=4)
            except Exception as error:
                print(error)
                raise error

        elif file_type == "xml":
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    xml = dicttoxml.dicttoxml(
                        data,
                        custom_root="dataset_description",
                        attr_type=False,
                    )

                    dom = parseString(xml)  # type: ignore
                    f.write(dom.toprettyxml())

            except Exception as error:
                print(error)
                raise error

        elif file_type not in ["xlsx", "csv"]:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

    except ValueError as error:
        print(error)
        raise ValueError("Invalid input") from error
    except Exception as error:
        print(error)
        raise error


def generate_study_description(data, file_path, file_type):
    """Generate a dataset description file.

    Args:
        data (dict): The dataset description to generate
        file_path (str): The path to the folder to save the dataset description in
        file_type (str): The type of file to save the dataset description as
    Returns:
        A dataset description file
    """
    ALLOWED_FILE_TYPES = ["json", "xml"]

    try:
        if file_type not in ALLOWED_FILE_TYPES:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

        if not utils.validate_file_path(file_path, writable=True):
            print("File path is invalid.")
            raise ValueError("Invalid file path")

        if not validate.validate_study_description(data):
            print("Study description is invalid.")
            raise ValueError("Invalid input data")

        if not path.exists(path.dirname(file_path)):
            makedirs(path.dirname(file_path))

        studyType = data["designModule"]["studyType"]

        if studyType == "Interventional":
            if "targetDuration" in data["designModule"]:
                del data["designModule"]["targetDuration"]

            if "numberGroupsCohorts" in data["designModule"]:
                del data["designModule"]["numberGroupsCohorts"]

            if "bioSpec" in data["designModule"]:
                del data["designModule"]["bioSpec"]

            if "studyPopulation" in data["eligibilityModule"]:
                del data["eligibilityModule"]["studyPopulation"]

            if "samplingMethod" in data["eligibilityModule"]:
                del data["eligibilityModule"]["SamplingMethod"]

        elif studyType == "Observational":
            if "phaseList" in data["designModule"]:
                del data["designModule"]["phaseList"]

            if "numberArms" in data["designModule"]:
                del data["designModule"]["numberArms"]

            if "isPatientRegistry" in data["designModule"]:
                del data["designModule"]["isPatientRegistry"]

        if file_type == "json":
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    json.dump(data, f, indent=4)
            except Exception as error:
                print(error)
                raise error

        elif file_type == "xml":
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    xml = dicttoxml.dicttoxml(
                        data,
                        custom_root="study_description",
                        attr_type=False,
                    )

                    dom = parseString(xml)  # type: ignore
                    f.write(dom.toprettyxml())

            except Exception as error:
                print(error)
                raise error

        elif file_type not in ["xlsx", "csv"]:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

    except ValueError as error:
        print(error)
        raise ValueError("Invalid input") from error
    except Exception as error:
        print(error)
        raise error


def generate_study_description_from_clinical_trials(ct_identifier):
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
                    "overallOfficialFirstName": c.get("name", "").split()[0] if c.get("name") else "",
                    "overallOfficialLastName": " ".join(c.get("name", "").split()[1:]) if c.get("name") else "",
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
    # Split full name
    name = rp.get("investigatorFullName", "").strip().split()
    if name:
        rpd["responsiblePartyInvestigatorFirstName"] = name[0]
        rpd["responsiblePartyInvestigatorLastName"] = " ".join(name[1:])
    # Title
    if rp.get("investigatorTitle"):
        rpd["responsiblePartyInvestigatorTitle"] = rp["investigatorTitle"]

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


def generate_readme(data, file_path, file_type):
    """Generate a readme file.

    Args:
        data (dict): The readme to generate
        file_path (str): The path to the folder to save the readme in
        file_type (str): The type of file to save the readme as
    Returns:
        A readme file
    """
    ALLOWED_FILE_TYPES = ["txt", "md"]

    try:
        if file_type not in ALLOWED_FILE_TYPES:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

        if not utils.validate_file_path(file_path, writable=True):
            print("File path is invalid.")
            raise ValueError("Invalid file path")

        if not validate.validate_readme(data):
            print("Readme is invalid.")
            raise ValueError("Invalid input data")

        if file_type in ["txt", "md"]:
            with open(
                path.join(path.dirname(__file__), "templates", "readme.mdtxt.template"),
                encoding="utf-8",
            ) as template_file:
                try:
                    with open(file_path, "w", encoding="utf8") as output_file:
                        template = Template(template_file.read())

                        substitutions = {
                            "title": data.get("Title"),
                            "identifier": data.get("Identifier") or "",
                            "version": data.get("Version") or "",
                            "publication_date": data.get("PublicationDate") or "",
                            "about": data.get("About") or "",
                            "dataset_description": data.get("DatasetDescription") or "",
                            "dataset_access": data.get("DatasetAccess") or "",
                            "standards_followed": data.get("StandardsFollowed") or "",
                            "resources": data.get("Resources") or "",
                            "license": data.get("License") or "",
                            "how_to_cite": data.get("HowToCite") or "",
                            "acknowledgement": data.get("Acknowledgement") or "",
                        }

                        output_file.write(template.substitute(substitutions))

                except Exception as error:
                    print(error)
                    raise error

        else:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

    except ValueError as error:
        print(error)
        raise ValueError("Invalid input") from error
    except Exception as error:
        print(error)
        raise error


def generate_changelog_file(data, file_path, file_type):
    """Generate a changelog file.

    Args:
        data (str): The changelog to generate
        file_path (str): The path to the folder to save the changelog in
        file_type (str): The type of file to save the changelog as
    Returns:
        A changelog file
    """
    ALLOWED_FILE_TYPES = ["txt", "md"]

    if file_type not in ALLOWED_FILE_TYPES:
        print("File type is invalid.")
        raise ValueError("Invalid file type")

    if not utils.validate_file_path(file_path, writable=True):
        print("File path is invalid.")
        raise ValueError("Invalid file path")

    if file_type in ["txt", "md"]:
        try:
            with open(file_path, "w", encoding="utf8") as f:
                f.write(data)

        except Exception as error:
            print(error)
            raise error


def generate_license_file(
    file_path,
    file_type,
    identifier="",
    data="",
):
    # sourcery skip: low-code-quality
    """Generate a license file.

    Args:
        identifier (str): The identifier of the license
        data (str): License text if the identifier is not provided (takes precedence
            over identifier)
        file_path (str): The path to the folder to save the license in
        file_type (str): The type of file to save the license as
    Returns:
        A license file
    """
    ALLOWED_FILE_TYPES = ["txt", "md"]

    if identifier == "" and data == "":
        print("Identifier or data must be provided.")
        raise ValueError("Invalid input")

    if not utils.validate_file_path(file_path, writable=True):
        print("File path is invalid.")
        raise ValueError("Invalid file path")

    if file_type not in ALLOWED_FILE_TYPES:
        print("File type is invalid.")
        raise ValueError("Invalid file type")

    if file_type in ["txt", "md"]:
        # if data is provided, use that
        if data != "":
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(data)

            except Exception as error:
                print(error)
                raise error
        # if data is not provided, use identifier
        else:
            with open(
                path.join(path.dirname(__file__), "assets", "licenses.json"),
                encoding="utf-8",
            ) as f:
                list_of_licenses = json.load(f)["licenses"]

                license_text = ""
                for item in list_of_licenses:
                    if "licenseId" in item and item["licenseId"] == identifier:
                        if "detailsUrl" in item:
                            try:
                                response = utils.requestJSON(item["detailsUrl"])

                                if "licenseText" in response:
                                    license_text = response["licenseText"]
                                else:
                                    print("Could not get text for license.")
                                    raise NotImplementedError(
                                        "License text not available"
                                    )

                                with open(file_path, "w", encoding="utf8") as f:
                                    f.write(license_text)
                                    print("License file generated.")

                                return

                            except Exception as error:
                                print(error)
                                raise error

                        else:
                            print("Could not get text for license.")
                            raise NotImplementedError("License text not available")


def generate_datatype_file(data, file_path, file_type):
    """Generate a datatype file.

    Args:
        data (list): The list of datatypes to generate
        file_path (str): The path to the folder to save the datatype in
        file_type (str): The type of file to save the datatype as
    Returns:
        A datatype dictionary yaml file
    """
    ALLOWED_FILE_TYPES = ["yaml"]

    try:
        if file_type not in ALLOWED_FILE_TYPES:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

        if not utils.validate_file_path(file_path, writable=True):
            print("File path is invalid.")
            raise ValueError("Invalid file path")

        if not validate.validate_datatype_dictionary(data):
            print("Datatype is invalid.")
            raise ValueError("Invalid input data")

        if not path.exists(path.dirname(file_path)):
            makedirs(path.dirname(file_path))

        # Create the datatype file before generating the datatype description file
        datatype_data: Dict[str, List[Dict[str, Any]]] = {"datatype_dictionary": []}

        with open(
            path.join(path.dirname(__file__), "assets", "datatype_dictionary.yaml"),
            encoding="utf-8",
        ) as f:
            schema = yaml.safe_load(f)

        for entry in data:
            for item in schema["datatype_dictionary"]:
                if entry == item["code_name"] or entry in item["aliases"]:
                    print(item)
                    new_item = {}
                    if "code_name" in item:
                        new_item["code_name"] = item["code_name"]
                    if "datatype_description" in item:
                        new_item["datatype_description"] = item["datatype_description"]
                    if "aliases" in item:
                        new_item["aliases"] = item["aliases"]
                    if "related_terms" in item:
                        new_item["related_terms"] = item["related_terms"]
                    if "related_standards" in item:
                        new_item["related_standards"] = item["related_standards"]
                    datatype_data["datatype_dictionary"].append(new_item)

        if file_type == "yaml":
            try:
                with open(file_path, "w", encoding="utf8") as f:
                    yaml.dump(datatype_data, f, indent=4, sort_keys=False)
            except Exception as error:
                print(error)
                raise error

        elif file_type not in ["yaml"]:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

    except ValueError as error:
        print(error)
        raise ValueError("Invalid input") from error
    except Exception as error:
        print(error)
        raise error
