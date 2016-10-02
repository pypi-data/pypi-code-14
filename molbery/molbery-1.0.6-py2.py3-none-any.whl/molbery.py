#!/usr/bin/env python

__version__ = "1.0.6"

try:
    import sys
    from os.path import exists
    from os import makedirs
    from math import log10
    from time import sleep
    from argparse import ArgumentParser
    from string import maketrans                    
    from tabulate import tabulate  
    from Bio.Blast import NCBIWWW,NCBIXML
    from Bio import SeqIO
    from joblib import Parallel, delayed
    from shutil import rmtree
    from regex import findall,search
except:
    sys.stderr.write("Some of the modules could not be loaded! Dependencies not met.\n")
    raise SystemExit

def blast_probes(arg):
    gid=str(arg[1])
    seq=str(arg[2])
    sleep(int(gid)*3)
    result_handle=NCBIWWW.qblast("blastn","nt",seq)                                     #Blasting probes against "nr" Db
    blast_record=NCBIXML.read(result_handle)
    fh=open(arg[0]+"_blast_results/probe_"+str(int(gid)+1)+"_blast.out","w")    
    hits=len(blast_record.alignments)                                                  #PARSING BLAST OUTPUT                                         
    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
                fh.write("seq:"+str(alignment.title)+"\n"+"E value:"+str(hsp.expect)+"\n\n"+"query:"+str(hsp.query)+"\n"+"match:"+str(hsp.match)+"\n"+"sbjct:"+str(hsp.sbjct)+"\n\n"+"-+"*70+"\n\n")
    fh.close()
    

def find_probes(rec,args):
    if args.multi:
        seq_id=''.join(str(rec.id).split())
    else:
        seq_id=args.out
    nt_seq=str(rec.seq).upper()
    out=seq_id+".rst"
    output=open(out,'w')                                #Prompting and opening file in write mode
    output.write("Sequence ID - "+rec.id+"\n\n")

    tm_mer_22=list();final_29mer=list();screened_29mers=list();gc_tm_screened_29mer=list()
    for each in findall(r'(.{14}T.{7})',nt_seq,overlapped=True):                   #Regular expression to find all 22mers with T in 15th position
        nA=each.count("A",0,8);nT=each.count("T",0,8);nG=each.count("G",0,8);nC=each.count("C",0,8)         #Counting nucl. upto 8th pos       
        melt_temp_8 = (2 * (nA+nT)) + (4 * (nG+nC))                                                         #Calculating Tm of first 8 nucl.
        nA=each.count("A",8,15);nT=each.count("T",8,15);nG=each.count("G",8,15);nC=each.count("C",8,15)     #Counting nucl. from 8th to 15th pos    
        melt_temp_8_15 = (2 * (nA+nT)) + (4 * (nG+nC))                                                      #Calculating Tm of 8-15 nucl.
        if melt_temp_8 > melt_temp_8_15:
                tm_mer_22.append(each)                                                    #Screening for seq whose tm of loop > stem Nts
    
    intab="ATGC";outtab="TACG"
    trans=maketrans(intab,outtab) 
    final=dict()
    gc=[args.g,args.c]
    tm=[args.t,args.m]
    salt=args.s
    
    #Searching for complementation in loop region with stem
    for each in [fin for fin in [(mer[8:15][::-1].translate(trans))+mer for mer in tm_mer_22] if not search(fin[:4][::-1].translate(trans),fin[7:15])]:
        nA=each.count("A");nT=each.count("T");nG=each.count("G");nC=each.count("C")                        
        gc_cont=round(((nG + nC)/float(each.__len__()))*100,2)                                                                        
        melt_temp = round(100.5 + ((41 * (nG+nC))/(nA+nT+nG+nC)) -  (820/(nA+nT+nG+nC)) + (16.6*log10(salt)),2)
        if gc_cont >= int(gc[0]) and gc_cont <= int(gc[1]) and melt_temp >= int(tm[0]) and melt_temp <= int(tm[1]):
                    final[each]=(gc_cont,melt_temp)
    
    table=[];probes=[]
    cnt=1
    for key,value in final.items():                                                                             #setting up a pretty output table
                nA=key.count("A",15,22);nT=key.count("T",15,22);nG=key.count("G",15,22);nC=key.count("C",15,22)         
                melt_temp_0_7 = (2 * (nA+nT)) + (4 * (nG+nC))                                                   
                nA=key.count("A",7,15);nT=key.count("T",7,15);nG=key.count("G",7,15);nC=key.count("C",7,15)    
                melt_temp_7_15 = (2 * (nA+nT)) + (4 * (nG+nC))
                gc=value[0]
                tm=value[1]
                table.append([cnt,key,gc,tm,melt_temp_0_7,melt_temp_7_15])
                probes.append(key)
                cnt=cnt+1
                      
    headers = ["Probe","Molberys (29mer Probes)", "GC (%)", "Tm (C)", "Stem Tm (C)", "Loop Tm (C)"]
    output.write(tabulate(table, headers, tablefmt="grid"))                       
    output.close()
    sys.stdout.write("Results written to "+out+"\n")
    
    if args.blast:                                                                      #Blasting probes against NR Db 
        sys.stdout.write(str(len(final))+" probes queued for BLAST...\n")
    
        if not exists(seq_id+"_blast_results"):
                makedirs(seq_id+"_blast_results")
        else:
                rmtree(seq_id+"_blast_results")
                makedirs(seq_id+"_blast_results")

        to_blast=[(seq_id,j,probes[j])for j in range(len(probes))]
        try:
                Parallel(n_jobs=len(to_blast), verbose=25)(delayed(blast_probes)(i)for i in to_blast)           #Parallel processes for blasting probes
        except:
                sys.stderr.write("Blast request could not be completed. Check Network connection and try again!")

