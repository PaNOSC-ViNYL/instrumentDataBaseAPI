Quickstart
==========

.. code-block:: python
		
		from instrumentdatabaseapi import instrumentdatabaseapi as API
		repo = API.Repository(local_repo=".")
		repo.init(local_repo="instrumentdb")
		institute_name = "ILL"
		instrument_name = "ThALES"
		instrument_version="HEAD"
		simulation_program="mcstas"
		myinstrument = repo.load(institute_name,
		                         instrument_name,
					 instrument_version,
					 simulation_program,
					 dep=False)

