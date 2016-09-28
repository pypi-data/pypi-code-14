#!/usr/bin/python

import threading,os,sys,traceback,thread,string,re,Queue,logging,time,scapy
from scapy.layers.inet import UDP,TCP,IP
from scapy.layers.l2 import *
from scapy.config import conf
from scapy.fields import *
from scapy.packet import *
from scapy.packet import Raw

import pdb,random,socket,struct

from scapy.data import KnowledgeBase
from scapy import *
from scapy.config import conf
from scapy.plist import PacketList
from time import sleep
from struct import *
import ConfigParser
from bgplib import *

# Ensure booleans exist (not needed for Python 2.2.1 or higher)
try:
    True
except NameError:
    False = 0
    True = not False

class ThreadPool:

    """Flexible thread pool class.  Creates a pool of threads, then
    accepts tasks that will be dispatched to the next available
    thread."""
    
    def __init__(self, numThreads,queue,print_counter,counter_val):

        """Initialize the thread pool with numThreads workers."""
        
        self.__threads = []
        self.__resizeLock = threading.Condition(threading.Lock())
        self.__taskLock = threading.Condition(threading.Lock())
        self.__tasks = []
        self.__isJoining = False
	self.__queue = queue
	self.__print_counter=print_counter
	self.__counter_val=counter_val
	print "Creating Thread Pool"
        self.setThreadCount(numThreads)

    def setThreadCount(self, newNumThreads):

        """ External method to set the current pool size.  Acquires
        the resizing lock, then calls the internal version to do real
        work."""
        
        # Can't change the thread count if we're shutting down the pool!
        if self.__isJoining:
            return False
        
        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(newNumThreads)
        finally:
            self.__resizeLock.release()
        return True

    def __setThreadCountNolock(self, newNumThreads):
        
        """Set the current pool size, spawning or terminating threads
        if necessary.  Internal use only; assumes the resizing lock is
        held."""
        i=0
        while newNumThreads > len(self.__threads):
            newThread = ThreadPoolThread(self,self.__queue,self.__print_counter,self.__counter_val)
            self.__threads.append(newThread)
            newThread.start()
	    print "Creating the ",len(self.__threads)," thread"
	    i = i + 1 

        while newNumThreads < len(self.__threads):
            self.__threads[0].goAway()
            del self.__threads[0]
	
    def getThreadCount(self):

        """Return the number of threads in the pool."""
        
        self.__resizeLock.acquire()
        try:
            return len(self.__threads)
        finally:
            self.__resizeLock.release()

    def queueTask(self, task, args=None, taskCallback=None):

        """Insert a task into the queue.  task must be callable;
        args and taskCallback can be None."""
        
        if self.__isJoining == True:
            return False
        if not callable(task):
            return False
        
        self.__taskLock.acquire()
        try:
            self.__tasks.append((task, args, taskCallback))
            return True
        finally:
            self.__taskLock.release()

    def getNextTask(self):

        """ Retrieve the next task from the task queue.  For use
        only by ThreadPoolThread objects contained in the pool."""
        
        self.__taskLock.acquire()
        try:
            if self.__tasks == []:
                return (None, None, None)
            else:
                return self.__tasks.pop(0)
        finally:
            self.__taskLock.release()
    
    def joinAll(self, waitForTasks = True, waitForThreads = True):

        """ Clear the task queue and terminate all pooled threads,
        optionally allowing the tasks and threads to finish."""
        
        # Mark the pool as joining to prevent any more task queueing
        self.__isJoining = True

        # Wait for tasks to finish
        if waitForTasks:
            while self.__tasks != []:
                sleep(.1)

        # Tell all the threads to quit
        self.__resizeLock.acquire()
        try:
            self.__setThreadCountNolock(0)
            self.__isJoining = True

            # Wait until all threads have exited
	    logging.critical("Killing all threads. Thanks for Using the Tool.")
            if waitForThreads:
                for t in self.__threads:
                    #t.join()
		    t.goAway()
                    del t
	    else:
		for t  in self.__threads:
		    #t.join()
		    t.goAway()
		    del t

            # Reset the pool for potential reuse
            self.__isJoining = False
        finally:
            self.__resizeLock.release()


        
class ThreadPoolThread(threading.Thread):

    """ Pooled thread class. """
    threadSleepTime = 0.1
    #+http_get_pkt =0
    #+http_post_pkt =0
    tcp_syn_ack = 0
    tcp_syn =0
    tcp_ack = 0
    #+http_cont =0
    #+http_cont_fin = 0
    def __init__(self, pool,queue,print_counter,counter_val):

        """ Initialize the thread and remember the pool. """
        
        threading.Thread.__init__(self)
        self.__pool = pool
	self.__queue = queue
	self.__counter_val=counter_val
	self.__print_counter=print_counter
        self.__isDying = False
        
    def run(self):

        """ Until told to quit, retrieve the next task and execute
        it, calling the callback if any.  """

        while self.__isDying == False:
            cmd, args, callback = self.__pool.getNextTask()
            # If there's nothing to do, just sleep a bit
            if cmd is None:
                sleep(ThreadPoolThread.threadSleepTime)
            elif callback is None:
                cmd(args,self.__queue,self.__print_counter,self.__counter_val)
            else:
                callback(cmd(args))

    
    def goAway(self):

        """ Exit the run loop next time through."""
        
        self.__isDying = True

#This takes 00112233 and returns 00:11:22:33:00:65 where 00:64 is vlan 100
def get_mac (l2_prefix,vlan_num):
    hexval = hex(int(vlan_num))
    hexval=hexval[2:]
    MAC_ID = "00:00:00:00:00:00"
    if (len(hexval) == 1):
        MAC_ID = l2_prefix[:2] + ':' + l2_prefix[2:4] + ':' + l2_prefix[4:6] + ':' + l2_prefix[6:8] + ':00:0' + hexval
        return MAC_ID
    if (len(hexval) == 2):
        MAC_ID = l2_prefix[:2] + ':' + l2_prefix[2:4] + ':' + l2_prefix[4:6] + ':' + l2_prefix[6:8] + ':00:' + hexval
        return MAC_ID
    if(len(hexval) == 3):
        MAC_ID = l2_prefix[:2] + ':' + l2_prefix[2:4] + ':' + l2_prefix[4:6] + ':' + l2_prefix[6:8] + ':0' + hexval[0] + ':' + hexval[1:]
        return MAC_ID
    return MAC_ID

