from elavonvtpv.enum import CVNIndicator
from xml.etree import ElementTree as ETree


class Mpi:
    def __init__(self, eci, cavv=None, xid=None):
        """
        Defines a Mpi object
        :param cavv: the CAVV or UCAF value necessary for the authorization request
        :param xid: the XID field necessary for the authorization request
        :param eci: the electronic commerce indicator necessary for the authorization request
        """
        self.cavv = cavv
        self.xid = xid
        self.eci = eci

    def to_etree_element(self):
        """
        Transforms the Mpi object into an ElementTree Element so it can be used in the creation of a XML
        :return: An ElmentTree Element containing the data on the Mpi object
        """
        mpi = ETree.Element('mpi')

        if self.cavv:
            cavv = ETree.SubElement(mpi, 'cavv')
            cavv.text = self.cavv

        if self.xid:
            xid = ETree.SubElement(mpi, 'xid')
            xid.text = self.xid

        eci = ETree.SubElement(mpi, 'eci')
        eci.text = self.eci

        return mpi
