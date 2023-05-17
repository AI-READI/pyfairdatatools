import json
from os import path

from jsonschema import validate


def validate_dataset_description(data):
    """Validate a dataset description against the schema.

    Args:
        data (dict): The dataset description to validate
    Returns:
        bool: True if the dataset description is valid, False otherwise
    """
    schema = {}

    # Import the schema from the schemas folder
    with open(
        path.join(path.dirname(__file__), "schemas", "dataset_description.schema.json"),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        return True
    except Exception as e:
        print(e)
        return False
