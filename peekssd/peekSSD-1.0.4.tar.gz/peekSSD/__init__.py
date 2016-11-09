#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Copyright 2016 Shannon Sys
# All Rights Reserved.

import os
import sys
import time
import logging
import argparse
import subprocess

logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='show_stable.log',
                filemode='w')


def secure_erase_ssd(device):
    device = device
    cmd = "mkfs.ext4 -F -E discard " + device
    logging.info( cmd )
    p = subprocess.Popen( cmd, shell=True )
    returncode = p.wait()
    logging.info( returncode )

def fill_capacity_with_zero(device):
    for i in range(2):
        cmd = "dd if=/dev/zero bs=1024k of=" + device
    	logging.info( cmd )
    	p = subprocess.Popen( cmd, shell=True )
    	j = 1
    	while p.poll() == None:
            time.sleep(60)
            logging.info("dd is in process for %d seconds" %(60*j))
	    j = j + 1
def pre_condition( device ):

    cmd = "fio --name=wip --filename=%s --numjobs=1 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap --rw=write --group_reporting --iodepth=512 --iodepth_batch=128 --iodepth_batch_complete=128 --gtod_reduce=1 --loops=2" %device
    logging.info( cmd )
    p = subprocess.Popen( cmd, shell=True )
    i = 1
    while p.poll() == None:
        time.sleep(60)
        logging.info("pre condition is running %d seconds" %(60*i))
        i = i + 1


def iops_4k_random_read_test( device ):
    cmd = "sh iops_4k_RR.sh %s" %device
    process = subprocess.Popen( cmd, shell=True )
    i = 1
    while process.poll() == None:
        time.sleep(60)
        logging.info("testing IOPS 4KB randome read, running %d seconds" %(60*i))
        i = i + 1
    logging.info("IOPS 4KB Random Read Process Done")

def iops_8k_random_read_test( device ):
    cmd = "sh iops_8k_RR.sh %s" %device
    process = subprocess.Popen( cmd, shell=True )
    i = 1
    while process.poll() == None:
        time.sleep(60)
        logging.info("testing IOPS 8KB randome read, running %d seconds" %(60*i))
        i = i + 1
    logging.info("IOPS 8KB Random Read Process Done")

def iops_4k_random_write_test( device ):
    cmd = "sh iops_4k_RW.sh %s" %device
    process = subprocess.Popen( cmd, shell=True )
    i = 1
    while process.poll() == None:
        time.sleep(60)
        logging.info("testing IOPS 4KB Randome Write, running %d seconds" %(60*i))
        i = i + 1
    logging.info("IOPS 4KB Random Write Process Done")

def iops_8k_random_write_test( device ):
    cmd = "sh iops_8k_RW.sh %s" %device
    process = subprocess.Popen( cmd, shell=True )
    i = 1
    while process.poll() == None:
        time.sleep(60)
        logging.info("testing IOPS 8KB Randome Write running %d seconds" %(60*i))
        i = i + 1
    logging.info("IOPS 8KB Random Write Process Done")


def bandwidth_128k_sequence_read_test( device ):
    cmd = "sh bandwidth_128k_SR.sh %s" %device
    process = subprocess.Popen( cmd, shell=True )
    i = 1
    while process.poll() == None:
        time.sleep(60)
        logging.info("testing Bandwidth 4KB Sequence Read, running %d seconds" %(60*i))
        i = i + 1
    logging.info("Bandwidth 128KB Sequence Read Done")

def bandwidth_128k_sequence_write_test( device ):
    cmd = "sh bandwidth_128k_SW.sh %s" %device
    process = subprocess.Popen( cmd, shell=True )
    i = 1
    while process.poll() == None:
        time.sleep(60)
        logging.info("testing Bandwidth 4KB Sequence Write, running %d seconds" %(60*i))
        i = i + 1
    logging.info("Bandwidth 128KB Sequence Write Done")


