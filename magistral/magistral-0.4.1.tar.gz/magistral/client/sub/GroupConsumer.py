'''
Created on 11 Aug 2016
@author: rizarse
'''

import time
import logging
import threading

from kafka.consumer.group import KafkaConsumer
from magistral.client.Configs import Configs
from magistral.client.MagistralException import MagistralException
from kafka.structs import TopicPartition
from magistral.Message import Message

class GroupConsumer(threading.Thread):
        
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
     
    def __init__(self, threadId, name, sKey, bootstrapServers, groupId, permissions, cipher = None):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        
        self.group = groupId;
        self.subKey = sKey;
        
        self.cipher = None if cipher is None else cipher;
                
        configs = Configs.consumerConfigs();
        configs["bootstrap_servers"] = bootstrapServers;
        configs["group_id"] = groupId;
        configs['enable_auto_commit'] = False;
        
        self.__isAlive = True;
        
        self.__consumer = KafkaConsumer(
            bootstrap_servers = bootstrapServers,
            check_crcs = False,
            exclude_internal_topics = True,
            session_timeout_ms = 20000,
            fetch_min_bytes = 128,
            fetch_max_wait_ms = 256,           
            enable_auto_commit = False,
            max_in_flight_requests_per_connection = 10,
            group_id = groupId);
        
        self.permissions = permissions;
        self.map = {}
        
        self.__offsets = {}
        
        
    def recordsTotally(self, data):
        size = 0;
        for val in data.values(): 
            if len(val) > 0: size = size + len(val);
                               
        return size;
    
    def consumerRecord2Message(self, record):                    
        payload = record[6]
                                        
        if self.cipher is not None:
            try:
                payload = self.cipher.decrypt(payload)
            except:
                pass
                                        
        msg = Message(record[0], record[1], payload, record[2], record[3])
        return msg

    def run(self):
        
        threadLock.acquire()
        
        while self.__isAlive:
            try:

                data = self.__consumer.poll(512);
                for values in data.values():
                                         
                    for value in values:
                        msg = self.consumerRecord2Message(value);
                        listener = self.map[msg.topic()][msg.channel()];
                        if listener is not None: listener(msg);
                        
                self.__consumer.commit_async(); 
                    
            except:
                pass
              
        threadLock.release()

#   ////////////////////////////////////////////////////////////////////////////////////    

    def subscribe(self, topic, channel = -1, listener = None, callback = None):
        
        assert channel is not None and isinstance(channel, int), "Channel expected as int argument"        
        if (channel < -1): channel = -1;
                
        etopic = self.subKey + "." + topic;
        
        topics = self.__consumer.topics()
        
        if (etopic not in topics):
            self.logger.error("Topic [" + topic + "] does not exist");
            raise MagistralException("Topic [" + topic + "] does not exist");
                    
        self.logger.debug("Subscribe -> %s : %s | key = %s", topic, channel, self.subKey);
        
        if (self.permissions == None or len(self.permissions) == 0): 
            raise MagistralException("User has no permissions for topic [" + topic + "].");
        
        self.fch = [];
        
        for meta in self.permissions:             
            if (meta.topic() != topic): continue;  
            
            if channel == -1:
                self.fch = meta.channels();
            elif channel in meta.channels():                          
                self.fch = [ channel ];  
        
        if (len(self.fch) == 0): 
            npgex = "No permissions for topic [" + topic + "] granted";
            self.logger.error(npgex);                                
            raise MagistralException(npgex);
        
        if (self.map == None or etopic not in self.map): 
            self.map[etopic] = {}
        
#         // Assign Topic-partition pairs to listen
        
        tpas = [];
        for ch in self.fch:            
            tpas.append(TopicPartition(etopic, ch));
            if (listener is not None): self.map[etopic][ch] = listener;        
        
        self.__consumer.assign(tpas);
                
        if callback is not None: 
            callback(self.__consumer.assignment());
            
        return self.__consumer.assignment();
        
        
    def unsubscribe(self, topic): 
        self.consumer.unsubscribe();
        self.map.remove(topic);
        
        tpas = [];
        for t, chm in self.map.items():
            for p in chm.keys(): tpas.append(TopicPartition(t, p))

        self.consumer.assign(tpas);

    def close(self):
        self.__isAlive = False
        self.__consumer.pause()
        self.__consumer.close()
  
threadLock = threading.Lock()    