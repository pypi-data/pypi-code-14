import sys
import getopt
import json
import codecs
import os
import urllib
import cgi
from landmark_extractor.extraction.Landmark import RuleSet

INDEX_TEMPLATE = '\
<!DOCTYPE html>\
<html>\
<head>\
    <title>[[TITLE]]</title>\
    <script src="jquery.1.11.2.js" type="text/javascript"></script>\
    <script src="bootstrap.min.3.3.1.js" type="text/javascript"></script>\
    <script src="jquery.watable.js" type="text/javascript" charset="utf-8"></script>\
    <link rel="stylesheet" href="bootstrap.min.3.3.1.css" />\
    <link rel="stylesheet" href="watable.css"/>\
    <style type="text/css">\
        body { padding: 30px; font-size: 12px }\
        .watable * {white-space: inherit !important;}\
    </style>\
</head>\
<body>\
    <h2>[[TITLE]]</h2>\
    <div id="example1" style="width:auto"></div>\
    <script type="text/javascript">\
        var cols =\
            [[COLUNMS]];\
        var rows =\
            [[ROWS]];\
        var data = {\
            cols: cols,\
            rows: rows\
        };\
        $(document).ready( function() {\
                $("#example1").WATable({\
                    data: data,\
                    pageSizes: [10,25,50,100,250],\
                    columnPicker: true\
                });\
        });\
    </script>\
</body>\
</html>'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def run_extraction_check(page_file_dir, output_dir, rules, show_empties = True, is_cdr_format = False):
    output_str = os.path.join(os.path.abspath(output_dir), 'eval.html')
    
    titles = rules.names()
    titles.insert(0, 'page')
    
    cols = {}
    rows = []
        
    total_count = 0
    counts = {}
    for name in rules.names():
        counts[name] = 0
    
    files = [f for f in os.listdir(page_file_dir) if os.path.isfile(os.path.join(page_file_dir, f))]
    for the_file in files:
        if the_file.startswith('.'):
            continue
        
        with codecs.open(os.path.join(page_file_dir, the_file), "r", "utf-8") as myfile:
            if is_cdr_format:
                cdr_str = myfile.read().encode('utf-8')
                page_str = json.loads(cdr_str)['raw_content']
            else:
                page_str = myfile.read().encode('utf-8')
        total_count = total_count + 1
        
        extraction = rules.extract(page_str)
#                 if not rules.validate(extraction):
#                     continue
        
        results = []
        results.append(urllib.unquote(the_file))
        
        row = {}
        row['page'] = os.path.abspath(page_file_dir)+"/"+urllib.pathname2url(the_file)
#                 row['page'] = subdir+"/"+urllib.pathname2url(the_file)
        
        for name in rules.names():
            found = False
            if name in extraction:
                if extraction[name]:
                    extract = extraction[name]['extract']
                    if 'sequence' in extraction[name]:
                        extract = 'LIST<br>----<br>'
                        for sequence_extract in extraction[name]['sequence']:
                            extract = extract + cgi.escape(str(sequence_extract['sequence_number']) + ') ' + sequence_extract['extract']) + '<br>'
                    else:
                        extract = cgi.escape(extract)
                    
                    if extract:
                        results.append(extract)
                        row[name] = extract
                        counts[name] = counts[name] + 1
                        found = True
                    
            if not found:
                row[name] = ''
                key = name+'Cls'
                row[key] = 'red'
                results.append('NULL')
                
#                 wr.writerow(results)
        rows.append(row)
    
    #make the cols for the UI
    index = 1
    for title in titles:
        col = {}
        col['index'] = index
        col['type'] = 'string'
        
        if index == 1:
            col['sortOrder'] = 'asc'
            col['format'] = '<span style="word-break:break-all;"><a href="file://{0}" target="_blank">{0}</a></span>'
        else:
            col['friendly'] = title + ' [' + str(counts[title]) + '/' + str(total_count) +']'
            col['tooltip'] = rules.get(title).toolTip()
        cols[title] = col
        
        index = index + 1
    
    index_output = INDEX_TEMPLATE.replace('[[TITLE]]', page_file_dir).replace('[[COLUNMS]]', json.dumps(cols)).replace('[[ROWS]]', json.dumps(rows))
    
    with codecs.open(output_str, "w", "utf-8") as myfile:
        myfile.write(index_output)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        
        #read the directory location from arg0
        page_file_dir = args[0]
        
        output_dir = args[1]
        
        #read the rules from arg1
        json_file_str = args[2]
        with codecs.open(json_file_str, "r", "utf-8") as myfile:
            json_str = myfile.read().encode('utf-8')
        
        json_object = json.loads(json_str)
        rules = RuleSet(json_object)
        
        run_extraction_check(page_file_dir, output_dir, rules)
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())