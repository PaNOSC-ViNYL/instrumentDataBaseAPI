""" 
This is the main API for getting instrument descriptions from the instrument database 
"""

from abc import ABCMeta, abstractmethod
from git import Repo
import git
import importlib
import importlib.util
import sys
import os

from typing import Union, Optional

from libpyvinyl import Instrument


class Repository:
    """
    :class Repository:
    The API to interact with the instrument database is offered by the Repository class
    """

    def __init__(
        self,
        url: str = "https://github.com/PaNOSC-ViNYL/instrument_database.git",
        local_repo: str = "/dev/shm/instrumentDBAPI/",
    ) -> None:
        """
        Initiate the repository from an URL or local repo

        :param url: URL of the git repository storing the instrument database
        :param local_repo: local directory where the instrument database is copied to
        """
        self.__url = url
        self.__local_repo = local_repo
        return

    def init(
        self,
        url: str = "https://github.com/PaNOSC-ViNYL/instrument_database.git",
        local_repo: str = "/tmp/instrumentDBAPI/",
        branch: str = "shervin",
    ):
        """
        Initiate the repository from an URL or local repo

        :param url: URL of the git repository storing the instrument database
        :param local_repo: local directory where the instrument database is copied to
        :param branch: branch in the repository to checkout
        """
        self.__url = url
        self.__local_repo = local_repo

        repo = git.Repo.clone_from(self.__url, self.__local_repo, branch=branch)
        assert not repo.bare
        sys.path.append(self.__institutes_absdir())

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

    def get_institutes(self) -> list:
        """
        Get the list of institutes
        """
        basedir = self.__institutes_absdir()
        institutes = []
        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if os.path.isdir(dd):
                institutes.append(d)
        return institutes

    def ls_institutes(self) -> None:
        """
        Print the list of institutes
        """
        for institute in self.get_institutes():
            print(" - " + institute)

    def ls_instruments(self, institute: Optional[str] = None) -> None:
        """
        Print the names of the available instruments

        :param institute: name of the institute as returned by :func:`~instrumentdatabaseapi.instrumentdatabaseapi.Repository.ls_institutes`
        """
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

    def ls_versions(self, institute: str, instrument: str) -> None:
        """
        Print all implemented versions for the given instrument

        :param institute: name of the institute as returned by :func:`~instrumentdatabaseapi.instrumentdatabaseapi.Repository.ls_institutes`
        :param instrument: name of the instrument as returned by :func:`~instrumentdatabaseapi.instrumentdatabaseapi.Repository.ls_instruments`

        Version formats:
          - **HEAD** is the most recent up-to-date version of the instrument and it is still currently in use
          - **YYYY/MM/DD** last day of validity of the instrument description. After that date, the instrument have been either modified (so more recent version should be available) or it not in service anymore
        """

        basedir = self.__versions_absdir(institute, instrument)
        print("Available versions for instrument " + instrument + ":")
        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if os.path.isdir(dd):
                print(" - ", instrument + "/" + d)

    def load(
        self,
        institute: str,
        instrument: str,
        version: str = "HEAD",
        flavour: str = "quick",
    ) -> Instrument:
        """
        Load an intrument from the repository

        :param institute: name of the institute
        :param instrument: name of the instrument
        :param version: version name
        :param flavour: optional string that might identify two alternative implementations of the same instrument with the same version

        :return: the instrument object
        :raise: NotImplementedError if the instrument module does not provide a def_instrument method
        """

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
        if not hasattr(myinstrumentmodule, "def_instrument") or not callable(
            myinstrumentmodule.def_instrument
        ):
            raise NotImplementedError(
                "Instrument description script does not implement a def_instrument() method"
            )

        instrument_obj = myinstrumentmodule.def_instrument()
        return instrument_obj


#    def dump_instrument(self, outfile):
#        """Save the instrument in .py format"""

#    def save_parameters(self, outfile):
#        """Print the parameters of the instrument in .json format"""
