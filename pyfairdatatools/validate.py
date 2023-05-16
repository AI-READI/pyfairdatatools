import json
from os import path

from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
        "scores": {"type": "array", "items": {"type": "number"}, "minItems": 1},
    },
    "required": ["name"],
}

validate(instance={"name": "John", "age": 30, "scores": [70, 90]}, schema=schema)
# No error, the JSON is valid.

validate(instance={"name": "John", "age": 30, "scores": ["B", "A"]}, schema=schema)
# ValidationError: 'B' is not of type 'number'.

validate(instance={"name": "John", "age": 30, "scores": []}, schema=schema)
# No error, the JSON is valid.


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
        path.join(path.dirname(__file__), "schemas", "dataset_description_schema.json"),
        encoding="utf-8",
    ) as f:
        schema = json.load(f)

    try:
        validate(instance=data, schema=schema)
        return True
    except Exception as e:
        print(e)
        return False
