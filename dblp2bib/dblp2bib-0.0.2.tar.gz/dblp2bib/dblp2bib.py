"""
    Downloads the DBLP XML file, and creates a .bib file for all conferences / workshops / journals you are interested in
"""

"""
    Imports
"""
from os.path import exists, join      # for checking whether certain path/files exist
from os      import mkdir,stat,remove  # creating files and checking their attributes, cleaning up downloads
import sys
import argparse     # for parsing command line options
import urllib # for downloading a file
import gzip # for uncompressing the dblp xml file
import hashlib # for verifying md5 digest
from shutil import rmtree # for clearing output diretory
from lxml import etree # for xml parsing
from bibtexparser.bwriter import BibTexWriter # writing bibtex files
from bibtexparser.bibdatabase import BibDatabase # writing bibtex files

"""
    Constants
"""
DBLP_XML_FILE_URL = "http://dblp.uni-trier.de/xml/dblp.xml.gz"
DBLP_XML_DTD_FILE_URL="http://dblp.uni-trier.de/xml/dblp.dtd"
DBLP_XML_FILE_CHECKSUM_URL = "http://dblp.uni-trier.de/xml/dblp.xml.gz.md5"
DBLP_ROOT_URL = "http://dblp.uni-trier.de/"

"""
    Arguments
"""
parser = argparse.ArgumentParser(description='Download sample directories to use as source for decoy dirs')
parser.add_argument('-dd', '--data_dir', type=str, default="data", help='Directory to download the DBLP XML file to')
parser.add_argument('-sf', '--sources_file', type=str, default="security.list", help='Textfile that contains all conferences / journals / workshops that you are interested in')
parser.add_argument('-od', '--out_dir', type=str, default=None, help="Directory to store the extracted .bib files.")
args = parser.parse_args()

DATA_DIR = args.data_dir
SOURCES_FILE = args.sources_file
OUT_DIR = args.out_dir if args.out_dir else SOURCES_FILE.replace(".list","")

"""
    TODO error checks.
    TODO checking available space
    TODO check md5 from downloaded file
"""

"""
    Helpers
"""
def create_dir_if_not_exists(dir_path):
    if not exists(dir_path): mkdir(dir_path)

def file_exists(file_path):
    if not exists(file_path):
        return False
    if stat(file_path).st_size <= 0:
        return False
    return True

def filename_for(entry):
    volume = entry["volume"] if ("volume" in entry) else None
    year = entry["year"]
    key = entry["ID"].split("/")[1]
    if volume:
        name = key+"_"+year+"_"+volume+".bib"
    else:
        name = key+"_"+year+".bib"
    return join(OUT_DIR,key,name) # OUTDIR/ccs/ccs_2012_34.bib


