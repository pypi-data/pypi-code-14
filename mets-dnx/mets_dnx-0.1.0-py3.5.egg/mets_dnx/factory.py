import hashlib
import os
import re
import time

from lxml import etree as ET

from pydc import factory as dc_factory
from pymets import mets_factory as mf
from pymets import mets_model
from pydnx import factory as dnx_factory

def generate_md5(filepath, block_size=2**20):
    """For producing md5 checksums for a file at a specified filepath."""
    m = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(block_size)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def build_amdsec(amdsec, tech_sec=None, rights_sec=None, 
                 source_sec=None, digiprov_sec=None):
    amd_id = amdsec.attrib['ID']
    amd_tech = ET.SubElement(
                    amdsec, 
                    "{http://www.loc.gov/METS/}techMD", 
                    ID=amd_id + "-tech")
    amd_rights = ET.SubElement(
                    amdsec,
                    "{http://www.loc.gov/METS/}rightsMD",
                    ID=amd_id + "-rights")
    amd_source = ET.SubElement(
                    amdsec,
                    "{http://www.loc.gov/METS/}sourceMD",
                    ID=amd_id + "-source")
    amd_digiprov = ET.SubElement(
                    amdsec,
                    "{http://www.loc.gov/METS/}digiprovMD",
                    ID=amd_id + "-digiprov")

    for el in [amd_tech, amd_rights, amd_source, amd_digiprov]:
        mdWrap = ET.SubElement(
                        el, 
                        "{http://www.loc.gov/METS/}mdWrap",
                        MDTYPE="OTHER", OTHERMDTYPE="dnx")
        xmlData = ET.SubElement(mdWrap, "{http://www.loc.gov/METS/}xmlData")
        if (el.tag == "{http://www.loc.gov/METS/}techMD" and 
                tech_sec != None):
            xmlData.append(tech_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}rightsMD" and 
                rights_sec != None):
            xmlData.append(rights_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}sourceMD" and 
                source_sec != None):
            xmlData.append(source_sec)
        elif (el.tag == "{http://www.loc.gov/METS/}digiprovMD" and 
                digiprov_sec != None):
            xmlData.append(digiprov_sec)


