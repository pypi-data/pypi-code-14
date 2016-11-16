from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from copy import deepcopy

class Queue(object):

    '''
        initialize queue object. A queue is a mongo collection where records awaiting progress are kept. The queue object is the gateway for interacting with a queue.
    '''

    def __init__(self, db, queueName):

        if queueName in ['queueList', 'batchList']:
            raise ValueError('Queue name \'' + queueName + '\' is reserved')

        self.queueName = queueName

        self.queue = db[self.queueName]

        self.db = db

        ## check if an instance already exists
        queueFind = db['queueList'].find_one({'queueName': queueName})

        if queueFind:

            self._id = queueFind['_id']

        else:
            ## create a new instance
            queueNew = db['queueList'].insert_one({'queueName': queueName})
            self._id = queueNew.inserted_id

    def getQueueSize(self):

        return self.queue.count()

    def getQueueStats(self):

        stats = {}
        stats['_counter'] = {}

        stats['_counter']['max'] = self.queue.find_one({}, sort=[('_counter', DESCENDING)])['_counter']
        stats['_counter']['min'] = self.queue.find_one({}, sort=[('_counter', ASCENDING)])['_counter']

        stats['_timestamp'] = {}
        stats['_timestamp']['min'] = (datetime.now() - self.queue.find_one({}, sort=[('_timestamp', DESCENDING)])['_timestamp']).total_seconds()
        stats['_timestamp']['max'] = (datetime.now() - self.queue.find_one({}, sort=[('_timestamp', ASCENDING)])['_timestamp']).total_seconds()

        return stats

    def getAvailSize(self):

        return self.queue.count({'_jobName': '', '_lockTimestamp': ''})

    def add(self, item, batchName='', priority=False):

        if type(item) == dict:
            item = [item]

        if batchName!='':
            newBatch = Batch(batchName=batchName, batchCount=len(item), db=self.db)
            batchID=newBatch.batchID
        else:
            batchID=''

        for row in item:
            row['_timestamp'] = datetime.now()
            row['_counter'] = 0
            row['_batchName'] = batchName
            row['_batchID'] = batchID
            row['_jobName'] = ''
            row['_lockTimestamp'] = ''
            if priority:
                row['_priority'] = 1
            else:
                row['_priority'] = 0

        result = self.queue.insert_many(item)

        if batchName!='':
            returnSet = {}
            returnSet['_insertedCount'] = len(result.inserted_ids)
            returnSet['_batchID'] = batchID

            return returnSet
        else:
            return len(result.inserted_ids)

    def next(self, job, limit=1):

        res = self.queue.find({'_jobName': '', '_lockTimestamp': ''}, limit = limit, sort=[('_priority', DESCENDING)])

        res_id = []

        records = []

        for row in res:

            records.append(row)

            res_id.append(row['_id'])

        lock = self.queue.update_many({'_id': {'$in': res_id}}, update = {'$set': {'_jobName': job, '_lockTimestamp': datetime.now()}, '$inc': {'_counter': 1}})

        return records

    def release(self, release):

        result = self.queue.update_many({'_id': {'$in': [d['_id'] for d in release]}}, {'$set': {'_jobName': '', '_lockTimestamp': ''}})

        return result.modified_count

    def timeout(self, t=300):

        result = self.queue.update_many({'_lockTimestamp': {'$lt': datetime.now() - timedelta(seconds=t)}}, {'$set': {'_jobName': '', '_lockTimestamp': ''}})

        return result.modified_count

    def cleanup(self, n=30):

        result = self.queue.delete_many({'_counter': {'$gte': n}})

        return result.deleted_count

    def complete(self, records, completeBatch=False):

        if completeBatch:

            batchSet = {}
            for record in records:
                if record['_batchID'] in batchSet:
                    batchSet[record['_batchID']] += 1
                else:
                    batchSet[record['_batchID']] = 1

            for batch in batchSet:

                self.db.batchList.update_one({'_id': batch}, {'$inc': {'completeCount': batchSet[batch]}})
                self.db.batchList.update_one({'_id': batch, '$where': 'this.batchCount==this.completeCount'}, {'$set': {'isComplete': True, 'completedTimestamp': datetime.now()}})

        result = self.queue.delete_many({'_id': {'$in': [d['_id'] for d in records]}})
        return result.deleted_count

class Batch(object):

    def __init__(self, batchName, batchCount, db):

        self.batchName = batchName
        self.batchCount = batchCount

        insertBatch = db['batchList'].insert_one({'batchName': batchName, 'batchCount': batchCount, 'timestamp': datetime.now(), 'completeCount': 0, 'isComplete': False})

        self.batchID = insertBatch.inserted_id

def clean(data):

    dataClean = deepcopy(data)

    for row in dataClean:
        del row['_id']
        del row['_counter']
        del row['_timestamp']
        del row['_batchName']
        del row['_lockTimestamp']
        del row['_jobName']
        del row['_priority']
        del row['_batchID']

    return dataClean
