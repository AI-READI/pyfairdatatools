"""Pulls A JSON schema from a URL and saves it to a filepath"""

import json
import requests

schema_paths = [
    {
        "sourceURL": "https://raw.githubusercontent.com/AI-READI/cds-specification/main/docs/public/schemas/dataset_description.schema.json",  # noqa: E501 # pylint: disable=line-too-long
        "destinationFileName": "dataset_description.schema.json",
    },
    {
        "sourceURL": "https://raw.githubusercontent.com/AI-READI/cds-specification/study_description_schema/docs/public/schemas/study_description.schema.json",  # noqa: E501 # pylint: disable=line-too-long
        "destinationFileName": "study_description.schema.json",
    },
    {
        "sourceURL": "https://raw.githubusercontent.com/AI-READI/datatype-dictionary/main/datatype_dictionary.schema.json",  # noqa: E501 # pylint: disable=line-too-long
        "destinationFileName": "datatype_dictionary.schema.json",
    },
]


def main():
    """CLI entrypoint."""

    folder_path = "pyfairdatatools/schemas/"

    for schema_path in schema_paths:
        file_path = folder_path + schema_path["destinationFileName"]

        print(f"Pulling {schema_path['sourceURL']} to {file_path}")

        # Pull the schema from the URL
        response = requests.get(
            schema_path["sourceURL"], allow_redirects=True, timeout=10
        )
        schema = response.json()

        # Write the schema to a file
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(schema, file, indent=2)

    return


if __name__ == "__main__":  # pragma: no cover
    main()  # pylint: disable=no-value-for-parameter
