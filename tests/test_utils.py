"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

# import os

import pytest

from pyfairdatatools.utils import feet_to_meters, requestJSON, validate_file_path


class TestDescribeFeetToMeters:
    def test_when_integer(self):
        converted = feet_to_meters(42)
        assert converted == 12.80165

    def test_when_string(self):
        with pytest.raises(ValueError):
            feet_to_meters("hello")


class TestRequestJSON:
    def test_when_valid_url(self):
        response = requestJSON("https://dummyjson.com/test")
        assert response["status"] == "ok"

    def test_when_invalid_url(self):
        with pytest.raises(Exception):
            requestJSON("https://dummyjson.com/invalid")


class TestValidateFilePath:
    def test_when_valid_path(self):
        assert validate_file_path("pyfairdatatools/README.md") == True

    def test_when_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            validate_file_path("pyfairdatatools/invalid.md", preexisting_file=True)

    # def test_when_invalid_writable(self):
    #     with pytest.raises(PermissionError):
    #         root_file_path = os.path.join(os.path.abspath(os.sep), "README.md")
    #         print(root_file_path)
    #         validate_file_path(root_file_path, writable=True)
