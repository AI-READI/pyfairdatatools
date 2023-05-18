import json
from xml.dom.minidom import parseString

import dicttoxml

from . import validate


def generate_dataset_description(data, folder_path, file_type):
    """Generate a dataset description file.

    Args:
        data (dict): The dataset description to generate
        folder_path (str): The path to the folder to save the dataset description in
        file_type (str): The type of file to save the dataset description as
    Returns:
        A dataset description file
    """
    ALLOWED_FILE_TYPES = ["json", "xml", "xlsx", "csv"]

    try:
        if file_type not in ALLOWED_FILE_TYPES:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

        if not validate.validate_dataset_description(data):
            print("Dataset description is invalid.")
            raise ValueError("Invalid input data")

        if file_type == "json":
            try:
                with open(folder_path, "w", encoding="utf8") as f:
                    json.dump(data, f, indent=4)
            except Exception as error:
                print(error)
                raise error

        elif file_type == "xml":
            try:
                with open(folder_path, "w", encoding="utf8") as f:
                    xml = dicttoxml.dicttoxml(
                        data,
                        custom_root="dataset_description",
                        attr_type=False,
                        item_func=lambda x: "variable",
                    ).decode("utf-8")
                    dom = parseString(xml)
                    f.write(dom.toprettyxml())

            except Exception as error:
                print(error)
                raise error

        elif file_type == "xlsx":
            pass
        elif file_type == "csv":
            pass
        else:
            print("File type is invalid.")
            raise ValueError("Invalid file type")

    except ValueError as error:
        print(error)
        raise ValueError("Invalid input") from error
    except Exception as error:
        print(error)
        raise error
