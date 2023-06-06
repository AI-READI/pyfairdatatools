"""Sample integration test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned

import pytest
from click.testing import CliRunner
from expecter import expect

from pyfairdatatools.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def describe_cli():
    def describe_conversion():
        def returns_none(runner):
            result = runner.invoke(main)

            expect(result.exit_code) == 0
            expect(result.output) is None

        # def when_invalid(runner):
        #     result = runner.invoke(main, ["foobar"])

        #     expect(result.exit_code) == 0
        #     expect(result.output) == ""
