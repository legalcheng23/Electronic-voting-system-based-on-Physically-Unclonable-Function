from pymongo import MongoClient
conn = MongoClient()
db = conn.local
collection_vote_result = db.vote_result # 存候選人票數
cursor2 = collection_vote_result.find_one({'candidate':'Teacher Huang'})
print(cursor2)
print('123')