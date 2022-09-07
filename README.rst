============
Introduction
============
.. image:: https://img.shields.io/pypi/v/instrumentDataBaseAPI.svg
        :target: https://pypi.python.org/pypi/instrumentDataBaseAPI

.. image:: https://img.shields.io/travis/PaNOSC-ViNYL/instrumentDataBaseAPI.svg
        :target: https://travis-ci.com/PaNOSC-ViNYL/instrumentDataBaseAPI

.. image:: https://readthedocs.org/projects/instrumentDataBaseAPI/badge/?version=latest
        :target: https://instrumentDataBaseAPI.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://github.com/PaNOSC-ViNYL/instrumentDataBaseAPI/actions/workflows/doc.yml/badge.svg?event=page_build
	   :target: https://github.com/PaNOSC-ViNYL/instrumentDataBaseAPI/actions/workflows/doc.yml)



This library provides a simple python API to the instrument database of neutron and X-ray facilities for users to be used in Jupyter notebooks with the tools developed by the PANOSC project.

The user is able to retrieve the instrument description from the centrally maintained repository on Github as well as any suitable repository.

This API is meant as a **READ ONLY** access to the instrument database. Modifications to the instrument description can either be performed to the instruments after loading a specific instrument or to the python description script by advanced users.

The instrument database is then copied locally in a temporary directory. It is highly suggested to define which is the local folder PATH.


This API is not part of the instrument database repository, because users can use it to access any kind of instrument database structured as https://github.com/PaNOSC-ViNYL/instrument_database.


* Free software: MIT license
* Documentation: https://panosc-vinyl.github.io/instrumentDataBaseAPI/


