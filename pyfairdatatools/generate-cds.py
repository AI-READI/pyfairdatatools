import json
from os import makedirs, path
from string import Template
from xml.dom.minidom import parseString

import dicttoxml

from . import utils, validate



def generate_study_description_from_clinical_trials(data, file_path, file_type):
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

        # if not utils.validate_file_path(file_path, writable=True):
        #     print("File path is invalid.")
        #     raise ValueError("Invalid file path")

        # if not validate.validate_study_description(data):
        #     print("Study description is invalid.")
        #     raise ValueError("Invalid input data")

        if not path.exists(path.dirname(file_path)):
            makedirs(path.dirname(file_path))

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

