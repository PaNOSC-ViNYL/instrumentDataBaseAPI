"""Main module."""


class repository(url, local_repo=NULL):
    """Initiate the repository from an URL or local repo"""
    def __init__(self):

    def ls_instrument():
        """Print the names of the available samples"""
    def load(instrument, version="HEAD"):
        """Load an intrument from the repository"""
        return instrument_obj
    def dump_instrument(outfile):
        """Save the instrument in .py format"""
    def save_parameters(outfile):
        """Print the parameters of the instrument in .json format"""

#TODO: I'm not sure if we define the instrument here,
#or elsewhere. This is no instrument class defined in pyvinyl.
#https://github.com/PaNOSC-ViNYL/libpyvinyl/blob/master/libpyvinyl/BaseCalculator.py#L45
#but I think to add an instrument layer could be a good idea.
class instrument():
    """An instrument class"""
    def __init__(self, ):
        pass


if __name__ == "__main__":
    my_instrument, my_params = repository(my_url).load(my_instrument)
