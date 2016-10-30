
from Bio import Entrez

Entrez.email = "castelao@gmail.com"

handle = Entrez.egquery(term="Moorea")
record = Entrez.read(handle)

gi_list = record["IdList"]

for row in record["eGQueryResult"]:
    if row["DbName"]=="nuccore":
        print(row["Count"])




handle = Entrez.esearch(db="nucleotide", term="Paenibacillus sp. HGH0039 aczJo-supercont1.2.C40, whole genome shotgun sequence.")
handle = Entrez.esearch(db="nucleotide", term="HMPREF1207_04959")
record = Entrez.read(handle)
gi_list = record["IdList"]
gi_str = ",".join(gi_list)
handle = Entrez.efetch(db="nucleotide", id=gi_str, rettype="gb", retmode="text")
text = handle.read()
print text[:500]


import os
from Bio import SeqIO
from Bio import Entrez
Entrez.email = "A.N.Other@example.com"  # Always tell NCBI who you are
filename = "gi_186972394.gbk"
if not os.path.isfile(filename):
    # Downloading...
    net_handle = Entrez.efetch(db="nucleotide", id="186972394", rettype="gb", retmode="text")
    out_handle = open(filename, "w")
    out_handle.write(net_handle.read())
    out_handle.close()
    net_handle.close()
    print("Saved")
print("Parsing...")
record = SeqIO.read(filename, "genbank")
print(record)






from Bio import Entrez
Entrez.email = "castelao@gmail.com"

from Bio import Entrez

handle = Entrez.einfo()
record = Entrez.read(handle)
record.keys()
record["DbList"]

#handle = Entrez.einfo(db="nuccore")
handle = Entrez.einfo(db="nucleotide")
record = Entrez.read(handle)
record["DbInfo"].keys()
record["DbInfo"]["Description"]
record["DbInfo"]["Count"]
record["DbInfo"]["LastUpdate"]


# Searching
handle = Entrez.esearch(db="nucleotide", term="AGEN01000040")
#handle = Entrez.esearch(db="nucleotide", term="AGEN01000040 AND HMPREF1207_04959")
record = Entrez.read(handle)

handle = Entrez.efetch(db="nucleotide", id="512137967", rettype="gb", retmode="text")


term = "AGEN01000040"
seq_start = 684559
seq_stop = 760461

def efetch_hit(term, seq_start, seq_stop):
    """ Fetch the relevant part of a hit
    """
    Entrez.email = "castelao@gmail.com"

    handle = Entrez.esearch(db="nucleotide", term=term)
    record = Entrez.read(handle)

    assert len(record['IdList']) == 1, \
            "Sorry, I'm not ready to handle more than one record"

    handle = Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",
            id=record['IdList'][0],
            seq_start=seq_start, seq_stop=seq_stop)
    content = handle.read()

    return content



filename = '/Users/castelao/work/projects/others/gene_cluster_network/antiSMASH_input/PAL/clusterblast/cluster6.txt'

txt = open(filename).read()

import re

rule = r"""
    ^
    ClusterBlast\ scores\ for\ (?P<target>.*)\n+
    Table\ of\ genes,\ locations,\ strands\ and\ annotations\ of\ query\ cluster:\n+
    (?P<QueryCluster>
      (\w+ \s+ \d+ \s \d+ \s [+|-] \s \w+ (\s+\w+)?\s*\n+)+
      )
    \n \n+
    Significant \  hits:\ \n
    (?P<SignificantHits>
      (\d+ \. \ \w+ \t .* \n+)+
      )
    \n \n
    (?P<Details>
      Details:\n\n
      (
        >>\n
        \d+ \. .+ \n
        Source:\ .+ \n
        Type:\ .+ \n
        Number\ of\ proteins\ with\ BLAST\ hits\ to\ this\ cluster:\ \d+ \n
        Cumulative\ BLAST\ score:\ \d+
        \n \n
        Table\ of\ genes,\ locations,\ strands\ and\ annotations\ of\ subject\ cluster:\n
        (?P<TableGenes>
          (\w+ \"? \t \w+ \t \d+ \t \d+ \t [+|-] \t .* \n)+
          )
        \n
        Table\ of\ Blast\ hits\ \(query\ gene,\ subject\ gene,\ %identity,\ blast\ score,\ %coverage,\ e-value\): \n
        (?P<BlastHit>
          (\w+ \t \w+ \"? \t \d+ \t \d+ \t \d+\.\d+ \t \d+\.\d+e[+|-]\d+ \t \n)+
          )
        \n+
        )+
      )
      \n*
      $
"""

re.search(rule, txt, re.VERBOSE).groupdict()['Details']