#This takes 100.1. and returns 100.1.100.1 where vlan is 100
def get_ip (l3_prefix,host_num,curr_vlan):
    IP_PKT = "0.0.0.0"
    start_addr = int(host_num)
    if ((int(curr_vlan) < 254) and (int(host_num) < 254)):
        IP_PKT =  str(l3_prefix) + str(curr_vlan) + "." + str(start_addr) 
    if ((int(host_num) > 254) and (int(curr_vlan) < 254)):
        modval=int(host_num) % 256
        quoval=int(host_num)/256
        quoval=quoval+modval
        IP_PKT = str(l3_prefix) +  str(curr_vlan) + "." + str(quoval)
    if ((int(host_num) > 255) and (int(curr_vlan) > 255)):
        modval=int(host_num) % 256
        quoval=int(host_num)/256
        quoval=int(l3_prefix[2])+quoval
        modval1=int(curr_vlan) % 256
        quoval1=int(curr_vlan)/256
        quoval1=modval1+quoval1
        IP_PKT = str(l3_prefix[0:2]) +  str(quoval) + '.' + str(modval) + "." + str(quoval1)
    return IP_PKT


#This takes 1.1 and returns 1.1.0.100 where 1.1.0.100 is vlan 100
def get_ip_old (l3_prefix,vlan_num):
    print "get_ip_old"
    IP_PKT = "0.0.0.0"
    if (int(vlan_num) < 254):
        IP_PKT =  str(l3_prefix) + '0.' + str(vlan_num) 
    if (int(vlan_num) > 254):
	modval=int(vlan_num) % 256
	quoval=int(vlan_num)/256
        IP_PKT = str(l3_prefix) +  str(quoval) + '.' + str(modval)
    return IP_PKT



#The File Parser for the parsing all the fields.

def populate_variables_from_cfg(cfg_file):
    logging.warning("In function :  populate_variables_from_cfg ")
#  try:
    global connection_type
    global addr_base
    global start_host_ip
    global MAX_BURST
    global BURST_TIMER
    global l3_addr_prefix
    global l2_addr_prefix
    global log_level
    global log_file
    global hosts_per_port
    global port_count
    global interface
    global file_contents
    global packet_num
    global KILLALL
    global TARGET_IP
    global d_port
    global dst_mac
    global SOURCE_PORT
    global SYNACK_NO
    global SYN_NO
    global CONT_PSH_ACK
    global CONT_FIN
    global CONT_FIN_ACK
    global BGP_OPEN
    global BGP_KEEPALIVE
    global	BGP_UPDATE
    global	BGP_NOTIFY
    global	FIN
    global ACK_NO
    global INVALID
    global THREADS
    global ARP_TIMER
    global BGP_TIMER
    global RETRY_TIMER
    global RETRY_VAL
    global Syn_Host
    global Auth_Syn_Host
    global Syn_Ack_Rcv
    global Syn_Rcv
    global Ack_Rcv
    global Data_Ack_Rcv
    global Fin_Push_Ack_Rcv
    global Fin_Ack_Rcv
    global Push_Ack_Rcv
    global Fin_Ack_Host
    global Data_Ack_Host
    global Ack_Host
    global host_info

    #counter_create_issue=0
# Dont Change these Variables unless you are sure.
    SYNACK_NO=1
    ACK_NO=2
    FIN=3
    SYN_NO=4
    CONT_PSH_ACK=5
    CONT_FIN=6
    CONT_FIN_ACK=7
    BGP_OPEN=1
    BGP_KEEPALIVE=4
    BGP_UPDATE=2
    BGP_NOTIFY=3
    INVALID=999
    KILLALL = 1 
    packet_num=1
    host_info={}
    Syn_Host={}
    Syn_Ack_Rcv={}
    Syn_Rcv={}
    Ack_Host={}
    Data_Ack_Host={}
    Ack_Rcv={}
    Data_Ack_Rcv={}
    Fin_Push_Ack_Rcv={}
    Fin_Ack_Rcv={}
    Push_Ack_Rcv={}
    Fin_Ack_Host={}
    Config = ConfigParser.ConfigParser()
    Config.read(cfg_file)
    Config.sections()

    """ ConfigureParser here """

    connection_type=Config.get('main','connection_type')
    addr_base=Config.get('main','addr_base')
    start_host_ip=Config.get('main','start_host_ip')
    l3_addr_prefix = Config.get('main','l3_addr_prefix')
    l2_addr_prefix=Config.get('main','l2_addr_prefix')
    hosts_per_port=Config.get('main','hosts_per_port')
    port_count=Config.get('main','port_count')
    interface = Config.get('main','interface')
    SOURCE_PORT = Config.get('default','src_client_port')
    d_port = Config.get('default','dst_port')
    dst_mac = Config.get('default','target_mac')
    TARGET_IP = Config.get('default','target_ip')
    THREADS = Config.get('default','threads_per_capture')
    ARP_TIMER = Config.get('default','arp_timer')
    MAX_BURST = Config.get('default','burst')
    BURST_TIMER = Config.get('default','burst_timer')
    RETRY_VAL = Config.get('default','max_retry')
    RETRY_TIMER = Config.get('default','retry_timer')
    BGP_TIMER = Config.get('default','bgp_timer')
    log_file = Config.get('default','log_file')
    log_level = Config.get('default','log_level')

    populate_user_info(Config)
#  except:
#	logging.critical("Some Fields have been set to default as the config was not found in the file. The tool may not work as intended")


