#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    DChars Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of DChars.
#    DChars is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DChars is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DChars.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏DChars❏ : dchars/languages/bod/syllabic_structure.py
"""

import itertools

################################################################################
# PREFIXES, SUFFIXES, etc.
#
# NB : the grammatical endings 'i, 'o, ... are not defined here but appear in
#      the code.
#
################################################################################
# ག ད བ	མ འ :
PREFIXES = (
                "G",
                "D",
                "B",
                "M",
                "-",
           )

# from http://vajranotes.wordpress.com/2011/10/31/the-tibetan-syllable/
SUPERFIXES = (
                "R",
                "L",
                "S",
             )

# from http://vajranotes.wordpress.com/2011/10/31/the-tibetan-syllable/
ROOT = (
                 'K',
                 'KH',
                 'G',
                 'NG',
                 'C',
                 'CH',
                 'J',
                 'NY',
                 'T',
                 'TH',
                 'D',
                 'N',
                 'P',
                 'PH',
                 'B',
                 'M',
                 'TS',
                 'TSH',
                 'DZ',
                 'W',
                 'ZH',
                 'Z',
                 '-',
                 'Y',
                 'R',
                 'L',
                 'SH',
                 'S',
                 'H',
                 'A',

                 'BH',
                 'GH',
                 'DH',
                 'DD',
                 'DDH',
                 'DZH',
                 'TT',
                 'TTH',
                 'NN',
                 'SS',
                 'KSS',
                 'KK',
                 'RR',
                 'TIB. TRANS. OF CHIN. SOUND F',
                 'TIB. TRANS. OF CHIN. SOUND V',
       )

# from http://vajranotes.wordpress.com/2011/10/31/the-tibetan-syllable/
SUBFIXES = (
                "Y",
                "R",
                "L",
                "W",
             )

# ག ང ད ན བ མ འ ར ལ ས :
SUFFIXES1 = (
                "G",
                "NG",
                "D",
                "N",
                "B",
                "M",
                "-",
                "R",
                "L",
                "S",
            )

# ས ད :
SUFFIXES2 = (
                "S",
                "D",
            )

# combinations of superfixes, roots and subfixes :
# the result takes in account the fact that the superfix/root/subfix can be missing
SUPERFIXES_ROOT_SUBFIXES = list(itertools.product(SUPERFIXES, ROOT)) + \
                           list(itertools.product(ROOT, SUBFIXES)) + \
                           list(itertools.product(SUPERFIXES, ROOT, SUBFIXES))

COMMON_CONSONANTS_STACK = (
# from http://www.thlib.org/reference/transliteration/tibstacks.php :

        # རྐརྒརྔརྗརྙརྟརྡརྣརྦརྨརྩརྫ (rka,rga,rnga,rja,rnya,rta,rda,rna,rba,rma,rtsa,rdza)
        ('R', 'K'),
        ('R', 'G'),
        ('R', 'NG'),
        ('R', 'J'),
        ('R', 'NY'),
        ('R', 'T'),
        ('R', 'D'),
        ('R', 'N'),
        ('R', 'B'),
        ('R', 'M'),
        ('R', 'TS'),
        ('R', 'DZ'),

        # ལྐལྒལྔལྕལྗལྟལྡལྤལྦལྷ (lka,lga,lnga,lca,lja,lta,lda,lpa,lba,lha)
        ('L', 'K'),
        ('L', 'G'),
        ('L', 'NG'),
        ('L', 'C'),
        ('L', 'J'),
        ('L', 'T'),
        ('L', 'D'),
        ('L', 'P'),
        ('L', 'B'),
        ('L', 'H'),

        # སྐསྒསྔསྙསྟསྡསྣསྤསྦསྨསྩ (ska,sga,snga,snya,sta,sda,sna,spa,sba,sma,stsa)
        ('S', 'K'),
        ('S', 'G'),
        ('S', 'NG'),
        ('S', 'NY'),
        ('S', 'T'),
        ('S', 'D'),
        ('S', 'N'),
        ('S', 'P'),
        ('S', 'B'),
        ('S', 'M'),
        ('S', 'TS'),

        # ཀྭཁྭགྭཅྭཉྭཏྭདྭཙྭཚྭཞྭཟྭ (kwa,khwa,gwa,cwa,nywa,twa,dwa,tswa,tshwa,zhwa,zwa)
        ('K', 'W'),
        ('KH','W'),
        ('G', 'Y'),
        ('C', 'Y'),
        ('N', 'Y', 'W'),
        ('T', 'W'),
        ('D', 'W'),
        ('TS','W'),
        ('TSH','W'),
        ('ZH','W'),
        ('Z', 'W'),

        # རྭཤྭསྭཧྭ (rwa,shwa,swa,hwa)
        ('R', 'W'),
        ('SH','W'),
        ('S', 'W'),
        ('H', 'W'),

        # ཀྱཁྱགྱཔྱཕྱབྱམྱ (kya,khya,gya,pya,phya,bya,mya)
        ('K', 'Y'),
        ('KH','Y'),
        ('G', 'Y'),
        ('P', 'Y'),
        ('PH','Y'),
        ('B', 'Y'),
        ('M', 'Y'),

        # ཀྲཁྲགྲཏྲཐྲདྲཔྲཕྲབྲམྲཤྲསྲཧྲ (kra,khra,gra,tra,thra,dra,pra,phra,bra,mra,shra,sra,hra)
        ('K', 'R'),
        ('KH','R'),
        ('G', 'R'),
        ('T', 'R'),
        ('TH','R'),
        ('D', 'R'),
        ('P', 'R'),
        ('PH','R'),
        ('B', 'R'),
        ('M', 'R'),
        ('SH','R'),
        ('S', 'R'),
        ('H', 'R'),

        # ཀླགླབླཟླརླསླ (kla,gla,bla,zla,rla,sla)
        ('K', 'L'),
        ('G','L'),
        ('B', 'L'),
        ('Z', 'L'),
        ('R', 'L'),
        ('S', 'L'),

        # རྐྱརྒྱརྨྱརྒྭརྩྭ (rkya,rgya,rmya,rgwa,rtswa)
        ('R', 'K', 'Y'),
        ('R', 'G', 'Y'),
        ('R', 'M', 'Y'),
        ('R', 'G', 'W'),
        ('R', 'TS','W'),

        # སྐྱསྒྱསྤྱསྦྱསྨྱ	(skya,sgya,spya,sbya,smya)
        ('S', 'K', 'Y'),
        ('S', 'G', 'Y'),
        ('S', 'P', 'Y'),
        ('S', 'B', 'Y'),
        ('S', 'M', 'Y'),

        # སྐྲསྒྲསྣྲསྤྲསྦྲསྨྲ (skra,sgra,snra,spra,sbra,smra)
        ('S', 'K', 'R'),
        ('S', 'G', 'R'),
        ('S', 'N', 'R'),
        ('S', 'P', 'R'),
        ('S', 'B', 'R'),
        ('S', 'M', 'R'),

        # གྲྭདྲྭཕྱྭ (grwa,drwa,phywa)
        ('G', 'R', 'W'),
        ('D', 'R', 'W'),
        ('PH','Y', 'W'),
       )

# source : http://www.tibet.columbia.edu/iats/it/IATS-X_Chilton_slides.pdf, slide 32
# prefixed + superfixed + root consonant
CHILTON_S_LIST = (
    (None,None,"K"),
    ("D", None,"K"),
    ("B", None,"K"),
    (None,"R", "K"),
    (None,"L", "K"),
    (None,"S", "K"),
    ("B", "R", "K",),
    ("B", "S", "K",),

    (None,None,"KH"),
    ("M", None,"KH"),
    ("-", None,"KH"),

    (None,None,"G"),
    ("D", None,"G"),
    ("B", None,"G"),
    ("M", None,"G"),
    ("-", None,"G"),
    (None,"R", "G"),
    (None,"L", "G"),
    (None,"S", "G"),
    ("B", "R", "G"),
    ("B", "S", "G"),
    
    (None,"NG",None),
    ("D", "NG",None),
    ("M", "NG",None),
    ("R", "NG",None),
    ("L", "NG",None),
    ("S", "NG",None),
    ("B", "R", "NG",),
    ("B", "S", "NG",),

    (None,None,"C"),
    ("G", None,"C"),
    ("B", None,"C"),
    ("L", None,"C"),
    ("B", "L", "C",),

    (None,None,"CH"),
    ("M", None,"CH"),
    ("-", None,"CH"),

    (None,None,"J"),
    ("M", None,"J"),
    ("-", None,"J"),
    (None,"R", "J"),
    (None,"L", "J"),
    ("B", "R", "J",),

    (None,None,"NY"),
    ("G", None,"NY"),
    ("M", None,"NY"),
    (None,"R", "NY"),
    (None,"S", "NY"),
    ("B", "R", "NY",),
    ("B", "S", "NY",),

    (None,None,"T"),
    ("G", None,"T"),
    ("B", None,"T"),
    (None,"R", "T"),
    (None,"L", "T"),
    (None,"S", "T"),
    ("B", "R", "T",),
    ("B", "L", "T",),
    ("B", "S", "T",),

    (None,None,"TH"),
    ("M", None,"TH"),
    ("-", None,"TH"),

    (None,None,"D"),
    ("G", None,"D"),
    ("B", None,"D"),
    ("M", None,"D"),
    ("-", None,"D"),
    (None,"R", "D"),
    (None,"L", "D"),
    (None,"S", "D"),
    ("B", "R", "D",),
    ("B", "L", "D",),
    ("B", "S", "D",),

    (None,None,"N"),
    ("G", None,"N"),
    ("M", None,"N"),
    (None,"R", "N"),
    (None,"S", "N"),
    ("B", "R", "N",),
    ("B", "S", "N",),

    (None,None,"P"),
    ("D", None,"P"),
    (None,"L", "P"),
    (None,"S", "P"),

    (None,None,"PH"),
    ("-", None,"PH"),

    (None,None,"B"),
    ("D", None,"B"),
    ("-", None,"B"),
    (None,"R", "B"),
    (None,"L", "B"),
    (None,"S", "B"),

    (None,None,"M"),
    ("D", None,"M"),
    (None,"R", "M"),
    (None,"S", "M"),

    (None,None,"TS"),
    ("G",None, "TS"),
    ("B",None, "TS"),
    (None,"R", "TS"),
    (None,"S", "TS"),
    ("B", "R", "TS",),
    ("B", "S", "TS",),

    (None,None,"TSH"),
    ("M", None,"TSH"),
    ("-", None,"TSH"),

    (None,None,"DZ"),
    ("M", None,"DZ"),
    ("-", None,"DZ"),
    (None,"R", "DZ"),
    ("B", "R", "DZ",),

    (None,None,"W"),

    (None,None,"ZH"),
    ("G", None,"ZH"),
    ("B", None,"ZH"),

    (None,None,"Z"),
    ("G", None,"Z"),
    ("B", None,"Z"),

    (None,None,"-"),

    (None,None,"Y"),
    ("G", None,"Y"),

    (None,None,"R"),
    ("B", None,"R"),

    (None,None,"L"),

    (None,None,"SH"),
    ("G", None,"SH"),
    ("B", None,"SH"),

    (None,None,"S"),
    ("G", None,"S"),
    ("B", None,"S"),

    (None,None,"H"),
    (None,"L", "H"),

    (None, None, "A"),
)
