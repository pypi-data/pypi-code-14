#!/usr/bin/env python

from zezfio.babel import type_fortran2c 
from collections import defaultdict

import re
import sys

magic_split_line_regex_dim=re.compile(r' +(\w*) +(.*?)( \(.*\) ?)?$')
magic_split_line_regex_formula=re.compile(r'^ +(\w+) +(.*?)\s*=(.+)?$')


def one_dwarf(path):
    with open(path,"r") as f:
        data = f.read()
    
    l_block = [block for block in re.split('\n\s*\n', data) if block]
    
    json_data = defaultdict(dict)
    
    for block in l_block:
        l_ligne = [ i for i in block.split("\n") if i ]

        category = l_ligne[0]
    
        l_attribute = []
    
        for attribute in l_ligne[1:]:
    
            info = dict()
            
            if "=" not in attribute:
                l_var = [v.strip() for v in re.findall(magic_split_line_regex_dim,attribute)[0] if v]

                info["name"] = l_var[0]
                info["type"] = type_fortran2c(l_var[1])
        
                try:
                    info["shape"] = "[%s]" % l_var[2][1:-1]
                except IndexError:
                    pass
            else:

                l_var = re.findall(magic_split_line_regex_formula,attribute)[0]

                info["name"] = l_var[0]
                info["type"] = type_fortran2c(l_var[1])
                info["default"] = l_var[2]
                info["default"] = info["default"].replace("maxval","max")
                info["default"] = info["default"].replace("minval","min")
        
            l_attribute.append(info)
        
        json_data[category]["attributes"] = l_attribute

    return json_data


def stz_dim_array(shape, list_category):
    for category in list_category:
        old = "%s_"%category
        new = "%s."%category
        shape = re.sub(r"\b%s"%old,new,shape)

    return shape



def schneewittchen(l_file):
    d = dict()
    for path in l_file:   
        d.update(one_dwarf(path))  

    return d

def magic_mirror(data):
    list_category = data.keys()
    for category,attributes in data.iteritems():
        for var in attributes["attributes"]:

            try:
                var["shape"] = stz_dim_array(var["shape"],list_category)
            except:
                pass

            try:
                var["default"] = stz_dim_array(var["default"],list_category)
            except KeyError:
                pass

if __name__ == '__main__':
    

    data = schneewittchen(sys.argv[1:])
    magic_mirror(data)

    import json
    print json.dumps(data,  indent = 4)