def print_progress (iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        print("\n")

"""
    Setup
    * create necessary directories if they don't exist
    * download dblp xml database, verify checksum
    * unzip it and clean up zip files
"""
# creating data directory and output directory
print("Creating directories if not exist...")
create_dir_if_not_exists( DATA_DIR )
print("Done.\n")

# define filenames
dblp_xml_gz_file = join(DATA_DIR, "dblp.xml.gz")
dblp_xml_gz_file_checksum = join(DATA_DIR, "dblp.xml.gz.md5")
dblp_xml_name = join(DATA_DIR, "dblp.xml")
dblp_xml_dtd = join(DATA_DIR, "dblp.dtd")

# download dblp xml file if not exists
if not file_exists(dblp_xml_gz_file) and not file_exists(dblp_xml_name):
    print("Downloading DBPL XML file, this might take a while...")
    urllib.request.urlretrieve(DBLP_XML_FILE_URL , dblp_xml_gz_file)
    print("Done.\n")

if not file_exists(dblp_xml_dtd):
    print("Downloading DBPL XML document type, this might take a while...")
    urllib.request.urlretrieve(DBLP_XML_DTD_FILE_URL , dblp_xml_dtd)
    print("Done.\n")


# download checksum if not exists
if not file_exists(dblp_xml_gz_file_checksum) and not file_exists(dblp_xml_name):
    print("Downloading DBPL XML CHECKSUM file...")
    urllib.request.urlretrieve(DBLP__XML_FILE_CHECKSUM_URL, dblp_xml_gz_file_checksum)
    print("Done.\n")

# veryifying checksum
if not file_exists(dblp_xml_name):
    print("Verifying checksum...")
    calculated_checksum = SOURCES_FILEhashlib.md5(open(dblp_xml_gz_file,'rb').read()).hexdigest()
    downloaded_checksum = open(dblp_xml_gz_file_checksum).read().split(" ")[0]
    if not (calculated_checksum == downloaded_checksum):
        print("Download failed because checksums did not matched. (calculated=%s,downloaded=%s)"%(calculated_checksum, downloaded_checksum))
        print("Remove files in '%s' directory and try again"%DATA_DIR)
        sys.exit(5)# I/O error
    print("Ok.\n")

# unzip file TODO add progress bar

    print("Decompressing dblp xml file, this might take a while...")
    with open(dblp_xml_name, "wb") as dblp_xml_file:
        for line in gzip.open(dblp_xml_gz_file, 'rb'):
            dblp_xml_file.write(line)
    print("Done.\n")

# remove zip file
if not file_exists(dblp_xml_name):
    print("Cleaning up...")
    remove(dblp_xml_gz_file)
    remove(dblp_xml_gz_file_checksum)
    print("Done.\n")

"""
    Load Sources
    * clear output directory
    * open sources file
"""
# clear output directory and create it
if (exists(OUT_DIR)): rmtree(OUT_DIR)
mkdir(OUT_DIR)

# open sources file
if not exists(SOURCES_FILE):
    open(SOURCES_FILE,"w").close()
    print("'%s' not found. Created."%SOURCES_FILE)
    print("Please populate '%s'. Add conference/journal keys to extract, one per line. optionally you can add a rank." % (SOURCES_FILE))
    print("Example: 'dbsec|Rank A'")
    sys.exit(5)

interested_in_list = open(SOURCES_FILE,"r").readlines()
if len(interested_in_list)==0:
    print("'%s' is empty."%SOURCES_FILE)
    print("Please populate '%s'. Add conference/journal keys to extract, one per line. optionally you can add a rank." % (SOURCES_FILE) )
    print("Example: 'dbsec|RankAA'")
    sys.exit(5)

# convert to hash
interested_in = {}
for line in interested_in_list:
    if line.startswith("#"): continue # comments
    if "|" in line:
        key,rank = line.split("|")
        interested_in[key] = rank.replace("\n","")
    else:
        interested_in[line.replace("\n","")]=""

print("Loaded %s conferences/journals/workshops of interest from '%s'" % (len(interested_in),SOURCES_FILE))
print(interested_in)

# create directories for each conference / journal / workshop
for k,v in interested_in.items():
    create_dir_if_not_exists(join(OUT_DIR,k))

"""
    Main Loop
    * open XML. for each article:
    * export article to .bib files if interested
"""
filesize = stat(dblp_xml_name).st_size

# TODO think of the case what happens when journal has same key as other
bib_writer = BibTexWriter()
current_position = 0
for _ , element in etree.iterparse(dblp_xml_name, tag=["article","inproceedings","proceedings","book","incollection","phdthesis","mastersthesis","www" ], load_dtd=True, huge_tree=True):
    current_position += len( etree.tostring(element))
    print_progress(current_position, filesize , "Extracting articles... ")

    # extract element key
    key = element.attrib["key"] # example journals/acta/Saxena96

    # check whether i am interested in this conference
    element_key =  key.split("/")[1]
    if not element_key in interested_in:
        element.clear()
        del element
        continue

    # create bib entry hash from xml element
    entry = {"ENTRYTYPE":element.tag, "ID":key}
    # if it has a rank, story rank
    #if interested_in[element_key]:
    #    entry["mendeley-tags"]= interested_in[element_key]

    for child in element:
         #print(child.tag, child.text)
         if child.tag=="author" and "author" in entry: # append author instead overwriting
            entry[child.tag] = entry[child.tag] + " and " + child.text
         elif child.tag=="url":
            entry[child.tag] = DBLP_ROOT_URL + child.text # add dblproot to url
         else:
             entry[child.tag] = "%s"%(child.text) # convert none strings

    # append entry to bibfile
    db = BibDatabase()
    db.entries = [entry]
    with open(filename_for(entry), 'a') as bibfile:
        bibfile.write(bib_writer.write(db))
    # free memory
    element.clear()
    del element

print("Done.")
print("Bye Bye... \n")
