"""Main module."""

from abc import ABCMeta, abstractmethod
from git import Repo
import git
import importlib
import importlib.util
import sys

from typing import Union, Optional
import os

from mcstasscript.interface import functions

MCSTAS_PATH = os.environ["MCSTAS"]
my_configurator = functions.Configurator()
my_configurator.set_mcrun_path("/usr/bin/")
my_configurator.set_mcstas_path(MCSTAS_PATH)
print("McStas path: ", MCSTAS_PATH)


class repository:
    """Initiate the repository from an URL or local repo"""

    def __init__(
        self,
        url: str = "https://github.com/PaNOSC-ViNYL/instrument_database.git",
        local_repo: str = "/tmp/instrumentDBAPI/",
    ):
        """ """
        self.__url = url
        self.__local_repo = local_repo
        return

    def __repr__(self):
        s = "URL: " + self.__url
        s += "\n"
        s += "local_dir: " + self.__local_repo
        return s

    def __institutes_reldir(self) -> str:
        return "/mcstas/institutes/"

    def __institutes_absdir(self) -> str:
        return self.__local_repo + self.__institutes_reldir()

    def __instruments_absdir(self, institute: str) -> str:
        """Returns the instrument path relative to the institute directory"""
        return self.__institutes_absdir() + institute + "/instruments/"

    def __versions_absdir(self, institute: str, instrument: str) -> str:
        return self.__instruments_absdir(institute) + instrument + "/"

    def init(
        self,
        url: Optional[str] = None,
        local_repo: Optional[str] = None,
        branch: str = "shervin",
    ):
        if url != None:
            self.__url = url
        if local_repo != None:
            self.__local_repo = local_repo

        repo = git.Repo.clone_from(self.__url, self.__local_repo, branch=branch)
        assert not repo.bare
        sys.path.append(self.__institutes_absdir())

    def get_institutes(self) -> list:
        """Get the list of institutes"""
        basedir = self.__institutes_absdir()
        institutes = []
        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if os.path.isdir(dd):
                institutes.append(d)
        return institutes

    def ls_institutes(self) -> None:
        """Print the list of institutes"""
        for institute in self.get_institutes():
            print(" - " + institute)

    def ls_instruments(self, institute: Optional[str] = None):
        """Print the names of the available samples"""
        institutes = []
        if institute is None:
            institutes += self.get_institutes()
        else:
            institutes.append(institute)

        for inst in institutes:
            basedir = self.__instruments_absdir(inst)
            print("Available instruments for " + inst + ":")
            for d in os.listdir(basedir):
                dd = os.path.join(basedir, d)
                if os.path.isdir(dd):
                    print(" - ", inst + "/" + d)

        return

    def ls_versions(self, institute: str, instrument: str) -> None:
        """Print all implemented versions for the given instrument"""
        basedir = self.__versions_absdir(institute, instrument)
        print("Available versions for instrument " + instrument + ":")
        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if os.path.isdir(dd):
                print(" - ", instrument + "/" + d)

    def load(self, institute, instrument, version="HEAD", flavour="quick"):
        """Load an intrument from the repository"""

        sys.path.append(self.__local_repo + "/mcstas/institutes/" + institute)
        myinstrumentmodule = importlib.import_module(
            "instruments."
            + instrument
            + "."
            + version
            + "."
            + instrument
            + "_"
            + flavour
        )

        instrument_obj = myinstrumentmodule.def_instrument()
        return instrument_obj

    def dump_instrument(self, outfile):
        """Save the instrument in .py format"""

    def save_parameters(self, outfile):
        """Print the parameters of the instrument in .json format"""
