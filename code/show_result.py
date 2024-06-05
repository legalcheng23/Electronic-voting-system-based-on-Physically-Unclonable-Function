from pymongo import MongoClient
conn = MongoClient()

db = conn.local
# vote_result 可能需要調整
collection = db.vote_result
collection.stats

candidate_1 = 'King Lee'
candidate_2 = 'Teacher Huang'
candidate_3 = 'Student Chu'

cursor = collection.find_one({'candidate':candidate_1})
if cursor is not None:
    print(candidate_1+'得票數: '+str(cursor['votes']))
    pass

cursor = collection.find_one({'candidate':candidate_2})

if cursor is None:
    print(candidate_2+'得票數: '+str(cursor['votes']))
    pass

cursor = collection.find_one({'candidate':candidate_3})
if cursor is None:
    print(candidate_3+'得票數: '+str(cursor['votes']))

if cursor is not None:
    print(candidate_2+'得票數: '+cursor['votes'])
    pass

cursor = collection.find_one({'candidate':candidate_3})
if cursor is not None:
    print(candidate_3+'得票數: '+cursor['votes'])
    pass
    