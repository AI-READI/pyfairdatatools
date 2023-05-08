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
