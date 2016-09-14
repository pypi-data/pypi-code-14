#############################################
#
#  A Rest API provider for quick save and get of NoSQL Data
#
#############################################

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import pymongo
import pdb
from pymongo import MongoClient
from bson.objectid import ObjectId
import pdb

import os
################################  Define database connections ######################
def norm(a):
    a['uid'] = str(a['_id'])
    del a['_id']
    return a;
class Store(object):
    __instance = None
    database = None
    
    def __new__(cls):
        if Store.__instance is None:
            print '[INFO] Creating the first instnace '
            try:
                Store.__instance = object.__new__(cls)
                client = MongoClient('localhost', 27020)
                Store.database = client['simple_store_common_database']
                print '[INFO] Data base connection Done '
            except Exception ,e:
                print '[ERROR] Not abel to connect Mongo Server. Did you run the deploy.bat ? '
                print e
        return Store.__instance
    
    def __init__(self):
        print '[INFO] __init__ is empty . Nothing done.. ' 

    
    def insert(self,db_name,data):
        if not Store.database: return {'status':'error','msg':'database server not running'}
        try:
            db =  Store.database[db_name]                
            res = db.insert(data)
            return {'status':'success','msg':'Insert successfully','out':str(res),'in':norm(data)}
        except Exception, e:
            return {'status':'error','msg':'Int able to insert ('+str(e)+')'}
            
    def update(self,id, db_name,data):
        return {'status':'error','msg':'Update is not yet suppoted.'}
        """
        if not Store.database: return {'status':'error','msg':'database server not running'}
        try:
            db =  Store.database[db_name]                
            res = db.insert(data)
            return {'status':'success','msg':'Insert successfully','out':str(res),'in':norm(data)}
        except Exception, e:
            return {'status':'error','msg':'Int able to insert ('+str(e)+')'}
            """
            
    def delete(self,db_name,id):
        if not Store.database: return {'status':'error','msg':'database server not running'}
        try:
            db =  Store.database[db_name]          
            #pdb.set_trace()
            res = db.remove({'_id': ObjectId(id)})
            return {'status':'success','msg':'Deleted successfully','out':str(res),'in':id}
        except Exception, e:
            return {'status':'error','msg':'Int able to delete ('+str(e)+')'}
            
    def get(self,db_name,id =None,query=None):
        if not Store.database: return {'status':'error','msg':'database server not running'}
        #pdb.set_trace()
        try:
            db =  Store.database[db_name]          
            if id:
                res = db.find_one({'_id': ObjectId(id)})
                return {'status':'success','msg':'find successfully','res':norm(res),'in':id}
            if query:
                res = [  norm(x)  for x in db.find(query).sort([("_id", pymongo.DESCENDING)])]
                return {'status':'success','msg':'find successfully','out':res,'in':query}
            else:
                res = [  norm(x)  for x in db.find().sort([("_id", pymongo.DESCENDING)])]
                return {'status':'success','msg':'find successfully','out':res,'in':''}
        except Exception, e:
            return {'status':'error','msg':'Int able to find ('+str(e)+')'}

################################  Run Tornado API connections ######################
print "hello"
root = os.path.dirname(os.path.abspath(__file__))
from bson import json_util
import json
class StoreHandler(tornado.web.RequestHandler):
    def get(self, db):
        arguments = self.request.arguments
        id = None
        query = None
        if 'id' in arguments:
            id = str(arguments.get('id')[0])
        else:
            if arguments:
                query  = {}
                for k, v in arguments.items():
                    query[k] = v[0]
            else:
                query = None
        
        res =  Store().get(db,id,query);
        self.write(json.dumps(res, default=json_util.default))
        
    def post(self, db):
        # pdb.set_trace()
        data = json.loads(self.request.body)
        print data
        cmd = data.get('_cmd')
        if cmd == None:
            res = {'status':'error','msg':'SimpleStore client Does not send proper Command'}
            self.write(json.dumps(res, default=json_util.default))
            return;
        del data['_cmd']
        
        #Get command
        if cmd == 'get':
            id = data.get('id')
            query = None
            if id:                     # Building ID
                del data['id']
                id = str(id)
            if data:                   # Building Query
                query  = {}
                for k, v in data.items():
                    query[k] = str(v[0]) 
            #Now call the store API.
            res =  Store().get(db,id,query);
        #Post Command
        elif cmd == 'post':
            id = data.get('id')
            query = None
            if id:                     # Building ID
                del data['id']
                id = str(id)
            if data:                   # Building Query
                query  = {}
                for k, v in data.items():
                    query[k] = str(v) 
            #Now call the store API.
            if id:
                res =  Store().update(db,id,query);
            else:
                res =  Store().insert(db,query);            
        #Post Command
        elif cmd == 'delete':
            id = data.get('id')
            if not id:                     # Building ID
                res = {'status':'error','msg':'SimpleStore client must pass id to delete'}
                self.write(json.dumps(res, default=json_util.default))
                return;
            res =  Store().delete(db,id);
        else:
            res = {'status':'error','msg':'SimpleStore client sends an invalid command'}
        
        #sendout the result to clinet        
        self.write(json.dumps(res, default=json_util.default))
        
print root
application = tornado.web.Application([
    (r"/docs/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "simplestore_index.html"}),
    (r"/api/([a-z0-9]+)", StoreHandler),

], debug=True)



if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


#test
def test():
    g = Store()
    print g.insert('table1',{'name':'dipankar1'})
    print g.insert('table1',{'name':'dipankar2'})
    print g.insert('table1',{'name':'dipankar3'})
    pdb.set_trace();
