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


def test_load(institute, instrument, version, flavour):
    instrument = repo.load("mcstas", "ILL", "D22", "HEAD", "quick", False)


def test_local():
    """Test for API design"""

    # init the local repo, making a git clone
    repo = API.Repository(local_repo="/opt/panosc/instrument_database")

    print()

    print("List of institutes:")
    assert type(repo.get_institutes()) is list
    repo.ls_institutes()

    assert type(repo.get_instruments("ILL")) is list
    repo.ls_instruments("ILL")

    assert type(repo.get_versions("ILL", "D22")) is list
    repo.ls_versions("ILL", "D22")

    assert type(repo.get_simulation_programs("ILL", "D22", "HEAD")) is list
    repo.ls_simulation_programs("ILL", "D22", "HEAD")

    assert type(repo.get_flavours("ILL", "D22", "HEAD", "mcstas")) is list
    repo.ls_flavours("ILL", "D22", "HEAD", "mcstas")

    instrument = repo.load("ILL", "D22", "HEAD", "mcstas", "quick", False)
    instrument = repo.load("ILL", "D22", dep=False)
    #    instrument = repo.load("simex", "test", "test")
    #    instrument.set_instrument_base_dir("/tmp/SPB_instrument/")
    # for calculator in instrument.calculators.values():
    #    print(calculator.name)
    #    print(calculator.parameters)
    # print("Calculators:")
    # print(instrument.calculators)
    # instrument.list_calculators()
    # instrument.list_parameters()
    #    print("Backengine output:")
    #    calculation_instrument.run()
    #    pmi.output.get_data()
    print("Parameters:")
    # print(instrument.parameters)
    print("Master parameters:")
    # print(instrument.master)
    instrument.run()


def test_design_defaults():
    """Test for API design"""

    # check init parameter types
    with pytest.raises(TypeError):
        repo = API.Repository(1.2)

    with pytest.raises(TypeError):
        repo = API.Repository(local_repo=5)

    # init the local repo, making a git clone
    repo = API.Repository()
    # how to avoid the repo = API.repository syntax? without the parentheses

    print()
    print(repo)

    # check the defaults
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

        print("List of institutes:")
        repo.ls_institutes()

        print()
        # raise exception
        with pytest.raises(ValueError):
            repo.ls_institutes()

        print("List of institutes:")
        repo.ls_institutes("mcstas")

        repo.ls_instruments("mcstas", "ILL")
        assert type(repo.get_institutes("mcstas")) is list
        instrument = repo.load("mcstas", "ILL", "D22", "HEAD", "quick")

        instrument = repo.load("simex", "test", "test")
        instrument.set_instrument_base_dir("/tmp/SPB_instrument/")
        for calculator in instrument.calculators.values():
            print(calculator.name)
            print(calculator.parameters)
        print("Calculators:")
        print(instrument.calculators)
        instrument.list_calculators()
        instrument.list_parameters()
        #    print("Backengine output:")
        #    calculation_instrument.run()
        #    pmi.output.get_data()
        print("Parameters:")
        print(instrument.parameters)
        print("Master parameters:")
        print(instrument.master)
        instrument.run()


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
