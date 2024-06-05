from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

conn = MongoClient()

db = conn.local
collection = db.mymongodb2
collection.stats

# collection.insert_one({'_id':'uid3', 'time':datetime.datetime.utcnow(), 'value':1})
cursor = collection.find_one({'_id':'uid3'})
if cursor is None:
    print('none')
else:
    collection.update_one({'_id':'uid3'}, { '$set':{'value':cursor['value']+1}})
    
# cursor = collection.find().sort("time", -1)
# for c in cursor:
#     print(c)
# print(cursor[1])