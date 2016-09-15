# -*- coding: utf-8 -*-

import  requests



url = 'http://roll.sohu.com/sports_bak/'
s = requests.session()
r = s.get(url)
r.encoding = "utf-8"
print r.content
