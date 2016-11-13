#!/usr/bin/env python

'''
MIT License

Copyright (c) 2016 Sebastian Antonsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''



import argparse
import os
import re
import warnings
import subprocess
import tempfile
import xmltodict
from fdfgen import forge_fdf

# tell user where to get pdftk
# TODO - package this in a sensible way


class Monster():

    def __init__(self, xml, monster_name, position):
        try:
            with open(xml) as xml:
                monsters = xmltodict.parse(xml.read())
            for m in monsters['compendium']['monster']:
                if m['name'] == monster_name:
                    monster = m
                    break
                else:
                    monster = None
        except:
            raise Exception(ValueError, "Could not parse " + xml.name)

        self.monster = monster
        if monster != None:
            self.fields = self._getFields(position)
        else:
            print "{0} is not a recognized monster.".format(monster_name)
            self.fields = [(' '.join(['Monster Name', str(position)]), monster_name)]

    def _getFields(self, position):

        fields = []

        stats = [('STR', self.monster['str']),
                 ('DEX', self.monster['dex']),
                 ('CON', self.monster['con']),
                 ('INT', self.monster['int']),
                 ('WIS', self.monster['wis']),
                 ('CHA', self.monster['cha'])]

        def _statMod(stat):
            stat = int(stat)
            stat_modifier = int((stat - 10) / 2)
            if stat_modifier >= 0:
                stat_modifier = '+' + str(stat_modifier)
            else:
                stat_modifier = str(stat_modifier)

            return stat_modifier


        stat_modifiers = [('STR Modifier', _statMod(self.monster['str'])),
                          ('DEX Modifier', _statMod(self.monster['dex'])),
                          ('CON Modifier', _statMod(self.monster['con'])),
                          ('INT Modifier', _statMod(self.monster['int'])),
                          ('WIS Modifier', _statMod(self.monster['wis'])),
                          ('CHA Modifier', _statMod(self.monster['cha']))]

        def _getXpValue(cr):
            xp_by_cr = [('0',10), ('1/8',25),
                        ('1/4',50), ('1/2',100),
                        ('1',200), ('2',450),
                        ('3',700), ('4',1100),
                        ('5',1800), ('6',2300),
                        ('7',2900), ('8',3900),
                        ('9',5000), ('10',5900),
                        ('11',7200), ('12',8400),
                        ('13',10000), ('14',11500),
                        ('15',13000), ('16',15000),
                        ('17',18000), ('18',20000),
                        ('19',22000), ('20',25000),
                        ('21',33000), ('22',41000),
                        ('23',50000), ('24',62000),
                        ('25',75000), ('26',90000),
                        ('27',105000), ('28',12000),
                        ('29',135000), ('30',155000)]
            for i in xp_by_cr:
                if cr == i[0]:
                    xp_value = "{:,}".format(i[1])
                    break
                else:
                    xp_value = None

            return xp_value


        def _getTypeRace(monster_type):
            if '(' in monster_type:
                m_type, race = monster_type.split('(')
                race = race[:-1]
            else:
                m_type = monster_type
                race = monster_type

            m_type = m_type.capitalize()
            race = race.capitalize()
            return m_type, race


        def _getSpeed():
            speed = self.monster['speed']
            # get the first the highest
            numbers = re.compile('\d+(?:\d+)?')
            speed =  numbers.findall(speed)
            speed = '/'.join([speed[0], max(speed)])

            return speed


        def _getHP():
            hp = self.monster['hp'].split(' ')[0]
            return hp


        def _getAC():
            ac = self.monster['ac'][:2]
            return ac

        info = [('Monster Name', self.monster['name']),
                ('Challenge', self.monster['cr']),
                ('XP', _getXpValue(self.monster['cr'])),
                ('Type', _getTypeRace(self.monster['type'])[0]),
                ('Race', _getTypeRace(self.monster['type'])[1]),
                ('Size', self.monster['size']),
                ('AC', _getAC()),
                ('Speed', _getSpeed()),
                ('Initiative', _statMod(self.monster['dex'])),
                ('HP A', _getHP())]

        def getAttacks():
            # get a list from actions containing only attacks
            attacks_list = []
            # create a string to hold all the attack notes
            attack_notes_strings = []

            actions = self.monster['action']

            # populate the list of all 'attacks'
            # and populate the list of all non 'attacks'
            if isinstance(actions, list):
                for action in actions:
                    if not action['name'] == 'Multiattack':
                        if 'attack' in action:
                            attacks_list.append(action)
                        else:
                            attack_notes_strings.append(action['name'])
            else:
                if 'attack' in actions:
                    attacks_list.append(actions)
                else:
                    attack_notes_strings.append(action['name'])

            # create a list for the attack formatting
            attacks = []
            # populate the list containing the attack formatting
            i = 0
            for idx in range(len(attacks_list)):
                attack = attacks_list[i]
                if idx > 2 :
                    # throw the 4th or higher attack into attack notes
                    # titles only
                    attack_notes_strings.append(attack['name'])

                if attack['name'] == 'Multiattack':
                    continue
                first = 'Attack ' + chr((i) + ord('A'))
                second = 'Attack Bonus ' + chr((i) + ord('A'))
                third = 'Damage/Type ' + chr((i) + ord('A'))

                i+=1

                attacks.append([first, attack['name']])
                #if weapon is versatile (one or two handed) attack['attack']
                #returns a list.
                if not isinstance(attack['attack'], list):
                    attacks.append([second, '+' + attack['attack'].split('|')[1]])
                    attacks.append([third, attack['attack'].split('|')[2]])
                else:
                    one_handed, two_handed = attack['attack']
                    attack_bonus = one_handed.split('|')[1]
                    damage = one_handed.split('|')[2] + '/' + two_handed.split('|')[2]
                    attacks.append([second, '+' + attack_bonus])
                    attacks.append([third, damage])

            # crate a list for all spells

            # find spells
            m = self.monster
            spells = self.monster['spells']
            if spells:
                attack_notes_strings.append(spells)

            # consolidate all the attack notes
            attack_notes_string = ', '.join(attack_notes_strings)
            # add the attack notes to the output of the function
            attacks.extend([('Attack Notes', attack_notes_string)])

            return attacks

        def getTraitsSkills():
            traitsSkills = []
            ts_strings = []
            m = self.monster
            # get save
            if m['save']:
                save = 'Saves: ' + m['save']
                ts_strings.append(save)
            # get skill
            if m['skill']:
                skills = 'Skills: ' + m['skill']
                ts_strings.append(skills)
            # get resist
            if m['resist']:
                resist = 'Resists: ' + m['resist']
                ts_strings.append(resist)
            # get vulnerable
            if m['vulnerable']:
                vulnerable = 'Vulnerable: ' + m['vulnerable']
                ts_strings.append(vulnerable)
            # get immune
            if m['immune']:
                immune = 'Immune: ' + m['immune']
                ts_strings.append(immune)
            # get conditionImmune
            if m['conditionImmune']:
                conditionImmune = 'conditionImmune: ' + m['conditionImmune']
                ts_strings.append(conditionImmune)
            # get senses
            if m['senses']:
                senses = 'Senses: ' + m['senses']
                ts_strings.append(senses)
            # get passive
            if m['passive']:
                passive = 'Passive: ' + m['passive']
                ts_strings.append(passive)

            # get trait headings only
            # apparently some creatures are missing the <trait> tag
            # catch the exception here
            try:
                if m['trait']:
                    traits = m['trait']
                    if isinstance(traits, list):
                        for t in traits:
                            trait = t['name']
                            ts_strings.append(trait)
                    else:
                        trait = m['trait']['name']
                        ts_strings.append(trait)
            except:
                error_string = '{0} does not have a <trait> tag!'.format(m['name'])
                warnings.warn(error_string)
            # get if multiattack
            multiattack = ''
            if isinstance(m['action'], list):
                for action in m['action']:
                    if action['name'] == 'Multiattack':
                        multiattack = 'Multiattack: ' + action['text']

            ts_strings.append(multiattack)

            # check for legendary actions - get titles only
            if 'legendary' in self.monster:
                legendary =  self.monster['legendary']

                if isinstance (legendary, list):
                    for action in legendary:
                        ts_strings.append('(legendary)' + action['name'])
                else:
                    ts_strings.append('(legendary)' + legendary['name'])


            # get spells
            # spells is so big and massive that it is way beyond the scope of
            # this simple encounter sheet

            # get a refernce to what page the monster is listed at in mm
            page = self.monster['page']
            ts_strings.append('Page: ' + page)

            ts_string = ', '.join(ts_strings)
            traitsSkills.extend([('Features/Skills', ts_string)])

            return traitsSkills


        fields.extend(stats)
        fields.extend(stat_modifiers)
        fields.extend(info)
        fields.extend(getAttacks())
        fields.extend(getTraitsSkills())
        # add positional value to field data
        for idx,f in enumerate(fields):
            lst = list(f)
            lst[0] =' '.join([lst[0],str(position)])
            fields[idx] = tuple(lst)

        return fields


class EncounterData():

    def __init__(self, fields):
        '''
        # example of valid fields structure
        fields = [('Encounter Name','DRAGONS DRAGONS DRAGONS'),
                  ('Difficulty','Hard'),
                  ('XP Value',25),
                  ('Location','n/a'),
                  ('Monster Name 0','555-1234')]
        '''

        self.fdf_file = self._createFDF(fields)

    def _createFDF(self, fields):
        fdf = forge_fdf("",fields,[],[],[])
        fdf_file = tempfile.NamedTemporaryFile()
        fdf_file.write(fdf)
        fdf_file.seek(0) # need to rewind the file handle in order to read form it
        # remember to fdf_file.close() at the end of the program

        return fdf_file


    def getData(self):
        return self.fdf_file.name

    def close(self):
        self.fdf_file.close()


def runBashCommand(bashCommand):
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def getArgs():

    def required_length(nmin,nmax):
        class RequiredLength(argparse.Action):
            def __call__(self, parser, args, values, option_string=None):
                if not nmin<=len(values)<=nmax:
                    msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(f=self.dest,nmin=nmin,nmax=nmax)
                    raise argparse.ArgumentTypeError(msg)
                setattr(args, self.dest, values)
        return RequiredLength

    description = 'Fill out Encounter Sheet with monster data'
    parser = argparse.ArgumentParser(description=description)
    here = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument('monsters', nargs='+', action=required_length(1,3),
                        help='Provide 1 to 3 monster names from the monster manual')
    parser.add_argument('--pdf', type=file,
                        help='A pdf template file to fill out',
                        default = os.path.join(here,'combat_encounter_sheet.pdf'))
    parser.add_argument('--xml', type=file,
                        help='Xml file containing the monster data',
                        default= os.path.join(here, 'monsters.xml'))
    parser.add_argument('--open', action='store_true',
                        help='Opens the file when the program completes')
    parser.add_argument('-o', '--output',
                        help='The output filename',
                        default = os.path.join(os.getcwd(), 'output.pdf'))
    parser.add_argument('-v', '--verbose', action="store_true")
    parser.add_argument('--name', help='Name of the encounter',
                        default=None)
    parser.add_argument('--difficulty', help='Difficulty of the encounter',
                        default='Hard')
    parser.add_argument('--xp', help='xp value of the encounter',
                        default='')
    parser.add_argument('-loc', '--location', help='Location of the encounter',
                        default='')

    args = parser.parse_args()

    return args


def fillOutPdf(data_file, args):
    # define command for running pdftk

    commandString = 'pdftk {0} fill_form {1} output {2} flatten' # && open {2}'
    pdftkCommand = commandString.format(os.path.realpath(args.pdf.name),
                                        data_file,
                                        args.output)


    # define command for opening the created pdf
    openCommand = 'open ' + args.output

    # run the commands
    try:
        runBashCommand(pdftkCommand)
    except:
        raise Exception(NameError, 'pdftk is not installed on this system.' \
                        '\nSee: https://www.pdflabs.com/tools/pdftk-server/ ' \
                        'for instructions on how to install.')
    print "Writing {0}".format(args.output)
    if args.open:
        runBashCommand(openCommand)
