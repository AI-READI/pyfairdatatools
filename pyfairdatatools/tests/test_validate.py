"""Unit tests for pyfairdatatools.validate module."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501


from pyfairdatatools.validate import validate_dataset_description


class TestValidateDatasetDescription:
    def test_minimal_valid_dataset_description(self):
        data = {
            "Title": "Test Title",
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
        }

        output = validate_dataset_description(data)

        assert output is True

    def test_fail_missing_title(self):
        data = {
            "Identifier": "10.5281/zenodo.1234567",
            "IdentifierType": "DOI",
        }

        output = validate_dataset_description(data)

        assert output is False
