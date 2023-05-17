"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison # noqa: E501

import pytest

from pyfairdatatools.utils import feet_to_meters


class TestDescribeFeetToMeters:
    def test_when_integer(self):
        converted = feet_to_meters(42)
        assert converted == 12.80165

    def test_when_string(self):
        with pytest.raises(ValueError):
            feet_to_meters("hello")
