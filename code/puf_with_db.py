from tarfile import PAX_NUMBER_FIELDS
import win32api
import serial # 引用pySerial模組
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import subprocess
import base64
COM_PORT = 'COM4'    
BAUD_RATES = 9600    
ser = serial.Serial(COM_PORT, BAUD_RATES) 
ser1=serial.Serial('COM3',9600) # puf
candidate_1 = 'King Lee'
candidate_2 = 'Teacher Huang'
candidate_3 = 'Student Chu'

conn = MongoClient()
db = conn.local
collection_vote_record = db.vote_record 
collection_PUF=db.mypuf_num 
collection_vote_result = db.vote_result 
c2 = db.uid_legal 

collection_vote_record.stats
collection_PUF.stats
c2.stats
collection_vote_result.stats

cursor = collection_vote_result.find_one({'candidate':candidate_1})
if cursor is None:
    collection_vote_result.insert_one({'candidate':candidate_1, 'votes':0})
    pass

cursor = collection_vote_result.find_one({'candidate':candidate_2})
if cursor is None:
    collection_vote_result.insert_one({'candidate':candidate_2, 'votes':0})
    pass

cursor = collection_vote_result.find_one({'candidate':candidate_3})
if cursor is None:
    collection_vote_result.insert_one({'candidate':candidate_3, 'votes':0})
    pass

def UID():
    try:
        while True:
            while ser.in_waiting:          
                data_raw = ser.readline()  
                data = data_raw.decode().strip()   
                base64_uid=base64.b64encode(data.encode('UTF-8'))
                cursor_uid = collection_vote_record.find_one({'uid':base64_uid})
                if cursor_uid is None:
                    cursor = c2.find_one({'uid':data})
                    if cursor is not None:
                        print('legal!')
                        str = 'PUF E-voting System.exe'
                        win32api.ShellExecute(0,'open',str,'','',1)
                        while True:
                            out=subprocess.call('tasklist |find /i"PUF_E-voting_System.exe"',shell=True)
                            if out==1:
                                return data  
                    else:
                        print(data)
                        print('not legal!')  
                else:
                    win32api.MessageBox(0,"This user has already voted","!!")
                    return 0
                                
    except ValueError:
        ser.close()   
        print('bye！')

def PUF():
    try:
        while True:
            while ser1.in_waiting:        
                data_raw1=ser1.readline()
                data1=data_raw1.decode()
                cursor = collection_PUF.find_one({'puf':data1})
                if cursor is None:
                    collection_PUF.insert_one({'puf':data1, 'time':datetime.datetime.utcnow()})
                    print('insert data successfully!')
                else:
                    print('this puf already exists in db!')
                print(data1)
                return data1
    except ValueError:
        ser1.close()   
        print('bye！')

def hashpuf(Puf,candidate):
    BinaryString = ''
    Puf_list=list(Puf)
    Candidate_list=list(candidate)
    for i in range(0,len(Candidate_list)):
        BinaryString+=DecimalToBinary(ord(Candidate_list[i]))
    for i in range(0,len(Puf_list)):
        BinaryString+=Puf_list[i]
    tmp = sha1hash(BinaryString)
    return tmp
    

def sha1hash(text):
    s = hashlib.sha256()
    s.update(text.encode("utf-8"))
    return s.hexdigest()


def DecimalToBinary(number): 
    num = []
    while True:
        a = number // 2
        b = number % 2
        num += [str(b)]
        number = a
        if number == 0:
            break
    return ''.join(num[::-1])
def main():
    cursor = collection_PUF.find().sort("time", -1)
    puf=cursor[0]
    uid = UID()
    if uid == 0:
        return
    base64_uid=base64.b64encode(uid.encode('UTF-8'))
    print(uid)
    candidate = get_candidate().strip()
    print(candidate)
    puf_candidate_support=puf_vote(puf,uid,candidate)
    puf_candidate_1 = puf_vote(puf, uid, candidate_1)
    puf_candidate_2 = puf_vote(puf, uid, candidate_2)
    puf_candidate_3 = puf_vote(puf, uid, candidate_3)
    
    print('uid: ' +uid)
    print('result: ')
    print(puf_candidate_support)

    cursor = collection_vote_record.find_one({'uid':base64_uid})
    cursor2 = collection_vote_result.find_one({'candidate':candidate})
    if cursor is None and cursor2 is not None:
        collection_vote_record.insert_one({'uid':base64_uid, 'pufraw':puf,
                               'puf_candidate_1':puf_candidate_1,
                               'puf_candidate_2':puf_candidate_2,
                               'puf_candidate_3':puf_candidate_3,
                               'pufsupport':puf_candidate_support})
        votes = cursor2['votes']
        collection_vote_result.update_one({'candidate':candidate}, {'$set':{'votes':votes+1}})
        print('insert data successfully!')
    else:
        print('this uid already exists in db!')
    pass
def puf_vote(puf,uid,candidate):
    tmp1 = hashpuf(puf,candidate)
    tmp2 = hashpuf(puf,uid)
    tmp3 = hashpuf(puf, tmp2+tmp1)
    return tmp3

ser_vote = serial.Serial('COM1', 9600) 

def get_candidate():
    data=""
    while 1:
        while ser_vote.inWaiting():
            data2 = ser_vote.readline()
            data = data2.decode()
            if data != '':
                print(data)
                return data
    return 'lee'

cursor = collection_PUF.find_one({})
if cursor is None:
    print('generating puf ...')
    PUF()
else:
    print('puf already exists')
while True:
    main()

