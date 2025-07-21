import re
import requests


def fetch_the_clinical_trials_data(identifier):
    if isinstance(identifier, str) and re.match( r"^NCT\d{8}$", identifier.strip()):
        url = f"https://classic.clinicaltrials.gov/api/v2/studies/{identifier}"
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return {
                "error": "No clinical study was found with the provided identifier",
                "status_code": 404,
                "message": f"No study found for identifier '{identifier}'.",
            }, 404
    clinical_trials_data = response.json()["protocolSection"]
    # print(clinical_trials_data)
    data = {
        "schema": "https://schema.aireadi.org/v0.1.0/study_description.json",
        "identificationModule": {
            "officialTitle": "AI Ready and Exploratory Atlas for Diabetes Insights",
            "acronym": "AI-READI",
            "orgStudyIdInfo": {},
            "secondaryIdInfoList": []
        },
        "statusModule": {
            "overalStatus": clinical_trials_data["statusModule"]["overallStatus"],
            "startDate": clinical_trials_data["statusModule"]["startDateStruct"]["date"],
        },
        "sponsorCollaboratorsModule": {
            "collaboratorList": [{
                "collaboratorName": c["name"],
                "collaboratorNameIdentifier": c["identifier"] if "identifier" in c else None,
            } for c in clinical_trials_data["sponsorCollaboratorsModule"]["collaborators"]],
        },
        # "oversightModule": clinical_trials_data["oversightModule"],
        # "descriptionModule": clinical_trials_data["descriptionModule"],
        # "conditionsModule": clinical_trials_data["conditionsModule"],
        # "designModule": clinical_trials_data["designModule"],
        # "armsInterventionsModule": clinical_trials_data["armsInterventionsModule"],
        # "eligibilityModule": clinical_trials_data["eligibilityModule"],
        "contactsLocationsModule": clinical_trials_data["contactsLocationsModule"],
}
    print(data, "jhjh")


fetch_the_clinical_trials_data("NCT02901184")