def get_total ():
	logging.warning("In function : get_total ")
	i=0
	vlan = int(addr_base)
	count = 0
	fail=0
	server_fail =0
	while (i<len(host_info)):
	  try:
		key_mac = get_mac (l2_addr_prefix,vlan)
		if(host_info[key_mac]==1):
			count=count + 1
		if(host_info[key_mac]==3):
			server_fail=server_fail+1
		if(host_info[key_mac]==2):
			fail=fail+1
		i = i + 1
		vlan=vlan + 1
	  except:
		logging.critical("Failed to get all host info")
		print"The total host  is " + str(count)
		print"The total Failure is " + str(fail)
		break
	print "The total host  is " + str(count)
	print "The total Failure is " + str(fail)
	print "The total Server Failure is " + str(server_fail)


def get_info (ip):
	logging.warning("In function : get_info ")
	try:
		key_ip = ip
		print "Sent Packets for ip " + str(key_ip)
		print "======================================================"
		print "Syn  : " + str(Syn_Host[key_ip])
		print "Acks  : " + str(Ack_Host[key_ip])
		print "Data Acks  : " + str(Data_Ack_Host[key_ip])
		print "Fin Acks  : " + str(Fin_Ack_Host[key_ip])
		print "Received Packets for ip " + str(key_ip)
		print "======================================================"
		print "Syn Ack : " + str(Syn_Ack_Rcv[key_ip])
		print "Syn  : " + str(Syn_Rcv[key_ip])
		print "Acks  : " + str(Ack_Rcv[key_ip])
		print "Data_Ack_Rcv  : " + str(Data_Ack_Rcv[key_ip])
		print "Fin Push Ack  : " + str(Fin_Push_Ack_Rcv[key_ip]) 
		print "Push Acks  : " + str(Push_Ack_Rcv[key_ip])
		print "Fin Acks  : " + str(Fin_Ack_Rcv[key_ip])
	except:
		logging.critical("Failed to get info of the host ip " + str(ip))

# This function populates the user information.
def populate_user_info(Config):
	logging.warning("In function : populate_user_info")
	i=0 
	max_host=int(hosts_per_port) * int(port_count)
	vlan = int(addr_base)
	port_curr_hostip = int(start_host_ip)
	k=0
	#try:
	if True:
		while (i < int(port_count)):
		  j=0
		  while (j<int(hosts_per_port)):
			num = k + 1
			key_mac = get_mac (l2_addr_prefix,port_curr_hostip)
			key_ip = get_ip (l3_addr_prefix,port_curr_hostip,vlan)

#**  Fill the defaults per host level here if config file doesnt have the values
			proto= Config.get(str(num),'proto')
			rid= Config.get(str(num),'routerid')
			routes= Config.get(str(num),'routes')
			target_ip= Config.get(str(num),'target_ip')
			sport= Config.get('default','src_client_port')


# Stats are all set to zero here  for all the hosts
			
    			Syn_Host[key_ip]=0
    			Syn_Ack_Rcv[key_ip]=0
    			Syn_Rcv[key_ip]=0
    			Ack_Host[key_ip]=0
    			Data_Ack_Host[key_ip]=0
    			Ack_Rcv[key_ip]=0
    			Data_Ack_Rcv[key_ip]=0
    			Fin_Push_Ack_Rcv[key_ip]=0
    			Fin_Ack_Rcv[key_ip]=0
    			Push_Ack_Rcv[key_ip]=0
    			Fin_Ack_Host[key_ip]=0
			host_info[key_ip]={}
			host_info[key_ip].update({'lastpkt':None})
			host_info[key_ip].update({'mac':key_mac})
			host_info[key_ip].update({'state':0})
			sport = random.randint(1000,50000)
			host_info[key_ip].update({'sport':sport})
			host_info[key_ip].update({'proto':proto})
			host_info[key_ip].update({'rid':rid})
			host_info[key_ip].update({'seq':0})
			host_info[key_ip].update({'ack':0})
			host_info[key_ip].update({'routes':routes})
			host_info[key_ip].update({'target_ip':target_ip})
			
			k= k + 1	
			j= j + 1
			port_curr_hostip = port_curr_hostip + 1
		  i= i + 1	
		  vlan = vlan + 1
		  print Syn_Ack_Rcv
	#except:
	#	logging.critical("Couldnt populate all Host info ")


# This function sends the TCP SYN Packets on all the ports.

def send_tcp_syn_pkts (dumb,extra_ports,burst_time):
	logging.warning("In function : send_tcp_syn_pkts")
	print ("In function : send_tcp_syn_pkts")
#    try:
        i =0
	burst_val =0
        curr_vlan = int(addr_base)
	
	port_curr_hostip = int(start_host_ip)
        while (i< int(port_count)):
	  j=0
	  while(j<int(hosts_per_port)):
            curr_mac = get_mac(l2_addr_prefix,port_curr_hostip)
	    curr_ip = get_ip(l3_addr_prefix,port_curr_hostip,curr_vlan)
	    #seq_num=RandInt().max
	    seq_num=random.randint(1000,45000)
	    if host_info.has_key(curr_ip):
		    SOURCE = host_info[curr_ip]['sport']
	    SOURCE = int(extra_ports)
	    if SOURCE > 65530:
		SOURCE =2
	    if False:
		print curr_mac
		print curr_ip
		print seq_num
		print SOURCE
		print dst_mac
		print d_port
		print TARGET_IP		
	    if True:
		if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
	            tcp_syn=Ether(dst=dst_mac,src=curr_mac)/IP(dst=TARGET_IP,src=curr_ip)/TCP(sport=int(SOURCE),dport=int(d_port),seq=seq_num,ack=0)
		else:
	            tcp_syn=Ether(dst=dst_mac,src=curr_mac)/Dot1Q(vlan=curr_vlan)/IP(dst=TARGET_IP,src=curr_ip)/TCP(sport=int(SOURCE),dport=int(d_port),seq=seq_num,ack=0)
		if (curr_mac != "ff:ff:ff:ff:ff:ff"):
			host_info[curr_ip]['seq']=seq_num+1
			host_info[curr_ip]['ack']=0
            		sendp(tcp_syn,iface=str(interface))
			host_info[curr_ip]['lastpkt']=tcp_syn
			burst_val = burst_val + 1
			Syn_Host[curr_ip] = Syn_Host[curr_ip] + 1
	    if (int(burst_val) > int(MAX_BURST)):
		burst_val = 0
		#sleep(float(BURST_TIMER))
		sleep(float(burst_time))
	    port_curr_hostip = int(port_curr_hostip) + 1
	    j = j + 1
          curr_vlan = curr_vlan + 1
          i = i+1