def build_mets(ie_dmd_dict=None,
                pres_master_dir=None, 
                modified_master_dir=None,
                access_derivative_dir=None,
                cms=None,
                webHarvesting=None,
                generalIECharacteristics=None,
                objectIdentifier=None,
                accessRightsPolicy=None,
                eventList=None,
                input_dir=None,
                digital_original=False):

    mets = mf.build_mets()

    # build ie-dmdsec
    # check if ie_dmd_dict is a single dictionary inside a list
    # (which is the convention for the METS factory, but not necessary for
    # the DC Factory)
    if type(ie_dmd_dict) == list and len(ie_dmd_dict) == 1:
        ie_dmd_dict = ie_dmd_dict[0]
    dc_record = dc_factory.build_dc_record(ie_dmd_dict)
    dmdsec = ET.SubElement(
                mets,
                "{http://www.loc.gov/METS/}dmdSec",
                ID="ie-dmd")
    mdwrap = ET.SubElement(
                dmdsec,
                "{http://www.loc.gov/METS/}mdWrap",
                MDTYPE="DC")
    xmldata = ET.SubElement(
                mdwrap,
                "{http://www.loc.gov/METS/}xmlData")
    xmldata.append(dc_record)

    # build ie amd section
    ie_amdsec = ET.SubElement(
                    mets,
                    "{http://www.loc.gov/METS/}amdSec",
                    ID="ie-amd")
    if ((generalIECharacteristics != None) 
            or (cms != None) 
            or (objectIdentifier != None)
            or (webHarvesting != None)):
        ie_amd_tech = dnx_factory.build_ie_amdTech(
            generalIECharacteristics=generalIECharacteristics,
            objectIdentifier=objectIdentifier)
    else:
        ie_amd_tech = None
    if (accessRightsPolicy != None):
        ie_amd_rights = dnx_factory.build_ie_amdRights(
            accessRightsPolicy=accessRightsPolicy)
    else:
        ie_amd_rights = None
    if (eventList != None):
        ie_amd_digiprov = dnx_factory.build_ie_amdDigiprov(event=eventList)
    else:
        ie_amd_digiprov = None
    # TODO (2016-10-03): add functionality for ie_amdSourceMD
    ie_amd_source = None
    build_amdsec(
            ie_amdsec,
            ie_amd_tech,
            ie_amd_rights,
            ie_amd_digiprov,
            ie_amd_source)

    mf.build_amdsec_filegrp_structmap(
        mets,
        ie_id="ie1", 
        pres_master_dir=pres_master_dir,
        modified_master_dir=modified_master_dir,
        access_derivative_dir=access_derivative_dir,
        digital_original=digital_original,
        input_dir=input_dir)


    # Create representation_level and file_level amdsecs, based on
    # the filegrp details
    file_groups = mets.findall('.//{http://www.loc.gov/METS/}fileGrp')
    for file_group in file_groups:
        rep_id = file_group.attrib['ID']
        rep_type = mets.find('.//{%s}structMap[@ID="%s"]/{%s}div' % 
            ('http://www.loc.gov/METS/', rep_id, 'http://www.loc.gov/METS/')
            ).attrib['LABEL']
        
        if rep_type == 'Preservation Master':
            pres_type = 'PRESERVATION_MASTER'
            pres_location = pres_master_dir
        elif rep_type == 'Modified Master':
            pres_type = 'MODIFIED_MASTER'
            pres_location = modified_master_dir
        elif rep_type == 'Access Derivative':
            pres_location = access_derivative_dir
            pres_type = 'ACCESS_DERIVATIVE'
        else:
            pres_type = None
            pres_location = '.'

        rep_amdsec = mets.xpath("//mets:amdSec[@ID='%s']" % 
                str(rep_id + '-amd'), namespaces=mets.nsmap)[0]
        general_rep_characteristics = [{'RevisionNumber': '1', 
                'DigitalOriginal': str(digital_original).lower(),
                'usageType': 'VIEW',
                'preservationType': pres_type}]
        rep_amd_tech = dnx_factory.build_rep_amdTech(
            generalRepCharacteristics=general_rep_characteristics)
        rep_amd_rights = None
        rep_amd_digiprov = None
        rep_amd_source = None
        build_amdsec(
            rep_amdsec,
            tech_sec=rep_amd_tech, 
            rights_sec=rep_amd_rights,
            source_sec=rep_amd_source, 
            digiprov_sec=rep_amd_digiprov)

        # create amdsec for files
        for fl in file_group.findall('./{http://www.loc.gov/METS/}file'):
            fl_id = fl.attrib['ID']
            fl_amdsec = None
            fl_amdsec = mets.xpath("//mets:amdSec[@ID='%s']" % 
                    str(fl_id + '-amd'), namespaces=mets.nsmap)[0]
            file_original_location = os.path.join(input_dir,
                fl.find('./{http://www.loc.gov/METS/}fLocat').attrib[
                        '{http://www.w3.org/1999/xlink}href'])
            file_size_bytes = os.path.getsize(file_original_location)
            last_modified = time.strftime(
                    "%Y-%m-%dT%H:%M:%S",
                    time.localtime(os.path.getmtime(file_original_location)))
            created_time = time.strftime(
                    "%Y-%m-%dT%H:%M:%S",
                    time.localtime(os.path.getctime(file_original_location)))
            general_file_characteristics = [{
                'fileOriginalPath': file_original_location,
                'fileSizeBytes': str(file_size_bytes),
                'fileModificationDate': last_modified,
                'fileCreationDate': created_time}]

            file_fixity =  [{
                'fixityType': 'md5',
                'fixityValue': generate_md5(file_original_location)}]

            fl_amd_tech = dnx_factory.build_file_amdTech(
                generalFileCharacteristics=general_file_characteristics,
                fileFixity=file_fixity)
            build_amdsec(fl_amdsec, tech_sec=fl_amd_tech)


    # clean up identifiers so they are consistent with Rosetta requirements
    for element in mets.xpath(".//*[@ID]"):
        element.attrib['ID'] = re.sub('ie[0-9]+\-', '', element.attrib['ID'])
        element.attrib['ID'] = re.sub(
                'rep([0-9]+)\-file([0-9]+)',
                r'fid\2-\1',
                element.attrib['ID'])
    for element in mets.xpath(".//*[@ADMID]"):
        element.attrib['ADMID'] = re.sub(
                'ie[0-9]+\-rep([0-9]+)\-file([0-9]+)-amd',
                r'fid\2-\1-amd',
                element.attrib['ADMID'])
        element.attrib['ADMID'] = re.sub(
                'ie[0-9]+\-rep([0-9]+)-amd',
                r'rep\1-amd',
                element.attrib['ADMID'])
    for element in mets.xpath(".//*[@FILEID]"):
        element.attrib['FILEID'] = re.sub(
                'ie[0-9]+\-rep([0-9])+\-file([0-9]+)',
                r'fid\2-\1',
                element.attrib['FILEID'])
    return mets