def latency_test_pre_condition( device ):
    cmd = "fio --name=wip --filename=%s --numjobs=1 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap --rw=write --group_reporting --iodepth=1 --iodepth_batch=128 --iodepth_batch_complete=128  --gtod_reduce=1 --loops=2" %device
    logging.info( cmd )
    p = subprocess.Popen( cmd, shell=True )
    i = 1
    while p.poll() == None:
        time.sleep(60)
        logging.info("pre condition for latency is running %d seconds" %(60*i))
        i = i + 1

def latency_4k_random_read_test( device ):

     for i in range(151):
        cmd = "sh latency_4k_RR.sh %s %d" %(device, i)
        process = subprocess.Popen( cmd, shell=True )
        logging.info("testing IOPS 4KB randome read, running %d seconds" %(60*i))
        process.wait()

def latency_4k_random_write_test( device ):
    for i in range(211):         
        cmd = "sh latency_4k_RW.sh %s %d" %(device, i)    
	process = subprocess.Popen( cmd, shell=True )
        logging.info("testing IOPS 4KB randome write, running %d seconds" %(60*i))
        process.wait()

def process_gnuplot_charts( device ):
    #gnuplot_iops_4k_random_read
    dev = device.split("/")[2]
    
    cmd = "grep %s iostat_4k_RR.log | awk '{print $4}' | sed -n '900,4499p' | awk '{print(NR, $0)}' > iostat_4k_RR.txt" %dev
    logging.info( cmd )
    process = subprocess.Popen( cmd, shell=True ).wait()
    process = subprocess.Popen( "gnuplot gnuplot_4k_RR.conf", shell=True ).wait()
    #gnuplot_iops_4k_random_write
    cmd = "grep %s iostat_4k_RW.log | awk '{print $5}' | sed -n '2700,6299p' | awk '{print(NR, $0)}' > iostat_4k_RW.txt" %dev
    logging.info( cmd )
    subprocess.Popen( cmd, shell=True ).wait()
    subprocess.Popen( "gnuplot gnuplot_4k_RW.conf", shell=True ).wait()

    cmd = "grep %s iostat_8k_RR.log | awk '{print $4}' | sed -n '900,4499p' | awk '{print(NR, $0)}' > iostat_8k_RR.txt" %dev
    logging.info( cmd )
    process = subprocess.Popen( cmd, shell=True ).wait()
    process = subprocess.Popen( "gnuplot gnuplot_8k_RR.conf", shell=True ).wait()
    #gnuplot_iops_8k_random_write
    cmd = "grep %s iostat_8k_RW.log | awk '{print $5}' | sed -n '2700,6299p' | awk '{print(NR, $0)}' > iostat_8k_RW.txt" %dev
    logging.info( cmd )
    subprocess.Popen( cmd, shell=True ).wait()
    subprocess.Popen( "gnuplot gnuplot_8k_RW.conf", shell=True ).wait()

    cmd = "grep %s iostat_128k_SR.log | awk '{print $6}' | sed -n '900,4499p' | awk '{print(NR, $0)}' > iostat_128k_SR.txt" %dev
    logging.info( cmd )
    process = subprocess.Popen( cmd, shell=True ).wait()
    process = subprocess.Popen( "gnuplot gnuplot_128k_SR.conf", shell=True ).wait()
    #gnuplot bandwidth 128k sequence write
    cmd = "grep %s iostat_128k_SW.log | awk '{print $7}' | sed -n '2700,6299p' | awk '{print(NR, $0)}' > iostat_128k_SW.txt" %dev
    logging.info( cmd )
    subprocess.Popen( cmd, shell=True ).wait()
    subprocess.Popen( "gnuplot gnuplot_128k_SW.conf", shell=True ).wait()
    # latency
    with open("latency_4k_RR.txt","w") as latency_4k_rr_file:
        for i in range(30,151):
            filename = "latency_4k_RR_" + str(i) + ".log"
            with open(filename) as afile:
                lines = afile.readlines()
		line = str(i*30 - 900) + " " + str(lines[8].strip().split(',')[2].split('=')[1]) + "\n"
                latency_4k_rr_file.write( line )
    subprocess.Popen( "gnuplot gnuplot_4k_RR_latency.conf", shell=True ).wait()

    with open("latency_4k_RW.txt", "w") as latency_4k_rw_file:
        for i in range(90,211):
            filename = "latency_4k_RW_" + str(i) + ".log"
            with open(filename) as afile:
                lines = afile.readlines()
                line = str(i*30 - 2700) + " " + str(lines[8].strip().split(',')[2].split('=')[1]) + "\n"
                latency_4k_rw_file.write( line )
    subprocess.Popen( "gnuplot gnuplot_4k_RW_latency.conf", shell=True ).wait()