#    except:
#        logging.critical("Error in send_tcp_syn_pkt function")





#MAIN Starts from here

if __name__ == "__main__":
    if os.name == "posix":
	# Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
	# DOS/Windows
        os.system('CLS')
    else:
	# Fallback for other operating systems.
        print '\n' * numlines
    if ( len ( sys.argv ) < 2 ) :
        print " The config file is required"
        sys.exit ( )
    if ( len ( sys.argv ) > 3 ) :
        print " The maximum arguments is 2. Make sure there are no spaces. "
        sys.exit ( )

#Function to send the Ack packet based on sync values
    def send_syn_ack_packet(Packet):
	logging.warning("In function :  send_syn_ack_packet ")
        if host_info.has_key(Packet[IP].dst) == False:
		return
        Ether_part = Packet[Ether]
        IP_part = Packet[IP]
        TCP_part = Packet[TCP]
	if (Packet.haslayer(Raw) != 0):
		data_part = Packet[Raw]

        source_mac=Ether_part.src
        dest_mac=Ether_part.dst
        source_ip=IP_part.src
        dest_ip = IP_part.dst
        seq_no = TCP_part.seq
        ack_no = TCP_part.ack
        ack_no = host_info[Packet[IP].dst]['seq']
        src_port = TCP_part.sport
        dst_port = TCP_part.dport
	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
                tcp_syn_ack=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+1,flags=18)
        else:
                Dot1q_part = Packet[Dot1Q]
                curr_vlan = Dot1q_part.vlan
                tcp_syn_ack=Ether(dst=source_mac,src=dest_mac)/Dot1Q(vlan=curr_vlan)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+1,flags=18)

        if ((dest_mac != "ff:ff:ff:ff:ff:ff") ):
		host_info[dest_ip]['seq']=ack_no+1
                host_info[dest_ip]['ack']=seq_no+1
	
                sendp(tcp_syn_ack,iface=str(interface))
		host_info[dest_ip]['lastpkt']=tcp_syn_ack
                #Ack_Host[dest_ip] = Ack_Host[dest_ip] + 1

    def getBgpPktLen (Packet):
	logging.warning("In function :  getBgpPktLen ")
	bgpTotalLen = Packet[BGPHeader].len
	return bgpTotalLen

#Function to send the bgp keepalive packet 
    def send_modify_pkt(ip,flg,bgp_type):
        if host_info.has_key(ip) == False: 
		return
	source_mac = host_info[ip]['mac']
	dest_mac = dst_mac
	source_ip = host_info[ip]
	dest_ip = TARGET_IP
	dst_port = d_port
	src_port = host_info[ip]['sport']
	seq_no = host_info[ip]['seq']
	ack_no = host_info[ip]['ack']
	flags = flg
	
	Packet=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=seq_no,ack=ack_no,flags=flg)
	if bgp_type == BGP_OPEN:
		send_bgp_open(Packet)	
	if bgp_type == BGP_KEEPALIVE:
		send_bgp_keepalive(Packet)	

#Function to send the bgp keepalive packet 
    def send_bgp_keepalive(Packet):
	logging.warning("In function :  send_bgp_keepalive ")
        if host_info.has_key(Packet[IP].dst) == False:
		return
        Ether_part = Packet[Ether]
        IP_part = Packet[IP]
        TCP_part = Packet[TCP]
	data_part = None
	val=1
	if (Packet.haslayer(BGPHeader) != 0):
		val = getBgpPktLen(Packet)

        source_mac=Ether_part.src
        dest_mac=Ether_part.dst
        source_ip=IP_part.src
        dest_ip = IP_part.dst
        seq_no = TCP_part.seq
        ack_no = TCP_part.ack
        ack_no = host_info[Packet[IP].dst]['seq']

        src_port = TCP_part.sport
        dst_port = TCP_part.dport

	bgpHd = BGPHeader(type=4)
	bgpKeep = BGPHeader(type=4,len=19)
	#bgpKeep = bgpHd

	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=24)/bgpKeep
        else:
                Dot1q_part = Packet[Dot1Q]
                curr_vlan = Dot1q_part.vlan
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/Dot1Q(vlan=curr_vlan)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=24)/bgpKeep
	#tcp_ack1.seq=ack_no+18
	#tcp_ack1.ack=seq_no+val+1
        if ((dest_mac != "ff:ff:ff:ff:ff:ff") ):
		dumbi = 0
		#while dumbi <2:
                host_info[dest_ip]['seq']=ack_no+(len(bgpKeep))
                host_info[dest_ip]['ack']=seq_no+val

		sendp(tcp_ack,iface=str(interface))
		host_info[dest_ip]['lastpkt']=tcp_ack
		#sendp(tcp_ack1,iface=str(interface))
		host_info[Packet[IP].dst]['state']=BGP_KEEPALIVE
		#	dumbi = dumbi + 1
                #Ack_Host[dest_ip] = Ack_Host[dest_ip] + 1


