#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt") as requirements_file:
    require = requirements_file.read()
    requirements = require.split()

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]


def get_from_init(rel_path,field):
    for line in read(rel_path).splitlines():
        if line.startswith(field):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find "+field+" string.")

initfile="instrumentdatabaseapi/__init__.py"

setup(
    author=get_from_init(initfile,"__author__")
    author_email=get_from_init(initfile,"__email__"),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="The API to retrieve an instrumentation",
    entry_points={
        "console_scripts": [
            "instrumentdatabaseapi=instrumentdatabaseapi.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="instrumentDataBaseAPI",
    name="instrumentDataBaseAPI",
    packages=find_packages(
        include=["instrumentdatabaseapi", "instrumentdatabaseapi.*"]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/PaNOSC-ViNYL/instrumentDataBaseAPI",
    version=get_from_init(initfile,"__version__"),
    zip_safe=False,
)
