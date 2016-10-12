import sys
import getopt
import codecs
from landmark_ml.learning.PageManager import PageManager
import os
import difflib

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def loadCluster(cluster_dir):
    page_manager = PageManager()
    files = [f for f in os.listdir(cluster_dir) if os.path.isfile(os.path.join(cluster_dir, f))]
    for the_file in files:
        if not the_file.endswith('html'):
            continue
        with codecs.open(os.path.join(cluster_dir, the_file), "r", "utf-8") as myfile:
            page_str = myfile.read().encode('utf-8')
        page_manager.addPage(the_file, page_str)
    page_manager.learnStripes()
    return page_manager

def mergeClusters(page_manager_1, page_manager_2):
    page_manager = PageManager()
    for page_id in page_manager_1._pages:
        page_manager.addPage(page_id, page_manager_1.getPage(page_id).getString(), add_special_tokens=False)
    for page_id in page_manager_2._pages:
        page_manager.addPage(page_id, page_manager_2.getPage(page_id).getString(), add_special_tokens=False)
    page_manager.learnStripes()
    return page_manager

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        
        #read the directory locations from args
        cluster_1_dir = args[0]
        cluster_2_dir = args[1]
        
        working = cluster_1_dir
        while not working.endswith('/clusters'):
            (working,other) = os.path.split(working)
        
        cluster_1_pm = loadCluster(cluster_1_dir)
        with codecs.open(os.path.join(working, 'cluster_1_stripes.txt'), "w", "utf-8") as myfile:
            for stripe in cluster_1_pm._stripes:
                myfile.write(str(stripe))
                myfile.write('\n')
        
        cluster_2_pm = loadCluster(cluster_2_dir)
        with codecs.open(os.path.join(working, 'cluster_2_stripes.txt'), "w", "utf-8") as myfile:
            for stripe in cluster_2_pm._stripes:
                myfile.write(str(stripe))
                myfile.write('\n')
                
        merged_pm = mergeClusters(cluster_1_pm, cluster_2_pm)
        with codecs.open(os.path.join(working, 'cluster_merged_stripes.txt'), "w", "utf-8") as myfile:
            for stripe in merged_pm._stripes:
                myfile.write(str(stripe))
                myfile.write('\n')
                
        with codecs.open(os.path.join(working, 'cluster_1_stripes.txt'), 'r', "utf-8") as file_1:
            with codecs.open(os.path.join(working, 'cluster_merged_stripes.txt'), 'r', "utf-8") as file_merged:
                diff = difflib.unified_diff(
                    file_1.readlines(),
                    file_merged.readlines(),
                    fromfile='cluster_1_stripes.txt',
                    tofile='cluster_merged_stripes.txt',
                )
                for line in diff:
                    sys.stdout.write(line)
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())