#Function to send the bgp_update packet based on 
    def send_bgp_update(Packet):
	logging.warning("In function :  send_bgp_update")
        if host_info.has_key(Packet[IP].dst) == False:
		return
        Ether_part = Packet[Ether]
        IP_part = Packet[IP]
        TCP_part = Packet[TCP]
	data_part = None
	val=1
	if (Packet.haslayer(BGPHeader) != 0):
		val = getBgpPktLen(Packet)

        source_mac=Ether_part.src
        dest_mac=Ether_part.dst
        source_ip=IP_part.src
        dest_ip = IP_part.dst
        seq_no = TCP_part.seq
        ack_no = TCP_part.ack
        ack_no = host_info[Packet[IP].dst]['seq']

        src_port = TCP_part.sport
        dst_port = TCP_part.dport

	bgpHd = BGPHeader(type=2)
	bgpAsPath =  BGPPathAttribute(flags=0x40,type=2,value="\x02\x02\x00\x00\x00\x80\x00\x00\x01\x05")
	#bgpAsPath =  BGPPathAttribute(flags=0x40,type=2)
	#bgpMed = BGPPathAttribute(type=4,value="\x02\x02\x45\x56")

	bgpNHop =  BGPPathAttribute(type=3,value="\x65\x01\x01\x05")
	bgpOrg =  BGPPathAttribute(type=1,value="\x01")
	bgpLPref =  BGPPathAttribute(type=5,value="\x00\x00\x00\x00")
	bgpLPref1 =  BGPPathAttribute(type=5,value="\x00\x10\x00\x00")
	bgpPathAttr1 = bgpNHop/bgpOrg/bgpLPref
	#bgpPathAttr1 = bgpAsPath/bgpNHop/bgpOrg/bgpLPref/bgpMed
	bgpPathAttr1 = bgpAsPath/bgpNHop/bgpOrg/bgpLPref
	#bgpPathAttr1 = bgpAsPath/bgpNHop/bgpOrg
	i=20
	while i < 10:
	   i +=1
	   if i == 5 or i== 3 or  i == 6 or i ==7:
		continue
	   else:
		bgpAttr = BGPPathAttribute(type=i,value="\x65\x01\x01\x05")
		bgpPathAttr1 = bgpPathAttr1/bgpAttr
	bgpPathAttr2 = bgpNHop/bgpOrg/bgpLPref1
	bgpNLRI = []	
	bgpNLRI1 = []	
	bgpNLRI.append(BGPIPField("","22.1.0/8"))
	bgpNLRI1.append(BGPIPField("","22.1.1.0/8"))
	i = 1
	while i<30:
		i = i + 1
		ip_val=socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
		mask=random.randint(0,32)
		ip_mask=str(ip_val)+"/"+str(mask)
		bgpIP = BGPIPField('',str(ip_mask))
		#bgpIP = BGPIPField('',"5.5.5.6/24")
		if i == 2:
			bgpNLRI.append(bgpIP)
			continue
		bgpNLRI.append(bgpIP)
		bgpNLRI1.append(bgpIP)
	bgpUpd = BGPUpdate(total_path=bgpPathAttr1,nlri=bgpNLRI)
	bgpUpd2 = BGPUpdate(total_path=bgpPathAttr2,nlri=bgpNLRI1)
	bgpUpdate = bgpHd/bgpUpd
	bgpUpdate1 = bgpHd/bgpUpd2

	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=24)/bgpUpdate
                #tcp_ack1=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no+85,ack=seq_no+val,flags=24)/bgpUpdate1
        else:
                Dot1q_part = Packet[Dot1Q]
                curr_vlan = Dot1q_part.vlan
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/Dot1Q(vlan=curr_vlan)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=24)/bgpUpdate

        if ((dest_mac != "ff:ff:ff:ff:ff:ff") ):
		host_info[dest_ip]['seq']=ack_no+(len(bgpUpdate))
		host_info[dest_ip]['ack']=seq_no+val
		dumbi = 0
		#while dumbi <2:
		#tcp_ack.display()
		sendp(tcp_ack,iface=str(interface))
		host_info[dest_ip]['lastpkt']=tcp_ack
		#sendp(tcp_ack1,iface=str(interface))
		host_info[Packet[IP].dst]['state']=BGP_UPDATE
		#	dumbi = dumbi + 1
                #Ack_Host[dest_ip] = Ack_Host[dest_ip] + 1

#Function to send the bgp_open packet based on sync values
    def send_bgp_open(Packet):
	logging.warning("In function :  send_bgp_open ")
        if host_info.has_key(Packet[IP].dst) == False:
		return
        Ether_part = Packet[Ether]
        IP_part = Packet[IP]
        TCP_part = Packet[TCP]
	data_part = None
	val=1
	if (Packet.haslayer(BGPHeader) != 0):
		val = getBgpPktLen(Packet)

        source_mac=Ether_part.src
        dest_mac=Ether_part.dst
        source_ip=IP_part.src
        dest_ip = IP_part.dst
        seq_no = TCP_part.seq
        ack_no = TCP_part.ack
        ack_no = host_info[Packet[IP].dst]['seq']

        src_port = TCP_part.sport
        dst_port = TCP_part.dport

	bgpHd = BGPHeader(type=1)
	bgpCap2 = BGPOptionalParameter(type=2,value='\x00\x01\x05\x01')
	bgpCap2 = BGPOptionalParameter(type=2)
	bgpCap2 = BGPOptionalParameter(type=1,value='\x00\x01\x05\x02')
	bgpCap = bgpCap2
	i = 10
	while i<20:
		i = i + 1
		if i == 64:
			continue
		bgpCap1 = BGPOptionalParameter(type=i,value='\x00\x01\x05\x02')
		bgpCap = bgpCap/bgpCap1
	bgpCap2 = BGPOptionalParameter(type=12)
	bgpCap2 = BGPOptionalParameter(type=65,len=4,value='\x00\x00\xfd\xe8')
	bgpCap = bgpCap/bgpCap2
	bgpCap2 = BGPOptionalParameter(type=1,value='\x00\x01\x05\x01')
	bgpCap = bgpCap/bgpCap2
	bgpCaplist = BGPOptionalParameter(type=2,value=bgpCap)
	bgpOpen = bgpHd/BGPOpen (AS=65000,bgp_id="5.5.5.5",hold_time=6,opt_parm=bgpCaplist)
	#bgpOpen = bgpHd/BGPOpen (version=4,AS=65000,bgp_id="5.5.5.5",hold_time=30)
	bgpOpen1 = bgpHd/BGPOpen (version=6,AS=65000,bgp_id="5.5.5.5",hold_time=3)

	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=24)/bgpOpen
        else:
                Dot1q_part = Packet[Dot1Q]
                curr_vlan = Dot1q_part.vlan
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/Dot1Q(vlan=curr_vlan)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=24)/bgpOpen

        if ((dest_mac != "ff:ff:ff:ff:ff:ff") ):
		host_info[dest_ip]['seq']=ack_no+len(bgpOpen)
		#host_info[dest_ip]['seq']=ack_no+int(str(len(bgpOpen)),16)+1
		host_info[dest_ip]['ack']=seq_no+val
		dumbi = 0
		#while dumbi <2:
		sendp(tcp_ack,iface=str(interface))
		host_info[dest_ip]['lastpkt']=tcp_ack
		host_info[Packet[IP].dst]['state']=BGP_OPEN
		#	dumbi = dumbi + 1
                #Ack_Host[dest_ip] = Ack_Host[dest_ip] + 1


