from pymongo import MongoClient
conn = MongoClient()
db = conn.local
collection_vote_result = db.vote_result 
cursor2 = collection_vote_result.find_one({'candidate':'Teacher Huang'})
print(cursor2)
print('123')