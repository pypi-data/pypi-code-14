# First write in 2016-7-30
# by sheep @ scut
# Usage: Pathway objects and interfaces
from ..visualize.options import IntegrationOptions


class Pathway:
    def __init__(self):
        self.core_implement = None
        self.option = None
        pass

    '''
    This is the core object of this module, parse files from file or public database, provide methods for data
    export, integration, visualize and modify

    Attribute:
        core_implement: KEGG, BioPAX or SBGN.
    '''

    def export(self):
        '''
        Export self to certain pathway format
        :param format: the desire format want to export
        :return: a xml string of export result
        '''
        raise NotImplementedError

    def draw(self):
        '''
        draw self
        :return: None
        '''
        raise NotImplementedError

    def integrate(self, id_lists, visualize_option_lists):
        '''
        to integrate custom data to the pathway
        :param id_lists: the id list of a pathway
        :param visualize_option_lists: the visualize option of a pathway
        :return: None
        '''
        self.option = IntegrationOptions()
        self.option.set(id_lists, visualize_option_lists)

    # below is several property
    @property
    def root(self):
        raise NotImplementedError

    @property
    def is_root(self):
        raise NotImplementedError

    @property
    def children(self):
        raise NotImplementedError

    def flatten(self):
        raise NotImplementedError

    @property
    def members(self):
        raise NotImplementedError

    @property
    def nodes(self):
        raise NotImplementedError
