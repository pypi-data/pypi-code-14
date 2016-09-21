#!/usr/bin/env python3

import argparse
import os
import sys
import xml.etree.ElementTree
import json

def get_experiment_library_name(EXPERIMENT):
    DESIGN = EXPERIMENT.findall('DESIGN')
    if len(DESIGN) > 1:
        print('more than 1 DESIGN')
        sys.exit(1)
    LIBRARY_DESCRIPTOR = DESIGN[0].findall('LIBRARY_DESCRIPTOR')
    if len(LIBRARY_DESCRIPTOR) > 1:
        print('more than 1 LIBRARY_DESCRIPTOR')
        sys.exit(1)
    LIBRARY_NAME = LIBRARY_DESCRIPTOR[0].findall('LIBRARY_NAME')
    if len(LIBRARY_NAME) > 1:
        print('more than 1 LIBRARY_NAME')
        sys.exit(1)
    return LIBRARY_NAME[0].text

def modify_tcga_dict(result, library_target_dict, bam_name, key_set,
                                         xml_multi_capture_per_library_path_open,
                                         xml_no_capture_per_library_path_open):
    center_name = result.find('center_name').text
    bam_name = get_bam_name_set_from_result(result)
    analysis_id = result.find('analysis_id').text
    print('analysis_id=%s' % analysis_id)
    result_id = result.items()[0][1]
    if center_name == 'BCM' or center_name == 'WUGSC' or center_name == 'SANGER' or center_name == 'BI':
        experiment_xml = result.find('experiment_xml')
        if len(experiment_xml.findall('EXPERIMENT_SET')) != 1:
               print('analysis_id: %s has != 1 experimental_xml.findall(EXPERIMENT_SET)' % analysis_id)
               sys.exit(1)
        EXPERIMENT_SET = experiment_xml.find('EXPERIMENT_SET')
        for EXPERIMENT in EXPERIMENT_SET.findall('EXPERIMENT'):
            library_name = get_experiment_library_name(EXPERIMENT)
            library_target_dict[bam_name][library_name] = dict()
            library_target_dict[bam_name][library_name]['capture_kits'] = list()
            library_target_dict[bam_name][library_name]['target_set'] = list()
            library_target_dict[bam_name]['center_name'] = center_name
            library_target_dict[bam_name]['analysis_id'] = analysis_id
            library_target_dict[bam_name]['project'] = 'tcga'
            if len(EXPERIMENT.findall('EXPERIMENT_ATTRIBUTES')) == 0:
                xml_no_capture_per_library_path_open.write('center_name=' + center_name + '\tanalysis_id=' + analysis_id +
                                                           '\tbam_name=' + bam_name + '\tlibrary_name=' + library_name + '\n')
                continue
            if len(EXPERIMENT.findall('EXPERIMENT_ATTRIBUTES')) > 1:
                print('>1 EXPERIMENT_ATTRIBUTES')
                sys.exit(1)
            EXPERIMENT_ATTRIBUTES = EXPERIMENT.find('EXPERIMENT_ATTRIBUTES')
            num_capture_kit_info = 0
            for EXPERIMENT_ATTRIBUTE in EXPERIMENT_ATTRIBUTES.findall('EXPERIMENT_ATTRIBUTE'):
                if EXPERIMENT_ATTRIBUTE.find('TAG').text == 'CAPTURE_KIT_INFO':
                    if num_capture_kit_info > 1:
                        print('analysis_id: %s has >1 num_capture_kit' % analysis_id)
                        print('library_name = %s' % library_name)
                        sys.exit(1)
                    num_capture_kit_info += 1
                    CAPTURE_KIT_INFO_json = EXPERIMENT_ATTRIBUTE.find('VALUE').text
                    tsv_json = json.loads(CAPTURE_KIT_INFO_json)
                    capture_kits = tsv_json.get('capture_kits')
                    if len(capture_kits) > 0:
                        if len(capture_kits) > 1:
                            xml_multi_capture_per_library_path_open.write('center_name=' + center_name + '\tanalysis_id=' + analysis_id +
                                                                          '\tbam_name=' + bam_name + '\tlibrary_name=' + library_name + '\n')
                        for capture_kit in capture_kits:
                            capture_dict = dict()
                            key_list = capture_kit.keys() # for discovery/normalization
                            for akey in key_list:
                                key_set.add(akey)         # /end for disc/norm
                            capture_dict['cached_target_file_url'] = capture_kit.get('cached_target_file_url', None)
                            capture_dict['catalog_number'] = capture_kit.get('catalog_number')
                            capture_dict['is_custom'] = capture_kit.get('is_custom', None)
                            capture_dict['probe_file_url'] = capture_kit.get('probe_file_url', None)
                            capture_dict['reagent_name'] = capture_kit.get('reagent_name')
                            capture_dict['reagent_vendor'] = capture_kit.get('reagent_vendor')
                            capture_dict['target_file_url'] = capture_kit.get('target_file_url')
                            library_target_dict[bam_name][library_name]['capture_kits'].append(capture_dict)
                    elif len(capture_kits) == 0:
                        xml_no_capture_per_library_path_open.write('center_name=' + center_name + '\tanalysis_id=' + analysis_id +
                                                                      '\tbam_name=' + bam_name + '\tlibrary_name=' + library_name + '\n')
                        library_target_dict[bam_name][library_name] = list()
                if EXPERIMENT_ATTRIBUTE.find('TAG').text == 'target_set':
                    target_set = EXPERIMENT_ATTRIBUTE.find('VALUE').text
                    library_target_dict[bam_name][library_name]['target_set'].append(target_set)
            if num_capture_kit_info == 0:
                print('analysis_id: %s has 0 num_capture_kit' % analysis_id)
                sys.exit(1)
    else:
        sys.exit('unknown center_name: %s' % center_name)
    return library_target_dict

