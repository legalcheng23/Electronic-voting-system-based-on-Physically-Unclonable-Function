from pymongo import MongoClient

conn = MongoClient()

db = conn.local
collection = db.uid_legal
collection.stats

collection.insert_one({'uid':'11100101100111111101111000011'})
collection.insert_one({'uid':'11010111100100110010101100100'})

cursor = collection.find_one({'uid':'11010111100100110010101100100'})
if cursor is not None:
    print(cursor)
    print('legal!')
else:
    print('not legal!')