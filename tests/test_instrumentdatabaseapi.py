#!/usr/bin/env python

"""Tests for `instrumentdatabaseapi` package."""

import pytest
import tempfile

# from click.testing import CliRunner

from instrumentdatabaseapi import instrumentdatabaseapi as API

# from instrumentdatabaseapi import cli


from mcstasscript.interface import functions
import os

MCSTAS_PATH = os.environ["MCSTAS"]
my_configurator = functions.Configurator()
my_configurator.set_mcrun_path("/usr/bin/")
my_configurator.set_mcstas_path(MCSTAS_PATH)
print("McStas path: ", MCSTAS_PATH)


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


def test_local():
    """Test for API design"""

    # init the local repo, making a git clone
    repo = API.Repository(local_repo="/opt/panosc/instrument_database")
    print("Simulation programs:")
    repo.ls_simulation_programs()

    print()
    # raise exception
    with pytest.raises(ValueError):
        repo.ls_institutes("mcstass")

    print("List of institutes:")
    repo.ls_institutes("mcstas")

    repo.ls_instruments("mcstas", "ILL")
    assert type(repo.get_institutes("mcstas")) is list
    instrument = repo.load("mcstas", "ILL", "D22", "HEAD", "quick")

    instrument = repo.load("simex", "test", "test")


def test_design_defaults():
    """Test for API design"""

    # init the local repo, making a git clone
    repo = API.Repository()
    # how to avoid the repo = API.repository syntax? without the parentheses

    print()
    print(repo)
    assert (
        repo._Repository__url
        == "https://github.com/PaNOSC-ViNYL/instrument_database.git"
    )
    assert repo._Repository__local_repo == "/dev/shm/instrumentDBAPI/"
    # with tempfile.TemporaryDirectory() as temp_dir:
    with "/opt/panosc/instrument_database" as temp_dir:
        print("Testing with temporary directory")
        repo.init(local_repo=temp_dir)
        assert repo._Repository__local_repo == temp_dir

        print("Simulation programs:")
        repo.ls_simulation_programs()

        print()
        # raise exception
        with pytest.raises(ValueError):
            repo.ls_institutes("mcstass")

        print("List of institutes:")
        repo.ls_institutes("mcstas")

        repo.ls_instruments("mcstas", "ILL")
        assert type(repo.get_institutes("mcstas")) is list
        instrument = repo.load("mcstas", "ILL", "D22", "HEAD", "quick")

        instrument = repo.load("simex", "test", "test")


# api.ls_instruments()  # print the list of instruments available
# instrument_name = "ILL/D22"
# api.ls_versions(instrument_name)

# myinstrument = api.load_instrument("ILL/D22", "HEAD")
# myinstrument.print_parameters()

# myinstrument["wavelength"] = pint.Unit("5", "angstrom")

# mysample = ""  # sampleAPI.load_sample()
# # sampleAPI.ls_samples()

# myinstrument.set_sample()  # ?
# # or
# api.set_sample(myinstrument, mysample)  # ?

# mydate = myinstrument.run()