def get_bam_name_set_from_result(result):
    files = result.find('files')
    bam_name_set = set()
    for afile in files.findall('file'):
        file_name = afile.find('filename').text
        if file_name.endswith('.bam'):
            bam_name_set.add(file_name)
    if len(bam_name_set) == 0:
        print('result does not have a bam: %s' % result)
        return None
    elif len(bam_name_set) > 1:
        print('bam_name_set=%s' % str(bam_name_set))
        print('should only be 1 bam')
        sys.exit(1)
    elif len(bam_name_set) == 1:
        return bam_name_set.pop()
    sys.exit('should not be here')
    return

def get_dict_from_tcga_xml_path(xml_path):
    print('xml_path=%s' % xml_path)
    print('get tree')
    sys.stdout.flush()
    tree = xml.etree.ElementTree.parse(xml_path)
    print('get root')
    sys.stdout.flush()
    root = tree.getroot()
    print('get children')
    sys.stdout.flush()
    results = root.getchildren()

    xml_basename = os.path.basename(xml_path)
    xml_dirname = os.path.dirname(xml_path)
    xml_name, xml_ext = os.path.splitext(xml_basename)
    xml_multi_capture_per_library = xml_name + '_multi_capture_per_library'
    xml_no_capture_per_library = xml_name + '_no_capture_per_library'

    xml_multi_capture_per_library_path_open = open(xml_multi_capture_per_library, 'w')
    xml_no_capture_per_library_path_open = open(xml_no_capture_per_library, 'w')

    library_target_dict = dict()
    bam_set = set()
    key_set = set()
    print('get tcga results')
    sys.stdout.flush()
    for i, result in enumerate(results):
        if len(result.items()) == 0:
            continue
        else:
            print('i=%s' % str(int(i) - 1))
            bam_name = get_bam_name_set_from_result(result)
            if bam_name is not None:
                if bam_name in bam_set:
                    print('duplicate bam_name: %s' % bam_name)
                bam_set.add(bam_name)
                library_target_dict[bam_name] = dict()
                modify_tcga_dict(result, library_target_dict, bam_name, key_set,
                                 xml_multi_capture_per_library_path_open,
                                 xml_no_capture_per_library_path_open)
    xml_multi_capture_per_library_path_open.close()
    xml_no_capture_per_library_path_open.close()
    print('\n\nkey_set = %s' % key_set)
    return library_target_dict

