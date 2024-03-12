import json
from os import makedirs, path
from string import Template
from typing import Any, Dict, List
from xml.dom.minidom import parseString

import dicttoxml
import yaml

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
