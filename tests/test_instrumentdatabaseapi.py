#!/usr/bin/env python

"""Tests for `instrumentdatabaseapi` package."""

import pytest

from click.testing import CliRunner

from instrumentdatabaseapi import instrumentdatabaseapi as API
from instrumentdatabaseapi import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "instrumentdatabaseapi.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


def test_design_defaults():
    """Test for API design"""

    # init the local repo, making a git clone
    API.init()
    API.ls_instruments()  # print the list of instruments available
    instrument_name = "ILL/D22"
    API.ls_versions(instrument_name)

    myinstrument = API.load_instrument("ILL/D22", "HEAD")
    myinstrument.print_parameters()

    myinstrument["wavelength"] = pint.Unit("5", "angstrom")

    mysample = ""  # sampleAPI.load_sample()
    # sampleAPI.ls_samples()

    myinstrument.set_sample()  # ?
    # or
    API.set_sample(myinstrument, mysample)  # ?

    mydate = myinstrument.run()
