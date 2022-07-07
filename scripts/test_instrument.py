#!/usr/bin/env python

"""Tests for `instrumentdatabaseapi` package."""

_VALIDATION_SEED_ = 654321

from instrumentdatabaseapi import instrumentdatabaseapi as API

from mcstasscript.interface import functions
import os
import sys
import pytest
import numpy as np

MCSTAS_PATH = os.environ["MCSTAS"]
my_configurator = functions.Configurator()
#
my_configurator.set_mcstas_path(MCSTAS_PATH)
my_configurator.set_mcrun_path(MCSTAS_PATH + "/bin/")
print("McStas path: ", MCSTAS_PATH)


simulation_program = ""
flavour = ""
version = "HEAD"

if len(sys.argv) < 5:
    raise RuntimeError("Wrong number of command line inputs.")

institute = sys.argv[1]
instrument = sys.argv[2]
version = sys.argv[3]
simulation_program = sys.argv[4]
if len(sys.argv) > 5:
    flavour = sys.argv[5]


# init the local repo, making a git clone
repo = API.Repository(local_repo=".")

print("List of institutes:")
repo.ls_institutes()

repo.ls_instruments(institute)

repo.ls_versions(institute, instrument)

repo.ls_simulation_programs(institute, instrument, version)

print(f"List of flavours for {institute}/{instrument}/{version}/{simulation_program}")
repo.ls_flavours(institute, instrument, version, simulation_program)

myinstrument = repo.load(
    institute, instrument, version, simulation_program, flavour, False
)
validation_dir = repo.validation_dir(
    institute, instrument, version, simulation_program, flavour
)
myinstrument.set_instrument_base_dir("/tmp/validation/")
for calc in myinstrument.calculators:
    myinstrument.calculators[calc].settings(seed=_VALIDATION_SEED_)
# instrument.calculators["D22_quick"].output_path = "ciao"
# instrument.calculators["D22_quick"].base_dir = "/ciao"
# print(f"calculator_base_dir: {instrument.calculators['D22_quick'].calculator_base_dir}")

# print(f"instrument_base_dir: {instrument.calculators['D22_quick'].instrument_base_dir}")
# print(f"base_dir: {instrument.calculators['D22_quick'].base_dir}")

print()
print("Master parameters:")
print(myinstrument.master)
for par in myinstrument.master:
    print(par)

for par in myinstrument.master:
    print(par)
myinstrument.run()
output = myinstrument.output

if simulation_program == "mcstas":
    last_calc = list(myinstrument.calculators.values())[-1]

    detector = output[last_calc.name + "_data"].get_data()["data"][-1]
    # from mcstasscript.data.McStasDataFormat import McStasFormat
    # output["simulation_data"].write("/tmp/mysim.sim", McStasFormat)
    from mcstasscript.data.pyvinylData import pyvinylMcStasData
    from mcstasscript.data.McStasDataFormat import McStasFormat

    print(f"Validation directory: {validation_dir}")
    val_data = pyvinylMcStasData.from_file(validation_dir, McStasFormat, "validation")

    I_val = val_data.get_data()["data"][-1]
    assert np.array_equal(detector.Intensity, I_val.Intensity)
    assert np.array_equal(detector.Error, I_val.Error)
    assert np.array_equal(detector.Ncount, I_val.Ncount)

    print(I_val, detector)
# instrument.backengine()
