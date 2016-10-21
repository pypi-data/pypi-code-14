""" Convert nose-style test reports to UnitTH-style test reports by splitting modules into separate XML files

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2017-07-27
:Copyright: 2016, Karr Lab
:License: MIT
"""

from __future__ import unicode_literals
from xml.dom import minidom
import os


class Converter(object):
    """ Convert nose-style test reports to UnitTH-style test reports by splitting modules into separate XML files """

    @staticmethod
    def run(in_file_nose, out_dir_unitth):
        """ Convert nose-style test reports to UnitTH-style test reports by splitting modules into separate XML files

        Args:
            in_file_nose (:obj:`str`): path to nose-style test report
            out_file_unitth (:obj:`str`): path to save UnitTH-style test reports
        """
        suites = Converter.read_nose(in_file_nose)
        Converter.write_unitth(suites, out_dir_unitth)

    @staticmethod
    def read_nose(in_file):
        """ Parse nose-style test reports into a `dict`

        Args:
            in_file (:obj:`str`): path to nose-style test report

        Returns:
            :obj:`dict`: dictionary of test suites
        """
        suites = {}
        doc_xml = minidom.parse(in_file)
        suite_xml = doc_xml.getElementsByTagName("testsuite")[0]
        for case_xml in suite_xml.getElementsByTagName('testcase'):
            classname = case_xml.getAttribute('classname')
            if classname not in suites:
                suites[classname] = []
            case = {
                'name': case_xml.getAttribute('name'),
                'time': float(case_xml.getAttribute('time')),
            }
            
            skipped_xml = case_xml.getElementsByTagName('skipped')
            if skipped_xml:
                if skipped_xml[0].hasAttribute('type'):
                    type = skipped_xml[0].getAttribute('type')
                else:
                    type = ''
                case['skipped'] = {
                    'type': type,
                    'message': skipped_xml[0].getAttribute('message'),
                    'text': "".join([child.nodeValue for child in skipped_xml[0].childNodes]),
                }

            failure_xml = case_xml.getElementsByTagName('failure')
            if failure_xml:
                if failure_xml[0].hasAttribute('type'):
                    type = failure_xml[0].getAttribute('type')
                else:
                    type = ''
                case['failure'] = {
                    'type': type,
                    'message': failure_xml[0].getAttribute('message'),
                    'text': "".join([child.nodeValue for child in failure_xml[0].childNodes]),
                }

            error_xml = case_xml.getElementsByTagName('error')
            if error_xml:
                if error_xml[0].hasAttribute('type'):
                    type = error_xml[0].getAttribute('type')
                else:
                    type = ''
                case['error'] = {
                    'type': type,
                    'message': error_xml[0].getAttribute('message'),
                    'text': "".join([child.nodeValue for child in error_xml[0].childNodes]),
                }

            suites[classname].append(case)

        return suites

    @staticmethod
    def write_unitth(suites, out_dir):
        """ Write UnitTH-style test reports 

        Args:
            suites (:obj:`dict`): dictionary of test suites
            out_dir (:obj:`str`): path to save UnitTH-style test reports
        """
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)

        for classname, cases in suites.items():
            doc_xml = minidom.Document()

            suite_xml = doc_xml.createElement('testsuite')
            suite_xml.setAttribute('name', classname)
            suite_xml.setAttribute('tests', str(len(cases)))
            suite_xml.setAttribute('errors', str(sum('error' in case for case in cases)))
            suite_xml.setAttribute('failures', str(sum('failure' in case for case in cases)))
            suite_xml.setAttribute('skipped', str(sum('skipped' in case for case in cases)))
            suite_xml.setAttribute('time', '{:.3f}'.format(sum(case['time'] for case in cases)))
            doc_xml.appendChild(suite_xml)

            for case in cases:
                case_xml = doc_xml.createElement('testcase')
                case_xml.setAttribute('classname', classname)
                case_xml.setAttribute('name', case['name'])
                case_xml.setAttribute('time', '{:.3f}'.format(case['time']))
                suite_xml.appendChild(case_xml)

                if 'skipped' in case:
                    skipped_xml = doc_xml.createElement('skipped')
                    skipped_xml.setAttribute('type', case['skipped']['type'])
                    skipped_xml.setAttribute('message', case['skipped']['message'])
                    case_xml.appendChild(skipped_xml)

                    skipped_text_xml = doc_xml.createCDATASection(case['skipped']['text'])
                    skipped_xml.appendChild(skipped_text_xml)

                if 'failure' in case:
                    failure_xml = doc_xml.createElement('failure')
                    failure_xml.setAttribute('type', case['failure']['type'])
                    failure_xml.setAttribute('message', case['failure']['message'])
                    case_xml.appendChild(failure_xml)

                    failure_text_xml = doc_xml.createCDATASection(case['failure']['text'])
                    failure_xml.appendChild(failure_text_xml)

                if 'error' in case:
                    error_xml = doc_xml.createElement('error')
                    error_xml.setAttribute('type', case['error']['type'])
                    error_xml.setAttribute('message', case['error']['message'])
                    case_xml.appendChild(error_xml)

                    error_text_xml = doc_xml.createCDATASection(case['error']['text'])
                    error_xml.appendChild(error_text_xml)

            with open(os.path.join(out_dir, '{}.xml'.format(classname)), 'w') as output:
                doc_xml.writexml(output, encoding='utf-8', addindent='', newl="")
            doc_xml.unlink()
