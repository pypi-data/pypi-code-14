from pymongo import MongoClient
from datetime import datetime, timedelta

class Queue(object):

    '''
        initialize queue object. A queue is a mongo collection where records awaiting progress are kept. The queue object is the gateway for interacting with a queue.
    '''

    def __init__(self, db, queueName):

        self.queueName = queueName

        self.queue = db[self.queueName]

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

    def add(self, item, batchName=''):

        if type(item) == dict:
            item = [item]

        for row in item:
            row['_timestamp'] = datetime.now()
            row['_counter'] = 0
            row['_batchName'] = batchName
            row['_jobName'] = ''
            row['_lockTimestamp'] = ''

        result = self.queue.insert_many(item)

        return len(result.inserted_ids)

    def next(self, job, limit=1):

        res = self.queue.find({'_jobName': '', '_lockTimestamp': ''}, limit = limit)

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

    def complete(self, records):

        result = self.queue.delete_many({'_id': {'$in': [d['_id'] for d in records]}})

        return result.deleted_count

def clean(job):

    for row in job:
        del row['_id']
        del row['_counter']
        del row['_timestamp']
        del row['_batchName']
        del row['_lockTimestamp']
        del row['_jobName']

    return job