def main():
        #Argument parsing 
        parser = ArgumentParser(description='Design Molecular Beacons which works on ExoIII aided target recycling strategy. ( https://pypi.python.org/pypi/molbery/ )',prog='molbery')
        group = parser.add_mutually_exclusive_group()
        parser.add_argument("-v","--version", help="print version information and exit" , action='version', version='%(prog)s '+str(__version__))
        parser.add_argument("-b", "--blast", help="turn on blast search of probes against 'nr' db", action="store_true")
        parser.add_argument("input", help="full path of the fasta file containing DNA sequences", type=str)
        parser.add_argument("-g", help="minimum GC content of the probes", type=float, default=38.0)
        parser.add_argument("-c", help="maximum GC content of the probes", type=float, default=60.0)
        parser.add_argument("-t", help="lower limit of Tm of the probes in deg C", type=float, default=65.0)
        parser.add_argument("-m", help="upper limit of Tm of the probes in deg C", type=float, default=75.0)
        parser.add_argument("-s", help="salt concentration in Molar units", type=float, default=0.05)
        group.add_argument("--multi", help="use a multi-FASTA file", action="store_true")
        group.add_argument("-o","--out", help="output filename w/o extension when using single fasta seq", type=str, default="output")

        args = parser.parse_args()

        if args.g > args.c:
                sys.stderr.write("Minimum GC content cannot be greater than maximum.\nDefault:\nGC_min = 38\nGC_max=65\n")
                raise SystemExit
        if args.t > args.m:
                sys.stderr.write("Lower bound of Tm cannot be greater than upper bound.\nDefault:\nTm_min=65\nTm_max=75\n")
                raise SystemExit

        try:
                fhand=open(args.input,"rU")
                records = list(SeqIO.parse(fhand, "fasta"))
                fhand.close()
        except IOError as e:
                sys.stderr.write("Error opening file! I/O error("+str(e.errno)+"): "+str(e.strerror)+"\n")
                raise SystemExit

        if args.multi:
                for rec in records:
                        find_probes(rec,args)
        else:
                find_probes(records[0],args)
