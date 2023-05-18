"""Unit tests for pyfairdatatools.generate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

import json
from os import path

from pyfairdatatools.generate import generate_dataset_description


class TestGenerateDatasetDescription:
    def test_minimal_valid_dataset_description(self, tmp_path):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
        }

        file = tmp_path / "dataset_description.json"
        file_type = "json"

        generate_dataset_description(data, file, file_type)

        assert path.exists(file) is True

        with open(file, "r", encoding="utf8") as f:
            imported_data = json.load(f)

        assert imported_data == data

        file = tmp_path / "dataset_description.xml"
        file_type = "xml"

        generate_dataset_description(data, file, file_type)
