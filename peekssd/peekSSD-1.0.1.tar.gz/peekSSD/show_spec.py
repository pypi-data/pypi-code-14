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
                filename='show_spec.log',
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
def pre_condition_for_read_test( device ):
    cmd = "fio --name=full-range --filename=%s --numjobs=1 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0 --rw=randwrite \
--group_reporting --iodepth=128 --iodepth_batch=64 --iodepth_batch_complete=64" %device
    p = subprocess.Popen( cmd, shell=True )
    i = 1
    while p.poll() == None:
        time.sleep(60)
        logging.info("pre condition is running %d seconds" %(60*i))
        i = i + 1

def iops_4k_random_read_test( device ):

    cmd = "fio --name=riops_4k --filename=%s --numjobs=4 --bs=4k --ioengine=libaio --direct=1 --randrepeat=0 –norandommap \
--rw=randread --group_reporting --iodepth=512 --iodepth_batch=128 --iodepth_batch_complete=128 \
--gtod_reduce=1 --runtime=30> iops_4k_RR.txt" %device
    process = subprocess.Popen( cmd, shell=True )
    process.wait()

def iops_4k_random_write_test( device ):
    cmd = "fio --name=wiops_4k --filename=%s --numjobs=4 --bs=4k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap \
--rw=randwrite --group_reporting --iodepth=512 --iodepth_batch=128--iodepth_batch_complete=128 \
--gtod_reduce=1 --runtime=30 > iops_4k_RW.txt " %device

def iops_8k_random_read_test( device ):

    cmd = "fio --name=wiops_8k --filename=%s --numjobs=4 --bs=8k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap \
--rw=randwrite --group_reporting --iodepth=512 --iodepth_batch=128 --iodepth_batch_complete=128 \
--gtod_reduce=1 --runtime=30 > iops_8k_RR.txt" %device
    process = subprocess.Popen( cmd, shell=True )
    process.wait()

def iops_8k_random_write_test( device ):

    cmd = "fio --name=wiops_8k --filename=%s --numjobs=4 --bs=8k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap \
--rw=randwrite --group_reporting --iodepth=512 --iodepth_batch=128 --iodepth_batch_complete=128 \
--gtod_reduce=1 --runtime=30 > iops_8k_RW.txt" %device
    process = subprocess.Popen( cmd, shell=True )
    process.wait()


    
def bandwidth_128k_sequence_write_test( device ):
    
    cmd = "fio --name=wbw --filename=%s --numjobs=4 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0 --norandommap --rw=write --group_reporting --iodepth=512 --iodepth_batch=128 --iodepth_batch_complete=128 --gtod_reduce=1 --runtime=30 > bandwidth_128k_SW.txt" %device
    process = subprocess.Popen( cmd, shell=True )
    logging.info("Bandwidth 128KB Sequence Write Done")

def bandwidth_128k_sequence_read_test( device ):
    cmd = "fio --name=rbw --filename=%s --numjobs=4 --bs=128k --ioengine=libaio --direct=1 --randrepeat=0—norandommap \
--rw=read --group_reporting --iodepth=512 --iodepth_batch=128 --iodepth_batch_complete=128 \
--gtod_reduce=1 --runtime=30 > bandwidth_128k_SR.txt" %device
    process = subprocess.Popen( cmd, shell=True )
    process.wait()
    logging.info("Bandwidth 128KB Sequence Read Done")

def latency_4k_random_read_test( device ):
    cmd = "fio --name=rlat --filename=%s --numjobs=1 --runtime=30 --bs=4k --ioengine=libaio --direct=1 --randrepeat=0 \
--rw=randread --group_reporting --iodepth=1 --iodepth_batch_complete=0 > latency_4k_RR.txt" %device
    process = subprocess.Popen(cmd, shell=True )
    process.wait()
    

