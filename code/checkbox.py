from tarfile import PAX_NUMBER_FIELDS
import win32api
import serial # 引用pySerial模組
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import subprocess
import base64
conn = MongoClient()
db = conn.local
collection_vote_record = db.vote_record # 存投票結果
collection_PUF=db.mypuf_num # 存puf
collection_vote_record.stats
collection_PUF.stats
COM_PORT = 'COM4'    # 指定通訊埠名稱 uid
BAUD_RATES = 9600    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠
candidate_1 = 'King Lee'
candidate_2 = 'Teacher Huang'
candidate_3 = 'Student Chu'
def UID():
    try:
        while True:
            while ser.in_waiting:          # 若收到序列資料…
                data_raw = ser.readline()  # 讀取一行
                data = data_raw.decode().strip()   # 用預設的UTF-8解碼
                return data      
    except ValueError:
        ser.close()    # 清除序列通訊物件
        print('再見！')

def check():
    cursor = collection_PUF.find().sort("time", -1)
    puf=cursor[0]
    uid=UID()
    print(uid)
    base64_uid=base64.b64encode(uid.encode('UTF-8'))
    check=collection_vote_record.find_one({'uid':base64_uid})
    if check is None:
        win32api.MessageBox(0,"此用戶未投票","注意")
        return 0
    puf_candidate_1 = puf_vote(puf, uid, candidate_1)
    puf_candidate_2 = puf_vote(puf, uid, candidate_2)
    puf_candidate_3 = puf_vote(puf, uid, candidate_3)
    check_result=check["pufsupport"]
    print(check_result)
    if puf_candidate_1==check_result:
        win32api.MessageBox(0,"您投給的是"+candidate_1,"注意")
    elif puf_candidate_2==check_result:
        win32api.MessageBox(0,"您投給的是"+candidate_2,"注意")
    elif puf_candidate_3==check_result:
        win32api.MessageBox(0,"您投給的是"+candidate_3,"注意")
    # print(check["pufresult"])
    

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

def puf_vote(puf,uid,candidate):
    tmp1 = hashpuf(puf,candidate)
    tmp2 = hashpuf(puf,uid)
    tmp3 = hashpuf(puf, tmp2+tmp1)
    return tmp3
while True:
    check()