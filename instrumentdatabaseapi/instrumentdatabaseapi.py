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
import re

import subprocess  # for using pip

from typing import Union, Optional, List

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
                    URL can be anything git can manage
                    git will raise an error in case URL is not accepted
        :param local_repo: local directory where the instrument database is copied to
        """
        if not isinstance(url, str):
            raise TypeError("URL should be a string")
        if not isinstance(local_repo, str):
            raise TypeError("The local repo should be a string")

        self.__url = url
        self.__local_repo = local_repo + "/"
        sys.path.append(self.__local_repo)

        return

    def init(
        self,
        url: str = "https://github.com/PaNOSC-ViNYL/instrument_database.git",
        local_repo: str = "/tmp/instrumentDBAPI/",
        branch: str = "shervin",
    ) -> None:
        """
        Initiate the repository from an URL or local repo

        :param url: URL of the git repository storing the instrument database
        :param local_repo: local directory where the instrument database is copied to
        :param branch: branch in the repository to checkout
        """
        self.__url = url

        sys.path.remove(self.__local_repo)
        self.__local_repo = local_repo
        sys.path.append(self.__local_repo)

        repo = git.Repo.clone_from(self.__url, self.__local_repo, branch=branch)
        ## add the --depth option

        assert not repo.bare

    def __repr__(self) -> str:
        """
        Allowes to get basic information about the repository
        """
        s = "URL: " + self.__url
        s += "\n"
        s += "local_dir: " + self.__local_repo
        return s

    def __is_real_dir(self, abs_dir: str) -> bool:
        basename = os.path.basename(abs_dir)
        return (
            os.path.isdir(abs_dir)
            and basename != "__pycache__"
            and re.match("\..*", basename) == None
        )

    def __institutes_absdir(self) -> str:
        return self.__local_repo + "institutes/"

    def __instruments_absdir(self, institute: str) -> str:
        """Returns the instrument path relative to the institute directory"""
        return self.__institutes_absdir() + institute + "/instruments/"

    def __versions_absdir(self, institute: str, instrument: str) -> str:
        return self.__instruments_absdir(institute) + instrument + "/"

    def __simulation_programs_absdir(
        self, institute: str, instrument: str, version: str
    ) -> str:
        return self.__versions_absdir(institute, instrument) + version + "/"

    def __flavours_absdir(
        self, institute: str, instrument: str, version: str, simulation_program: str
    ) -> str:
        return (
            self.__simulation_programs_absdir(institute, instrument, version)
            + simulation_program
            + "/"
        )

    def get_institutes(self) -> list:
        """
        Get the list of institutes
        """

        basedir = self.__institutes_absdir()
        institutes = []
        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if self.__is_real_dir(dd):
                institutes.append(d)
        return institutes

    def ls_institutes(self) -> None:
        """
        Print the list of institutes
        """
        for institute in self.get_institutes():
            print(" - " + institute)

    def get_instruments(self, institute: str) -> List[str]:
        """ """
        basedir = self.__instruments_absdir(institute)
        instruments = []
        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if self.__is_real_dir(dd):
                instruments.append(d)
        return instruments

    def ls_instruments(self, institute: str) -> None:
        """
        Print the names of the available instruments

        :param institute: name of the institute as returned by :func:`~instrumentdatabaseapi.instrumentdatabaseapi.Repository.ls_institutes`
        """
        print("Available instruments for " + institute + ":")
        for instrument in self.get_instruments(institute):
            print(" - ", institute + "/" + instrument)

    def get_versions(self, institute: str, instrument: str) -> List[str]:
        """ """
        basedir = self.__versions_absdir(institute, instrument)
        versions = []

        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if self.__is_real_dir(dd):
                versions.append(d)
        return versions

    def ls_versions(self, institute: str, instrument: str) -> None:
        """
        Print all implemented versions for the given instrument

        :param institute: name of the institute as returned by :func:`~instrumentdatabaseapi.instrumentdatabaseapi.Repository.ls_institutes`
        :param instrument: name of the instrument as returned by :func:`~instrumentdatabaseapi.instrumentdatabaseapi.Repository.ls_instruments`

        Version formats:
          - **HEAD** is the most recent up-to-date version of the instrument and it is still currently in use
          - **YYYY/MM/DD** last day of validity of the instrument description. After that date, the instrument have been either modified (so more recent version should be available) or it not in service anymore
        """
        print("Available versions for instrument " + instrument + ":")
        for version in self.get_versions(institute, instrument):
            print(" - ", version)

    def get_simulation_programs(self, institute: str, instrument: str, version: str):
        simulation_programs = []

        basedir = self.__simulation_programs_absdir(institute, instrument, version)

        for d in os.listdir(basedir):
            dd = os.path.join(basedir, d)
            if self.__is_real_dir(dd):
                simulation_programs.append(d)
        return simulation_programs

    def ls_simulation_programs(
        self, institute: str, instrument: str, version: str
    ) -> None:
        """
        Print the list of simulation programs for which an instrument is implemented
        """
        print(
            f"Instrument {instrument} from institute {institute} is implemented with the following programs:"
        )
        for sim in self.get_simulation_programs(institute, instrument, version):
            print(" - ", sim)

    def get_flavours(
        self, institute: str, instrument: str, version: str, simulation_program: str
    ) -> List[str]:
        basedir = self.__flavours_absdir(
            institute, instrument, version, simulation_program
        )
        flavours = []
        for d in os.listdir(basedir):
            if re.match(instrument + ".*\.py", d):
                flavours.append(
                    d[len(instrument) : -3]
                )  # removed the instrument string and the .py at the end

        if len(flavours) == 0:
            return [""]

        return flavours

    def ls_flavours(
        self, institute: str, instrument: str, version: str, simulation_program: str
    ) -> None:
        """
        A given instrument might be technically implemented in different ways.
        Flavours are strings meant to distinguish these different implementations.
        By default an empty string should be used for an instrument.
        """

        flavours = self.get_flavours(institute, instrument, version, simulation_program)
        print(f"Available flavours for instrument {instrument}:")
        for d in flavours:
            print(" - ", d)

    def load(
        self,
        institute: str,
        instrument: str,
        version: str = "HEAD",
        simulation_program: str = "",
        flavour: str = "",
        dep: bool = True,
    ) -> Instrument:
        """
        Load an intrument from the repository

        :param simulation_program: name of the simulation program
        :param institute: name of the institute
        :param instrument: name of the instrument
        :param version: version name
        :param flavour: optional string that might identify two alternative implementations of the same instrument with the same version

        :return: the instrument object
        :raise: NotImplementedError if the instrument module does not provide a def_instrument method
        """

        if simulation_program == "":
            # assume there is only one and return it
            # raise error if more than one is found
            simulation_programs = self.get_simulation_programs(
                institute, instrument, version
            )
            if len(simulation_programs) != 1:
                raise RuntimeError(
                    f"No specific simulation program has been required, but {len(simulation_programs)} found"
                )
            simulation_program = simulation_programs[0]

        if flavour == "":
            # double check that an instrument without any flavour exists
            if not os.path.isfile(
                self.__flavours_absdir(
                    institute, instrument, version, simulation_program
                )
                + instrument
                + ".py"
            ):
                # need to retrieve one flavour
                flavours

        modulepath = os.path.relpath(
            self.__flavours_absdir(institute, instrument, version, simulation_program),
            self.__local_repo,
        ).replace("/", ".")
        print(modulepath)
        print(
            self.__flavours_absdir(institute, instrument, version, simulation_program)
        )

        mymodule = modulepath + "." + instrument
        if flavour != "":
            mymodule += "_" + flavour
        print(mymodule)
        if dep:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--target",
                    self.__local_repo + "python_dependencies/",
                    "-r",
                    self.__flavours_absdir(
                        institute, instrument, version, simulation_program
                    )
                    + "/requirements.txt",
                ]
            )

        myinstrumentmodule = importlib.import_module(mymodule)

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