#Function to send the Ack packet based on sync values
    def send_ack_packet(Packet):
	logging.warning("In function :  send_ack_packet ")
        if host_info.has_key(Packet[IP].dst) == False:
		return
        Ether_part = Packet[Ether]
        IP_part = Packet[IP]
        TCP_part = Packet[TCP]
	data_part = None
	val=1
	if (Packet.haslayer(BGPHeader) != 0):
		val = getBgpPktLen(Packet)

        source_mac=Ether_part.src
        dest_mac=Ether_part.dst
        source_ip=IP_part.src
        dest_ip = IP_part.dst
        seq_no = TCP_part.seq
        ack_no = TCP_part.ack
        ack_no = host_info[Packet[IP].dst]['seq']

        src_port = TCP_part.sport
        dst_port = TCP_part.dport
	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=16)
        else:
                Dot1q_part = Packet[Dot1Q]
                curr_vlan = Dot1q_part.vlan
                tcp_ack=Ether(dst=source_mac,src=dest_mac)/Dot1Q(vlan=curr_vlan)/IP(dst=source_ip,src=dest_ip)/TCP(sport=dst_port,dport=src_port,seq=ack_no,ack=seq_no+val,flags=16)

        if ((dest_mac != "ff:ff:ff:ff:ff:ff") ):
		host_info[dest_ip]['seq']=ack_no
		host_info[dest_ip]['ack']=seq_no+val
                sendp(tcp_ack,iface=str(interface))
		host_info[dest_ip]['lastpkt']=tcp_ack
                #Ack_Host[dest_ip] = Ack_Host[dest_ip] + 1



#This function process the incoming TCP packets from the queue.   
    def processTcpPacket(dumb,queue,print_counter,counter_val):
	logging.warning("In function : processTcpPacket")
	counter_create_issue= 0
	lst=[]
	i=0
	while 1:
		counter_create_issue = counter_create_issue + 1
		#try:
		if True:
		    if (queue.qsize != 0 ):
			lst.append(queue.get())
			Packet=PacketList(lst,"Sniffed")
			pkt_type=get_packet_type(Packet[i])
			#print " My packet type is "
			#print pkt_type 	
			if (pkt_type==SYNACK_NO):
				send_ack_packet(Packet[i])
				send_bgp_open( Packet[i] )
			elif (pkt_type==SYN_NO):
				#dumbi=0
				send_syn_ack_packet(Packet[i])
			elif (pkt_type==ACK_NO):
				dumbi = 0
			elif (pkt_type==FIN):
				send_tcp_fin_set(Packet[i])
			elif (pkt_type==CONT_FIN):
				send_tcp_fin_set(Packet[i])
			elif (pkt_type==CONT_FIN_ACK):
				dumbi = 0
				send_tcp_fin_set(Packet[i])
			elif (pkt_type==CONT_PSH_ACK):
				send_ack_packet(Packet[i])
			else :
				logging.warning("Received Packet with Flag set : " + str(pkt_type))

			bgp_pkt_type=get_bgp_packet_type(Packet[i])

			if (bgp_pkt_type==BGP_OPEN):
				logging.warning("Got a Bgp open")
				if host_info.has_key(Packet[i][IP].dst) == True:
					if host_info[Packet[i][IP].dst]['state'] == 0:  # REMOVE COMMENT HERE
						send_bgp_open(Packet[i])
			elif (bgp_pkt_type==BGP_KEEPALIVE):
				dumbi = 0
				send_bgp_keepalive(Packet[i])
				if True:
					Packet[i].seq=Packet[i].seq
					Packet[i].ack=int(Packet[i].ack)+19
					send_bgp_update(Packet[i])
					if counter_create_issue / 100 > 0:
						counter_create_issue= 0
						send_bgp_open(Packet[i])
			elif (bgp_pkt_type==BGP_UPDATE):
				dumbi=0
				print "recv bgp update"
				send_bgp_update(Packet[i])
				#recv_bgp_update(Packet[i])
			elif (bgp_pkt_type==BGP_NOTIFY):
				dumbi=0
				print "recv notify"
				send_tcp_syn_pkts(1,int(Packet[i].dport)+2,BURST_TIMER)
				#recv_bgp_notify(Packet[i])
			elif (bgp_pkt_type==None):
				dumbi = 0
			else :
				logging.warning("Received Packet with Flag set : " + str(bgp_pkt_type))
			lst.pop()
		#except:
		#	lst.pop()
		#	logging.critical("Error in the Process tcp packet")