def latency_4k_random_write_test( device ):
    cmd = "fio --name=wlat --filename=%s --numjobs=1 --runtime=30 --bs=4k --ioengine=libaio --direct=1—norandommap \
--randrepeat=0 --rw=randwrite --group_reporting --iodepth=1 --iodepth_batch_complete=0 > latency_4k_RW.txt " %device
    process = subprocess.Popen( cmd, shell=True )
    process.wait()

def get_average_value( filename ):
    
    if filename == "iops_4k_RR.txt":
        value = 10
    if filename == "iops_4k_RW.txt":
        value = 10
    if filename == "iops_8k_RR.txt":
        value = 10
    if filename == "iops_8k_RW.txt":
        value = 10
    if filename == "bandwidth_128k_SR.txt":
        value = 10
    if filename == "bandwidth_128k_SW.txt":
        value = 10
    if filename == "latency_4k_RR.txt":
        value = 10
    if filename == "latency_4k_RW.txt":
        value = 10
    return value
def workout_values():
    print "-------------Performance Summary---------------"
    print "\t\t\t", "Average Value\t"
    for filename in ("iops_4k_RR.txt","iops_4k_RW.txt","iops_8k_RR.txt","iops_8k_RW.txt",
	"bandwidth_128k_SR.txt","bandwidth_128k_SW.txt","latency_4k_RR.txt","latency_4k_RW.txt"):
        if filename == "iops_4k_RR.txt":
            get_average_value( filename )
            print "4K Random Read IOPS:\t%dK" %(get_average_value(filename))
	if filename == "iops_4k_RW.txt":
            print "4K Random Write IOPS:\t%dK" %(get_average_value(filename))
	if filename == "iops_8k_RR.txt":
           print "8K Random Read IOPS:\t%dK" %(get_average_value(filename))
	if filename == "iops_8k_RW.txt":
           print "8K Random Write IOPS:\t%dK" %(get_average_value(filename))
	if filename == "bandwidth_128k_SR.txt":
	    print "128K Sequence Read:\t%.1f MB/s" %(get_average_value(filename))
	if filename == "bandwidth_128k_SW.txt":
            print "128K Sequence Write:\t%.1f MB/s" %(get_average_value(filename))
	if filename == "latency_4k_RR.txt":
	    print "4K Random Read Latency:\t%.2f us" %(get_average_value(filename))
	if filename == "latency_4k_RW.txt":
	    print "4K Random Write Latency:%.2f us" %(get_average_value(filename))
    print "-------------------End-------------------------"
def determine_path():
    root = __file__
    return os.path.dirname(os.path.abspath(root))
    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--version', action='version',version='1.0.0')
    parser.add_argument('-d','--device', help="The Shannon Device under test, /dev/dfa or /dev/sdb")

    args = parser.parse_args()
#    global abs_path
#    abs_path = determine_path()
    device = args.device
    
    #secure_erase_ssd( device )
    #logging.info("Start fill zero to full device")
    #fill_capacity_with_zero( device )
    logging.info("Start 128K Sequence Write Bandwidth Test")
    #bandwidth_128k_sequence_write_test( device )
    logging.info("Start 4K Random Write Latency Test")
    #latency_4k_random_write_test( device )
    logging.info("Start 4K Random Write IOPS Test") 
    #iops_4k_random_write_test( device )
    logging.info("Start 8K Random Write IOPS Test")
    #iops_8k_random_write_test( device )
    logging.info("Start Pre Condition For Read Test")
    #pre_condition_for_read_test( device )
    logging.info("Start 128K Sequence Read Bandwidth Test")
    #bandwidth_128k_sequence_read_test( device )
    logging.info("Start 4K Random Write Latency Test")
    #latency_4k_random_read_test( device )
    logging.info("Start 4K Random Read IOPS Test")  
    #iops_4k_random_read_test( device )
    logging.info("Start 8K Random Read IOPS Test") 
    iops_8k_random_read_test( device )
    workout_values()
    

    
if __name__ == "__main__":
    sys.exit(main())
