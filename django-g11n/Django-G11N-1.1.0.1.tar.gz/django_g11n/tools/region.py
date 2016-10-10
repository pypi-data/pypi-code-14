"""
Region data from UN statistics division publication M49 as found in the URL.
The page isn't well structured so instead of transforming the table data and
having a lot of exceptions, just copy over the content and have a mechanism to
detect changes.
"""
URL = "http://unstats.un.org/unsd/methods/m49/m49regin.htm"
HASH = "40f5450a6386f90414d5233c9fcc5163"

# Two codes, the left code is the parent, the right the child.
DATA = """
001 World 
   002 Africa
   019 Americas
   142 Asia
   150 Europe
   009 Oceania

002 Africa
   014 Eastern Africa
   017 Middle Africa
   015 Northern Africa
   018 Southern Africa
   011 Western Africa

019 Americas
   419 Latin America and the Carribbean
   021 Northern America

419 Latin America and the Carribbean
   029 Carribbean
   013 Central America
   005 South America

142 Asia
   143 Central Asia
   030 Eastern Asia
   034 Southern Asia
   035 Southern-Eastern Asia
   145 Western Asia

150 Europe
   151 Eastern Europe
   154 Northern Europe
   039 Southern Europe
   155 Western Europe

009 Ocenia
   053 Australia and New Zealand
   054 Melanesia
   057 Micronesia
   061 Polynesia

014 Eastern Africa
   108 Burundi
   174 Comoros
   262 Djibouti
   232 Eritrea
   231 Ethiopia
   404 Kenya
   450 Madagascar
   454 Malawi
   480 Mauritius
   175 Mayotte
   508 Mozambique
   638 Réunion
   646 Rwanda
   690 Seychelles
   706 Somalia
   728 South Sudan
   800 Uganda
   834 United Republic of Tanzania
   894 Zambia
   716 Zimbabwe

017 Middle Africa 
   024 Angola
   120 Cameroon
   140 Central African Republic
   148 Chad
   178 Congo
   180 Democratic Republic of the Congo
   226 Equatorial Guinea
   266 Gabon
   678 Sao Tome and Principe

015 Northern Africa
   012 Algeria
   818 Egypt
   434 Libya
   504 Morocco
   729 Sudan
   788 Tunisia
   732 Western Sahara
       
018 Southern Africa
   072 Botswana
   426 Lesotho
   516 Namibia
   710 South Africa
   748 Swaziland
       
011 Western Africa
   204 Benin
   854 Burkina Faso
   132 Cabo Verde
   384 Cote d'Ivoire
   270 Gambia
   288 Ghana
   324 Guinea
   624 Guinea-Bissau
   430 Liberia
   466 Mali
   478 Mauritania
   562 Niger
   566 Nigeria
   654 Saint Helena
   686 Senegal
   694 Sierra Leone
   768 Togo

029 Caribbean
   660 Anguilla
   028 Antigua and Barbuda
   533 Aruba
   044 Bahamas
   052 Barbados
   535 Bonaire, Sint Eustatius and Saba
   092 British Virgin Islands
   136 Cayman Islands
   192 Cuba
   531 Curaçao
   212 Dominica
   214 Dominican Republic
   308 Grenada
   312 Guadeloupe
   332 Haiti
   388 Jamaica
   474 Martinique
   500 Montserrat
   630 Puerto Rico
   652 Saint-Barthélemy
   659 Saint Kitts and Nevis
   662 Saint Lucia
   663 Saint Martin (French part)
   670 Saint Vincent and the Grenadines
   534 Sint Maarten (Dutch part)
   780 Trinidad and Tobago
   796 Turks and Caicos Islands
   850 United States Virgin Islands
      
013 Central America
   084 Belize
   188 Costa Rica
   222 El Salvador
   320 Guatemala
   340 Honduras
   484 Mexico
   558 Nicaragua
   591 Panama
      
005 South America
   032 Argentina
   068 Bolivia (Plurinational State of)
   076 Brazil
   152 Chile
   170 Colombia
   218 Ecuador
   238 Falkland Islands (Malvinas)
   254 French Guiana
   328 Guyana
   600 Paraguay
   604 Peru
   740 Suriname
   858 Uruguay
   862 Venezuela (Bolivarian Republic of)
      
021 Northern America
   060 Bermuda
   124 Canada
   304 Greenland
   666 Saint Pierre and Miquelon
   840 United States of America
      
143 Central Asia
   398 Kazakhstan
   417 Kyrgyzstan
   762 Tajikistan
   795 Turkmenistan
   860 Uzbekistan
      
030 Eastern Asia
   156 China
   344 China, Hong Kong Special Administrative Region
   446 China, Macao Special Administrative Region
   408 Democratic People's Republic of Korea
   392 Japan
   496 Mongolia
   410 Republic of Korea
      
034 Southern Asia
   004 Afghanistan
   050 Bangladesh
   064 Bhutan
   356 India
   364 Iran (Islamic Republic of)
   462 Maldives
   524 Nepal
   586 Pakistan
   144 Sri Lanka
      
035 South-Eastern Asia   
    096 Brunei Darussalam
    116 Cambodia
    360 Indonesia
    418 Lao People's Democratic Republic
    458 Malaysia
    104 Myanmar
    608 Philippines
    702 Singapore
    764 Thailand
    626 Timor-Leste
    704 Viet Nam

145 Western Asia
   051 Armenia
   031 Azerbaijan
   048 Bahrain
   196 Cyprus
   268 Georgia
   368 Iraq
   376 Israel
   400 Jordan
   414 Kuwait
   422 Lebanon
   512 Oman
   634 Qatar
   682 Saudi Arabia
   275 State of Palestine
   760 Syrian Arab Republic
   792 Turkey
   784 United Arab Emirates
   887 Yemen

151 Eastern Europe
   112 Belarus
   100 Bulgaria
   203 Czechia
   348 Hungary
   616 Poland
   498 Republic of Moldova
   642 Romania
   643 Russian Federation
   703 Slovakia
   804 Ukraine
      
154 Northern Europe
   248 Åland Islands
   830 Channel Islands
   208 Denmark
   233 Estonia
   234 Faeroe Islands
   246 Finland
   831 Guernsey
   352 Iceland
   372 Ireland
   833 Isle of Man
   832 Jersey
   428 Latvia
   440 Lithuania
   578 Norway
   680 Sark
   744 Svalbard and Jan Mayen Islands
   752 Sweden
   826 United Kingdom of Great Britain and Northern Ireland
      
039 Southern Europe
   008 Albania
   020 Andorra
   070 Bosnia and Herzegovina
   191 Croatia
   292 Gibraltar
   300 Greece
   336 Holy See
   380 Italy
   470 Malta
   499 Montenegro
   620 Portugal
   674 San Marino
   688 Serbia
   705 Slovenia
   724 Spain
   807 The former Yugoslav Republic of Macedonia
      
155 Western Europe
   040 Austria
   056 Belgium
   250 France
   276 Germany
   438 Liechtenstein
   442 Luxembourg
   492 Monaco
   528 Netherlands
   756 Switzerland

053 Australia and New Zealand
   036 Australia
   554 New Zealand
   574 Norfolk Island
      
054 Melanesia
   242 Fiji
   540 New Caledonia
   598 Papua New Guinea
   090 Solomon Islands
   548 Vanuatu
      
057 Micronesia
   316 Guam
   296 Kiribati
   584 Marshall Islands
   583 Micronesia (Federated States of)
   520 Nauru
   580 Northern Mariana Islands
   585 Palau
      
061 Polynesia
   016 American Samoa
   184 Cook Islands
   258 French Polynesia
   570 Niue
   612 Pitcairn
   882 Samoa
   772 Tokelau
   776 Tonga
   798 Tuvalu
   876 Wallis and Futuna Islands

199 Least developed countries 
   004 Afghanistan
   024 Angola
   050 Bangladesh
   204 Benin
   064 Bhutan
   854 Burkina Faso
   108 Burundi
   116 Cambodia
   140 Central African Republic
   148 Chad
   174 Comoros
   180 Democratic Republic of the Congo
   262 Djibouti
   226 Equatorial Guinea
   232 Eritrea
   231 Ethiopia
   270 Gambia
   324 Guinea
   624 Guinea Bissau
   332 Haiti
   296 Kiribati
   418 Lao People's Democratic Republic
   426 Lesotho
   430 Liberia
   450 Madagascar
   454 Malawi
   466 Mali
   478 Mauritania
   508 Mozambique
   104 Myanmar
   524 Nepal
   562 Niger
   646 Rwanda
   678 Sao Tome and Principe
   686 Senegal
   694 Sierra Leone
   090 Solomon Islands
   706 Somalia
   728 South Sudan
   729 Sudan
   626 Timor-Leste
   768 Togo
   798 Tuvalu
   800 Uganda
   834 United Republic of Tanzania
   548 Vanuatu
   887 Yemen
   894 Zambia

432 Landlocked developing countries 
   004 Afghanistan
   051 Armenia
   031 Azerbaijan
   064 Bhutan
   068 Bolivia (Plurinational State of)
   072 Botswana
   854 Burkina Faso
   108 Burundi
   140 Central African Republic
   148 Chad
   231 Ethiopia
   398 Kazakhstan
   417 Kyrgyzstan
   418 Lao People's Democratic Republic
   426 Lesotho
   454 Malawi
   466 Mali
   496 Mongolia
   524 Nepal
   562 Niger
   600 Paraguay
   498 Republic of Moldova
   646 Rwanda
   728 South Sudan
   748 Swaziland
   762 Tajikistan
   807 The former Yugoslav Republic of Macedonia
   795 Turkmenistan
   800 Uganda
   860 Uzbekistan
   894 Zambia
   716 Zimbabwe

722 Small island developing States 
   016 American Samoa
   660 Anguilla
   028 Antigua and Barbuda
   533 Aruba
   044 Bahamas
   052 Barbados
   084 Belize
   092 British Virgin Islands
   132 Cabo Verde
   174 Comoros
   184 Cook Islands
   192 Cuba
   212 Dominica
   214 Dominican Republic
   242 Fiji
   258 French Polynesia
   308 Grenada
   316 Guam
   624 Guinea-Bissau
   328 Guyana
   332 Haiti
   388 Jamaica
   296 Kiribati
   462 Maldives
   584 Marshall Islands
   480 Mauritius
   583 Micronesia (Federated States of)
   500 Montserrat
   520 Nauru
   540 New Caledonia
   570 Niue
   580 Northern Mariana Islands
   585 Palau
   598 Papua New Guinea
   630 Puerto Rico
   659 Saint Kitts and Nevis
   662 Saint Lucia
   882 Samoa
   678 Sao Tome and Principe
   690 Seychelles
   702 Singapore
   090 Solomon Islands
   670 Saint Vincent and the Grenadines
   740 Suriname
   626 Timor-Leste
   776 Tonga
   780 Trinidad and Tobago
   798 Tuvalu
   850 United States Virgin Islands
   548 Vanuatu
"""

def get():
    """
    Returns a dictionary and a list of tuples.
    The dictionary keys are the 3 digit numbers as used by the UN Statistics
    office and the value is the US-English country name. The numbers are based
    on the ISO 31661-1 numeric codes, with addition of codes representing
    regions (these are not in the ISO standard).

    The list of tuples is (region, country), however instead of the name the
    number is used.

    As some of the numbers have leading zero's that have to be preserved, we
    keep it as a string instead of an integer.
    """
    data = {'name':dict(),
            'hier':list()}
    lines = DATA.split('\n')
    parent = None
    for line in lines:
        if len(line.strip()) == 0:
            continue

        number, name = line.strip().split(' ', 1)

        if number not in data['name']:
            data['name'][number] = name

        if not line.startswith('   '):
            parent = number
        else:
            data['hier'].append((parent, number))

    return data['name'], data['hier']