# This function listens to TCP packets and puts into the QUEUE
    def listen_to_tcp_packets(dumb,queue,print_counter,counter_val):
	#logging.warning("In function : listen_to_tcp_packets")
	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
		str_filter=" ip and tcp port " + str(d_port)
		#str_filter=" ip src " + str(TARGET_IP) + " and tcp port " + str(d_port)
	else:
		str_filter=" vlan and ip and tcp port " + str(d_port)
		#str_filter=" vlan and ip src " + str(TARGET_IP) + " and tcp port " + str(d_port)
	interf = str(interface)
	so=conf.L2listen(type=3,filter=str_filter,iface=interf)
	#so=config.conf.L2socket(type=3,filter=str_filter,iface=interf)
	#so=conf.L2listen(type=3,filter=str_filter,iface=interf)
	c=0
        while True:
                try:
			p = so.recv(1600)
			if p is None:
				logging.warning("packet was unknown")
			#p.display()	
			queue.put(p)
			c = c + 1
			#logging.warning("The total count is " + str(c))
		except:
			logging.critical("The listen_to_tcp_packets failed")

    def wait_send_arp_pkts (timer,queue,print_counter,counter_val):
	logging.warning("In function : wait_send_arp_pkts")
	while 1:
		if (int(timer)==0):
			logging.warning("ARP timer is stopped")
			break
		else:
			sleep(float(timer))
			logging.warning("ARP THREAD Woke up , now sending ARPS")
			send_arp_pkts(1)

    def wait_send_tcp_syn_pkts ((timer,burst_time),queue,print_counter,counter_val):
	logging.warning("In function : wait_send_tcp_syn_pkts")
	extra_ports = 2
	extra_ports = random.randint(1000,40000)
	tries = 0
	while 1:
		if (int(timer)==0):
			logging.warning("TCP timer is stopped")
			break
		else:
		  if(int(tries) < int(RETRY_VAL)):
			sleep(float(timer))
			send_tcp_syn_pkts(1,extra_ports,burst_time)
			extra_ports = int(extra_ports) 
			tries = int(tries) + 1


    # Send ARP Packets
    def send_arp_pkts (dumb):
	logging.warning("In function : send_arp_pkts")
    	#try:
	if True:
       	 i =0
       	 curr_vlan = int(addr_base)
	 port_curr_hostip = int(start_host_ip)
       	 while (i< int(port_count)):
	  j=0
	  while(j<int(hosts_per_port)):
            curr_mac = get_mac(l2_addr_prefix,port_curr_hostip)
	    curr_ip = get_ip(l3_addr_prefix,port_curr_hostip,curr_vlan)
	    if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
            	arp_packet=Ether(dst="FF:FF:FF:FF:FF:FF",src=curr_mac)/ARP(hwsrc=str(curr_mac),psrc=str(curr_ip),pdst=str(TARGET_IP),op=0x001)
	    else:
            	arp_packet=Ether(dst="FF:FF:FF:FF:FF:FF",src=curr_mac)/Dot1Q(vlan=curr_vlan,type=0x806)/ARP(hwsrc=str(curr_mac),psrc=str(curr_ip),pdst=str(TARGET_IP),op=0x001)
#	    arp_packet=Ether(dst="FF:FF:FF:FF:FF:FF",src=curr_mac)/ARP(hwsrc=str(curr_mac),psrc=str(curr_ip),pdst=str(TARGET_IP),op=0x001)
	    if (curr_mac != "ff:ff:ff:ff:ff:ff"):
		    sendp(arp_packet,iface=str(interface))
	    j= j +1
	    port_curr_hostip = int(port_curr_hostip) + 1
          curr_vlan = curr_vlan + 1
          i = i+1
        #except:
        #     logging.critical("Error in send_arp_pkt function")

    def receiveCallback(packet_info):
        logging.warning("Callback called for completing Processing "+ str(packet_info))

    def listenCallback(packet_info):
	logging.warning("Exiting from listening to the TCP packets "+ str(packet_info))



    # - get the packet type
    def get_bgp_packet_type(Packet):
	logging.warning("In function : get_bgp_packet_type") 
	#try:
	if True:
		field=Packet[TCP]
		mac=Packet[Ether]
		iphost = Packet[IP]	
		key_ip = iphost.dst
		if host_info.has_key(Packet[IP].dst) == False:
			return None
		if (mac.dst == "ff:ff:ff:ff:ff:ff"):
			logging.warning("MAC receive was "+str (mac.dst))
			return INVALID
		if (Packet.haslayer(BGPHeader) != 0):
			bgpType = Packet[BGPHeader].type
			return bgpType
		#if (Packet.haslayer(Raw) != 0):
		#	string_bgp = packet[Raw]

		return None
#	except:
#		logging.critical("Error in get packet processing")


    # - get the packet type
    def get_packet_type(packet):
	logging.warning("In function : get_packet_type")
	#try:
	if True:
		field=packet[TCP]
		mac=packet[Ether]
		iphost = packet[IP]	
		key_ip = iphost.dst
		logging.warning("Flag receive was "+str (field.flags))
		if (mac.dst == "ff:ff:ff:ff:ff:ff"):
			logging.warning("MAC receive was "+str (mac.dst))
			return INVALID
		if (packet.haslayer(Raw) != 0):
			string_bgp = packet[Raw]
		if (field.flags == 0x0004):
			return None
		if (field.flags == 0x0012):
			if Syn_Ack_Rcv.has_key(key_ip):
				Syn_Ack_Rcv[key_ip] = Syn_Ack_Rcv[key_ip] + 1
			if host_info.has_key(key_ip):
				#print "target ip check in synack"
				dumbi=0
			return SYNACK_NO
		if (field.flags == 0x0010):
			if (packet.haslayer(Raw) != 0):
				if (packet[Raw] != None):
					Data_Ack_Rcv[key_ip] = Data_Ack_Rcv[key_ip] + 1
					return None   ## Need to check this  
			if Ack_Rcv.has_key(key_ip):
				Ack_Rcv[key_ip] = Ack_Rcv[key_ip] + 1
			if host_info.has_key(key_ip):
				dumbi=0
				#print "target ip check in ackrcv"
			return ACK_NO
		if (field.flags == 0x0018):
			if Push_Ack_Rcv.has_key(key_ip):
				Push_Ack_Rcv[key_ip] = Push_Ack_Rcv[key_ip] + 1
			if host_info.has_key(key_ip):
				#print "target ip check in push_ackrcv"
				dumbi=0
			return CONT_PSH_ACK
		if (field.flags == 0x0019):
			#Fin_Push_Ack_Rcv[key_ip] = Fin_Push_Ack_Rcv[key_ip] + 1
			return CONT_FIN
		if (field.flags == 0x0011):
			#Fin_Ack_Rcv[key_ip] = Fin_Ack_Rcv[key_ip] + 1
			return CONT_FIN_ACK
		if (field.flags == 0x0002):
			#if Syn_Rcv.has_key(key_ip):
			#	Syn_Rcv[key_ip] = Syn_Rcv[key_ip] + 1
			if host_info.has_key(key_ip):
				#print "target ip check in syn rcv"
				dumbi=0
			return SYN_NO
		return field.flags
