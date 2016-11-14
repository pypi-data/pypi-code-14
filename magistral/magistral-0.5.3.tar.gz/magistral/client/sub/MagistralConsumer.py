'''
Created on 13 Aug 2016
@author: rizarse
'''

from kafka.consumer.group import KafkaConsumer
from kafka.structs import TopicPartition
from magistral.Message import Message
from magistral.client.MagistralException import MagistralException

class MagistralConsumer(object):
    
    __HISTORY_DATA_FETCH_SIZE_LIMIT = 10000;

    def __init__(self, pubKey, subKey, secretKey, bootstrap, cipher = None):
        self.__pubKey = pubKey
        self.__subKey = subKey
        self.__secretKey = secretKey
        
        self.__bootstrap = bootstrap
        if cipher is not None: self.__cipher = cipher
    
    def history(self, topic, channel, records):
        
        messages = []
        
        consumer = KafkaConsumer(bootstrap_servers = self.__bootstrap,
            enable_auto_commit = False, session_timeout_ms = 30000, fetch_min_bytes = 32, max_partition_fetch_bytes = 65536);
        
        if (records > self.__HISTORY_DATA_FETCH_SIZE_LIMIT): records = self.__HISTORY_DATA_FETCH_SIZE_LIMIT;
        
        kfkTopic = self.__subKey + "." + topic;
        x = TopicPartition(kfkTopic, channel);
        
        consumer.assign([x]);
        consumer.seek_to_end();        
        last = consumer.position(x);
        
        pos = last - records if last > records else 0;
        consumer.seek(x, pos);
        
        data = consumer.poll(256);   
        
        endIsNotReached = True;
        while endIsNotReached:
            
            if len(data.values()) == 0:
                return messages;
            
            records = list(data.values())
            
            for record in records[0]:
                index = record[2];
                if index >= last - 1: endIsNotReached = False;
                
                message = Message(record[0], record[1], record[6], index, record[3]);
                messages.append(message);
            
            if endIsNotReached == False: 
                consumer.close();
                return messages;
            
            pos = pos + len(messages)
            consumer.seek(x, pos);
            data = consumer.poll(256);
            
        consumer.close();
        
        return messages;
    
    def historyForTimePeriod(self, topic, channel, start, end, limit = -1):
        
        out = []        
        
        try:
            kfkTopic = self.__subKey + "." + topic;
            x = TopicPartition(kfkTopic, channel);
                        
            consumer = KafkaConsumer(bootstrap_servers = self.__bootstrap);
            consumer.assign([x]);
        
            consumer.config['enable_auto_commit'] = False;
            consumer.config['session_timeout_ms'] = 30000;
            consumer.config['fetch_min_bytes'] = 32;
            consumer.config['max_partition_fetch_bytes'] = 65536;
            
            consumer.seek_to_end();        
            last = consumer.position(x);
        
            position = last - 1000;
            
            found = False;
            while found == False:
                consumer.seek(x, position);
                data = consumer.poll(500);
                 
                if x not in data.keys() or len(data[x]) == 0: break;
                
                record = data[x][0];
                timestamp = record[3];
 
                if timestamp < start: 
                    found = True;
                    break;
                 
                position = position - 1000;
             
            consumer.close();
                       
            c = KafkaConsumer(bootstrap_servers = self.__bootstrap);            
            c.assign([x]);
             
            c.config['fetch_min_bytes'] = 32;
            c.config['max_partition_fetch_bytes'] = 65536;
                       
            c.seek(x, position);                        
            data = c.poll(256);
            
            while (x in data.keys() and len(data[x]) > 0):
                
                for record in data[x] :
                    timestamp = record[3];
                    if timestamp < start: continue;
                    
                    index = record[2];
                    
                    if timestamp > end or index >= last - 1:  
                        c.close();                 
                        return out;
                                    
                    message = Message(record[0], record[1], record[6], index, timestamp);
                    out.append(message); 
                    
                    if limit is not None and limit > 0 and len(out) >= limit:
                        c.close();                 
                        return out;                 
                    
                c.seek(x, position + len(data[x]));                        
                data = c.poll(256);
            
            return out;
        
        except:
            
            raise MagistralException("Exception during history invocation occurred");
