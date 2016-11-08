from __future__ import unicode_literals, absolute_import, print_function
from StringIO import StringIO
from xml.etree import ElementTree

from zerotk.string import dedent
from zerotk.xml_factory import WritePrettyXML, WritePrettyXMLElement, XmlFactory
import pytest


class TestXmlFactory(object):

    def test_simplest(self):
        '''
        <?xml version="1.0" ?>
        <user>
          <name>Alpha</name>
          <login>Bravo</login>
        </user>
        '''
        factory = XmlFactory('user')
        factory['name'] = 'Alpha'
        factory['login'] = 'Bravo'

        assert (
            factory.GetContents(xml_header=True)
            == dedent(self.test_simplest.__doc__)
        )
        assert factory.AsDict() == {"login": "Bravo", "name": "Alpha"}
        assert factory.AsJson() == '{"login": "Bravo", "name": "Alpha"}'

    def test_simple(self):
        '''
        <user>
          <name>Alpha</name>
          <login>Bravo</login>
          <location>
            <city>Charlie</city>
          </location>
        </user>
        '''
        factory = XmlFactory('user')
        factory['name'] = 'Alpha'
        factory['login'] = 'Bravo'
        factory['location/city'] = 'Charlie'

        assert (
            factory.GetContents()
            == dedent(self.test_simple.__doc__)
        )
        assert factory.AsDict() == {"login": "Bravo", "name": "Alpha", "location": {"city": "Charlie"}}
        assert factory.AsJson() == '{"login": "Bravo", "name": "Alpha", "location": {"city": "Charlie"}}'

    def test_attributes(self):
        '''
        <root>
          <alpha one="1" two="2">Alpha</alpha>
          <bravo>
            <charlie three="3"/>
          </bravo>
        </root>
        '''
        factory = XmlFactory('root')
        factory['alpha'] = 'Alpha'
        factory['alpha@one'] = '1'
        factory['alpha@two'] = '2'
        factory['bravo/charlie@three'] = '3'

        assert (
            factory.GetContents()
            == dedent(self.test_attributes.__doc__)
        )
        # We're ignoring attributes and empty tags for now.
        assert factory.AsDict() == {"alpha": "Alpha", "bravo": {"charlie": None}}
        assert factory.AsJson() == '{"alpha": "Alpha", "bravo": {"charlie": null}}'

    def test_repeating_tags(self):
        '''
        <root>
          <elements>
            <name>Alpha</name>
            <name>Bravo</name>
            <name>Charlie</name>
          </elements>
          <components>
            <component>
              <name>Alpha</name>
            </component>
            <component>
              <name>Bravo</name>
            </component>
            <component>
              <name>Charlie</name>
            </component>
          </components>
        </root>
        '''
        factory = XmlFactory('root')
        factory['elements/name'] = 'Alpha'
        factory['elements/name+'] = 'Bravo'
        factory['elements/name+'] = 'Charlie'

        factory['components/component+/name'] = 'Alpha'
        factory['components/component+/name'] = 'Bravo'
        factory['components/component+/name'] = 'Charlie'

        assert (
            factory.GetContents()
            == dedent(self.test_repeating_tags.__doc__)
        )
        assert factory.AsDict() == {
            "elements": {"name": ["Alpha", "Bravo", "Charlie"]},
            "components": {"component": [
                {"name": "Alpha"},
                {"name": "Bravo"},
                {"name": "Charlie"}
            ]}
        }
        assert factory.AsJson() == '{"elements": {"name": ["Alpha", "Bravo", "Charlie"]}, "components": '\
            '{"component": [{"name": "Alpha"}, {"name": "Bravo"}, {"name": "Charlie"}]}}'

    def test_hudson_job(self):
        '''
        <project>
          <actions/>
          <description/>
          <logRotator>
            <daysToKeep>7</daysToKeep>
            <numToKeep>7</numToKeep>
          </logRotator>
          <keepDependencies>false</keepDependencies>
          <properties/>
          <scm class="hudson.scm.SubversionSCM">
            <useUpdate>true</useUpdate>
            <excludedRegions/>
            <excludedUsers/>
            <excludedRevprop/>
          </scm>
          <assignedNode>KATARN</assignedNode>
          <canRoam>false</canRoam>
          <disabled>false</disabled>
          <blockBuildWhenUpstreamBuilding>true</blockBuildWhenUpstreamBuilding>
          <concurrentBuild>false</concurrentBuild>
          <buildWrappers/>
          <customWorkspace>WORKSPACE</customWorkspace>
        </project>
        '''
        factory = XmlFactory('project')
        factory['actions']
        factory['description']
        factory['logRotator/daysToKeep'] = '7'
        factory['logRotator/numToKeep'] = '7'
        factory['keepDependencies'] = 'false'
        factory['properties']
        factory['scm@class'] = 'hudson.scm.SubversionSCM'
        factory['scm/useUpdate'] = 'true'
        factory['scm/excludedRegions']
        factory['scm/excludedUsers']
        factory['scm/excludedRevprop']
        factory['assignedNode'] = 'KATARN'
        factory['canRoam'] = 'false'
        factory['disabled'] = 'false'
        factory['blockBuildWhenUpstreamBuilding'] = 'true'
        factory['concurrentBuild'] = 'false'
        factory['buildWrappers']
        factory['customWorkspace'] = 'WORKSPACE'

        assert (
            factory.GetContents()
            == dedent(self.test_hudson_job.__doc__)
        )

    def test_trigger_class(self):
        '''
        <root>
          <triggers class="vector"/>
        </root>
        '''
        # Simulating the use for HudsonJobGenerator._CreateTriggers
        factory = XmlFactory('root')
        triggers = factory['triggers']
        triggers['@class'] = 'vector'

        assert (
            factory.GetContents()
            == dedent(self.test_trigger_class.__doc__)
        )

    def test_type_error(self):
        with pytest.raises(TypeError):
            XmlFactory(9)

    def test_pretty_xml_to_stream(self, datadir):
        '''
        <root>
          <alpha enabled="true">
            <bravo>
              <charlie/>
            </bravo>
            <bravo.one/>
            <delta>XXX</delta>
          </alpha>
        </root>
        '''
        iss = file(datadir['input.xml'], 'r')
        oss = StringIO()

        WritePrettyXML(iss, oss)
        assert oss.getvalue() == dedent(self.test_pretty_xml_to_stream.__doc__)

    def test_pretty_xml_to_file(self, datadir):
        import filecmp
        iss = file(datadir['input.xml'], 'r')
        obtained_filename = datadir['pretty.obtained.xml']
        expected_filename = datadir['pretty.expected.xml']

        WritePrettyXML(iss, obtained_filename)
        assert_files_equal(obtained_filename, expected_filename)

    def test_escape(self):
        element = ElementTree.Element('root')
        element.attrib['name'] = '<no>'
        element.text = '> 3'
        oss = StringIO()
        WritePrettyXMLElement(oss, element)
        assert oss.getvalue() == '<root name="&lt;no&gt;">&gt; 3</root>'

        element = ElementTree.fromstring(oss.getvalue())
        assert element.attrib['name'] == '<no>'
        assert element.text == '> 3'


def assert_files_equal(obtained_filename, expected_filename):
    import filecmp
    import difflib

    if not filecmp.cmp(obtained_filename, expected_filename):
        obtained = open(obtained_filename, 'r').readlines()
        expected = open(expected_filename, 'r').readlines()
        diff = ['FILES DIFFER:', obtained_filename, expected_filename]
        diff += difflib.context_diff(obtained, expected)
        raise AssertionError('\n'.join(diff) + '\n')

    assert True
