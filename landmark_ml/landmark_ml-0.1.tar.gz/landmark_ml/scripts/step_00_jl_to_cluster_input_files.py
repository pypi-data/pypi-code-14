import sys
import getopt
import os
import codecs
import json
import shutil
import subprocess

def prep_for_clustering(input_directory, tld_json_lines_file, output_directory):
    tld_name = tld_json_lines_file[:-3]
    tld_directory = os.path.join(output_directory, tld_name)
    
    cdr_dir = os.path.join(tld_directory, "cdr")
    if os.path.exists(cdr_dir):
        shutil.rmtree(cdr_dir)
    os.makedirs(cdr_dir)
        
    html_dir = os.path.join(tld_directory, "html")
    if os.path.exists(html_dir):
        shutil.rmtree(html_dir)
    os.makedirs(html_dir)
    
    file_loc = os.path.join(input_directory, tld_json_lines_file)
    p = subprocess.Popen(['shuf', '-n', '20000', file_loc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    
    count = 1
    ad_count = 0
    for real_line in output.splitlines():
        line = real_line.strip()
        if line:
            try:
                crawl_page = json.loads(line)
#                 if not crawl_page['content_type'].startswith('image'):
                if 'raw_content' in crawl_page:
                    print crawl_page['_id']
                    if 'Views:' in crawl_page['raw_content']:
                        ad_count += 1
                    elif ad_count < 20:
                        continue
                    
                    print ad_count
                    
                    with codecs.open(os.path.join(cdr_dir, crawl_page['_id']+'.json'), "w", "utf-8") as output_file:
                        output_file.write(line)
                        output_file.close()
                        
                    with codecs.open(os.path.join(html_dir, crawl_page['_id']+'.html'), "w", "utf-8") as output_file:
                        output_file.write(crawl_page['raw_content'])
                        output_file.close()
                        
                    count += 1
                    if count == 200:
                        break
                        
            except:
                print ('skipping line ...')
                print json.dumps(crawl_page)

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            for opt in opts:
                if opt in [('-h', ''), ('--help', '')]:
                    raise Usage('python step_00_jl_to_cluster_input_files [INPUT_DIR] [OUTPUT_DIR] [SLD_FILE]')
            
            if len(args) == 3:
                input_directory = args[0]
                output_dir_count = 1
                output_directory_base = args[1]
                sld_file = args[2]
                with codecs.open(sld_file, "r", "utf-8") as myfile:
                    sld_count = 0
                    for line in myfile:
                        sld, count = line.split(':')
#                         count = int(count)
#                         if count > 10:
                        if sld == 'escort-ads.com':
                            jl_file = sld + ".jl"
                            print '...prepping ' + jl_file
                            prep_for_clustering(input_directory, jl_file, output_directory_base)
                        print 'done with ' + sld
                
            else:
                raise Usage('python step_00_jl_to_cluster_input_files [INPUT_DIR] [OUTPUT_DIR]')
            
        except getopt.error, msg:
            raise Usage(msg)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())