def modify_target_dict(result, library_target_dict, bam_name, target_set_set,
                       xml_multi_capture_per_library_path_open,
                       xml_no_capture_per_library_path_open):
    center_name = result.find('center_name').text
    analysis_id = result.find('analysis_id').text
    experiment_xml = result.find('experiment_xml')
    EXPERIMENT_SET = experiment_xml.find('EXPERIMENT_SET')
    # if len(EXPERIMENT_SET) != 1:
    #     print('number of EXPERIMENT_SET: %s' % str(len(EXPERIMENT_SET)))
    #     print('analysis_id: %s' % analysis_id)
    #     sys.exit(1)
    for EXPERIMENT in EXPERIMENT_SET.findall('EXPERIMENT'):
        library_name = get_experiment_library_name(EXPERIMENT)
        library_target_dict[bam_name][library_name] = dict()
        library_target_dict[bam_name][library_name]['target_set'] = list()
        library_target_dict[bam_name]['center_name'] = center_name
        library_target_dict[bam_name]['analysis_id'] = analysis_id
        library_target_dict[bam_name]['project'] = 'target'
        print('analysis_id=%s' % analysis_id)
        EXPERIMENT_ATTRIBUTES = EXPERIMENT.findall('EXPERIMENT_ATTRIBUTES')
        if len(EXPERIMENT_ATTRIBUTES) == 0:
            xml_no_capture_per_library_path_open.write('center_name=' + center_name + '\tanalysis_id=' + analysis_id +
                                                       '\tbam_name=' + bam_name + '\tlibrary_name=' + library_name + '\n')
            continue
        if len(EXPERIMENT_ATTRIBUTES) != 1:

            print('number of EXPERIMENT_ATTRIBUTES: %s' % str(len(EXPERIMENT_ATTRIBUTES)))
            print('analysis_id: %s' % analysis_id)
            sys.exit(1)
        num_target_set = 0
        for EXPERIMENT_ATTRIBUTE in EXPERIMENT_ATTRIBUTES[0].findall('EXPERIMENT_ATTRIBUTE'):
            if EXPERIMENT_ATTRIBUTE.find('TAG').text == 'target_set':
                target_set = EXPERIMENT_ATTRIBUTE.find('VALUE').text
                target_set_set.add(target_set)
                library_target_dict[bam_name][library_name]['target_set'].append(target_set)
                num_target_set += 1
        if num_target_set == 0:
            xml_no_capture_per_library_path_open.write('center_name=' + center_name + '\tanalysis_id=' + analysis_id +
                                                       '\tbam_name=' + bam_name + '\tlibrary_name=' + library_name + '\n')
        if num_target_set > 1:
            print('num_target_set=%s' % num_target_set)
            print('analysis_id: %s' % analysis_id)
            sys.exit(1)
    return

def get_dict_from_target_xml_path(xml_path):
    print('xml_path=%s' % xml_path)
    print('get tree')
    sys.stdout.flush()
    tree = xml.etree.ElementTree.parse(xml_path)
    print('get root')
    sys.stdout.flush()
    root = tree.getroot()
    print('get children')
    sys.stdout.flush()
    results = root.getchildren()

    xml_basename = os.path.basename(xml_path)
    xml_dirname = os.path.dirname(xml_path)
    xml_name, xml_ext = os.path.splitext(xml_basename)
    xml_multi_capture_per_library = xml_name + '_multi_capture_per_library'
    xml_no_capture_per_library = xml_name + '_no_capture_per_library'
    xml_multi_capture_per_library_path_open = open(xml_multi_capture_per_library, 'w')
    xml_no_capture_per_library_path_open = open(xml_no_capture_per_library, 'w')

    library_target_dict = dict()
    bam_set = set()
    target_set_set = set()
    print('get target results')
    sys.stdout.flush()
    for i, result in enumerate(results):
        if len(result.items()) == 0:
            continue
        else:
            print('i=%s' % str(int(i) - 1))
            bam_name = get_bam_name_set_from_result(result)
            if bam_name is not None:
                if bam_name in bam_set:
                    print('duplicate bam_name: %s' % bam_name)
                    sys.exit(1)
                bam_set.add(bam_name)
                library_target_dict[bam_name] = dict()
                modify_target_dict(result, library_target_dict, bam_name, target_set_set,
                                xml_multi_capture_per_library_path_open,
                                xml_no_capture_per_library_path_open)

    xml_multi_capture_per_library_path_open.close()
    xml_no_capture_per_library_path_open.close()
    print('target_set_set = %s' % str(target_set_set))
    return library_target_dict

def main():
    parser = argparse.ArgumentParser('capture kit from cgquery xml')
    parser.add_argument('-t', '--tcga_xml_path', required=True)
    parser.add_argument('-g', '--target_xml_path', required=True)
    args = vars(parser.parse_args())

    tcga_xml_path = args['tcga_xml_path']
    target_xml_path = args['target_xml_path']

    tcga_bam_libraryname_capturekey_dict = get_dict_from_tcga_xml_path(tcga_xml_path)
    target_bam_libraryname_capturekey_dict = get_dict_from_target_xml_path(target_xml_path)

    total_bam_libraryname_capturekey_dict = {**tcga_bam_libraryname_capturekey_dict, **target_bam_libraryname_capturekey_dict}

    bam_libraryname_capturekey_json_path = 'bam_libraryname_capturekey.json'

    with open(bam_libraryname_capturekey_json_path, 'wt') as json_path_open:
        json.dump(total_bam_libraryname_capturekey_dict, json_path_open, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