def workout_values():
    print "-------------Performance Summary---------------"
    print "\t\t\t", "Average Value\t","Max Value\t"
    for filename in ("iostat_4k_RR.txt","iostat_4k_RW.txt","iostat_8k_RR.txt","iostat_8k_RW.txt",
	"iostat_128k_SR.txt","iostat_128k_SW.txt","latency_4k_RR.txt","latency_4k_RW.txt"):
        values = []
        with open(filename) as afile:
            for line in afile:
                #print line
                values.append(float(line.split()[1]))
        if filename == "iostat_4k_RR.txt":
            print "4K Random Read IOPS:\t%dK\t\t%dK" %((sum(values)/len(values)/1000.0),max(values)/1000)
	if filename == "iostat_4k_RW.txt":
            print "4K Random Write IOPS:\t%dK\t\t%dK" %((sum(values)/len(values)/1000.0),max(values)/1000)
	if filename == "iostat_8k_RR.txt":
            print "8K Random Read IOPS:\t%dK\t\t%dK" %((sum(values)/len(values)/1000.0),max(values)/1000)
	if filename == "iostat_8k_RW.txt":
            print "8K Random Write IOPS:\t%dK\t\t%dK" %((sum(values)/len(values)/1000.0),max(values)/1000)
	if filename == "iostat_128k_SR.txt":
	    print "128K Sequence Read:\t%.1f MB/s\t%.1f MB/s" %((sum(values)/len(values)),max(values))
	if filename == "iostat_128k_SW.txt":
            print "128K Sequence Write:\t%.1f MB/s\t%.1f MB/s" %((sum(values)/len(values)),max(values))
	if filename == "latency_4k_RR.txt":
	    print "4K Random Read Latency:\t%.2f us\t%.2f us " %((sum(values)/len(values)), min(values))
	if filename == "latency_4k_RW.txt":
	    print "4K Random Write Latency:%.2f us\t%.2f us " %((sum(values)/len(values)), min(values))
    print "-------------------End-------------------------"
    
def parse_pargs():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--version', action='version',version='1.0')
    parser.add_argument('-d','--device', help="The Shannon Device under test, /dev/dfa or /dev/sdb")
    return parser.parse_args();
    
def main(args):
    
    logging.info("Start IOPS test")
    logging.info("Start Secure Erase SSD")
    
    device = args.device
    #secure_erase_ssd( device )
    logging.info("Start fill zero to full device")
    #fill_capacity_with_zero( device )
    logging.info("Start pre condition")
    #pre_condition( device )
    logging.info("Start IOPS 4KB Random Read Test")
    #iops_4k_random_read_test( device )
    logging.info("Start IOPS 8KB Random Read Test")
    #iops_8k_random_read_test( device )
    logging.info("Start IOPS 4KB Random Write Test")
    #iops_4k_random_write_test( device )
    logging.info("Start IOPS 8KB Random Write Test")
    #iops_8k_random_write_test( device )

    logging.info("Start Bandwidth Test")
    logging.info("Start Bandwidth Test Secure Erase SSD")
    #secure_erase_ssd( device )
    logging.info("Start Bandwidth Pre Condition")
    #pre_condition( device )
    #bandwidth_128k_sequence_read_test( device )
    #bandwidth_128k_sequence_write_test( device )

    logging.info("Start Latency Test")
    logging.info("Start Latency Test Secure Erase SSD")
    #secure_erase_ssd( device )
    logging.info("Start Latency Pre Condition")
    #latency_test_pre_condition( device )
    #latency_4k_random_read_test( device )
    #latency_4k_random_write_test( device )
    
    process_gnuplot_charts(device)
    workout_values()

    
if __name__ == "__main__":
    
    args = parse_pargs()
    sys.exit(main(args))
