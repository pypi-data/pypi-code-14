import sys
import getopt
import os
import codecs
import json
import shutil

def jl_to_html_and_json(json_lines_file, output_directory):
    cdr_dir = os.path.join(output_directory, "cdr")
    if os.path.exists(cdr_dir):
        shutil.rmtree(cdr_dir)
    os.makedirs(cdr_dir)
        
    html_dir = os.path.join(output_directory, "html")
    if os.path.exists(html_dir):
        shutil.rmtree(html_dir)
    os.makedirs(html_dir)
    
    with codecs.open(json_lines_file, "r", "utf-8") as jl_file:
        for line in jl_file.read().splitlines():
            if line:
                try:
                    crawl_page = json.loads(line)
                    with codecs.open(os.path.join(cdr_dir, crawl_page['_id']+'.json'), "w", "utf-8") as output_file:
                        output_file.write(line)
                        output_file.close()
                    
                    with codecs.open(os.path.join(html_dir, crawl_page['_id']+'.html'), "w", "utf-8") as output_file:
                        output_file.write(crawl_page['raw_content'])
                        output_file.close()
            
                except:
                    print ('skipping line ...')
                    print line
            else:
                break
        
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            for opt, arg in opts:
                if opt in [('-h', ''), ('--help', '')]:
                    raise Usage('python jl_to_html_and_json -l limit [JL_FILE]')
            
            if len(args) == 1:
                jl_file = args[0]
                dir_path = os.path.dirname(os.path.realpath(jl_file))
                jl_to_html_and_json(jl_file, dir_path)
            else:
                raise Usage('python jl_to_html_and_json -l limit [JL_FILE]')
            
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())