#	except:
#		logging.critical("Error in get packet processing")
    

    # - tcp ack - packet sent out.
    def send_tcp_cont_ack(Packet):
	logging.warning("In function : send_tcp_cont_ack")
        if host_info.has_key(Packet[IP].dst) == False:
		return
	try:
		srcmac = Packet[Ether].dst
		dstmac = Packet[Ether].src
		srcip = Packet[IP].dst
		destip = Packet[IP].src
		length=int(Packet[IP].len) - 40
		seq = Packet[IP].ack
		ack = Packet[IP].seq + length
		seq = host_info[Packet[IP].dst]['seq']

		sport = Packet[IP].dport
		dport = Packet[IP].sport
		
	    	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
			http_cont_ack=Ether(dst=dstmac,src=srcmac)/IP(dst=destip,src=srcip)/TCP(sport=sport,dport=dport,seq=seq,ack=ack,flags=16)
		else:
			Dot1q_part = Packet[Dot1Q]
			curr_vlan = Dot1q_part.vlan
			http_cont_ack=Ether(dst=dstmac,src=srcmac)/Dot1Q(vlan=curr_vlan)/IP(dst=destip,src=srcip)/TCP(sport=sport,dport=dport,seq=seq,ack=ack,flags=16)
		if (srcmac != "ff:ff:ff:ff:ff:ff"):
			host_info[srcip]['seq']=seq
			host_info[srcip]['ack']=ack+1

			sendp(http_cont_ack,iface=str(interface))	
			host_info[srcip]['lastpkt']=http_cont_ack
			Data_Ack_Host[srcip] = Data_Ack_Host[srcip] + 1
		logging.warning("TCP ACK sent for"+ str(srcip)+str(srcmac))
	except:
		logging.critical("Error in tcp_cont_ack")


    #   # Send TCP FIN SET Packet
		# Send TCP SYN Finish Packet
    def send_tcp_fin_set(Packet):
		logging.warning("In function : send_tcp_fin_set")
		if host_info.has_key(Packet[IP].dst) == False:
			return
		srcmac = Packet[Ether].dst
		dstmac = Packet[Ether].src
		srcip = Packet[IP].dst
		destip = Packet[IP].src
		length=int(Packet[IP].len) - 40
		seq = Packet[IP].ack
		ack = Packet[IP].seq + length
                seq = host_info[Packet[IP].dst]['seq']

		sport = Packet[IP].dport
		dport = Packet[IP].sport
	    	if ((str(connection_type) == "plainbgp") or (str(connection_type) == "plainbgp")):
			tcp_fin_set=Ether(dst=dstmac,src=srcmac)/IP(dst=destip,src=srcip)/TCP(sport=sport,dport=dport,seq=seq,ack=ack+1,flags=17)
		else:
			Dot1q_part = Packet[Dot1Q]
			curr_vlan = Dot1q_part.vlan
			tcp_fin_set=Ether(dst=dstmac,src=srcmac)/Dot1Q(vlan=curr_vlan)/IP(dst=destip,src=srcip)/TCP(sport=sport,dport=dport,seq=seq,ack=ack+1,flags=17)
		if (srcmac != "ff:ff:ff:ff:ff:ff"):
			host_info[srcip]['seq']=seq
			host_info[srcip]['ack']=ack+1

			sendp(tcp_fin_set,iface=str(interface))
			host_info[srcip]['lastpkt']=tcp_fin_set
			#Fin_Ack_Host[srcip] = Fin_Ack_Host[srcip] + 1
		logging.warning("TCP Fin ACK sent for "+str(srcip)+str(srcmac))

    try:
        print "The processing file is ", sys.argv[1]
        populate_variables_from_cfg (sys.argv[1])
	if (int(log_level) != 0):
		logger = logging.root
		lgfile=time.asctime()
		if (int(log_file) == 1):
			hdlr = logging.FileHandler('/var/tmp/'+str(lgfile))
			print "The logging file is " + str(lgfile)
		else:
			hdlr = logging.StreamHandler(sys.stdout)
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		#formatter = logging.Formatter('%(levelname)s %(message)s')
		hdlr.setFormatter(formatter)
		logger.addHandler(hdlr)
		if (int(log_level) == 15):
			print "Logging Set to Debug Level"
			logger.setLevel(logging.WARNING)
		else:
			print "Logging Set to Critical Level"
			logger.setLevel(logging.CRITICAL)
	else:
		logging.disable(60)
		print "Logging is Disabled"
	queue = Queue.Queue(0)
	print_counter = Queue.Queue(0)
	counter_val = {}
	counter_val['TCP_SYN_ACK']=0
	counter_val['TCP_FIN_PUSH_ACK']=0
	pool = ThreadPool(4,queue,print_counter,counter_val)
	logging.warning("The constants"+str(ARP_TIMER)+str(BGP_TIMER))
	pool.queueTask(listen_to_tcp_packets,(1), )
#	pool.queueTask(wait_send_arp_pkts,(ARP_TIMER), )
	pool.queueTask(wait_send_tcp_syn_pkts,(BGP_TIMER,BURST_TIMER ),)
	global counter_create_issue
	counter_create_issue = 0
	pool.queueTask(processTcpPacket,(1), )
#	pool.queueTask(processTcpPacket,(1), )
	main_t1 = os.getpid()
	try:
	 x = 2	
         i=raw_input("")
         while ( str(i) != "exit" ):
	    if( str(i) == 2):
			print_coun_er.put(1)
	    elif (str(i) == "arp"):
			logging.warning("Sending ARPS")
			send_arp_pkts(1)
	    elif (str(i) == "tcp"):
		    extra_ports = random.randint(1000,40000)
	            send_tcp_syn_pkts(1,extra_ports,BURST_TIMER)
	    elif (str(i) == "open"):
		    send_bgp_open(1)
		    #x = x + 2
	    elif (str(i) == "stat"):
		get_total()
	    else:
		try:
			get_info(str(i))
		except:
			logging.critical("Invalid IP Address- Not in List")
            i=raw_input("")
	except KeyboardInterrupt:
		exit
	KILLALL = 0
	pool.joinAll(False,False)
	logging.shutdown()
	os.popen("kill -9 "+str(main_t1))
	sys.exit
    except:
        traceback.print_exc()
    


# MAIN ENDS Here.
