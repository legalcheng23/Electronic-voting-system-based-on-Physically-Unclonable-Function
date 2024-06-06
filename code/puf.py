import serial 
import hashlib
COM_PORT = 'COM4'    
BAUD_RATES = 9600    
ser = serial.Serial(COM_PORT, BAUD_RATES)  
ser1=serial.Serial('COM3',9600)
def UID():
    try:
        while True:
            while ser.in_waiting:        
                data_raw = ser.readline()  
                data = data_raw.decode()   
                print('Information Received：', data)
                return data
    except ValueError:
        ser.close()   
        print('bye！')

def PUF():
    try:
        while True:
            while ser1.in_waiting:        
                data_raw1=ser1.readline()
                data1=data_raw1.decode()
                print('Information Received：', data1)
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
    #print(tmp)
    return tmp
    

def sha1hash(text):
    s = hashlib.sha1()
    s.update(text.encode("utf-8"))
    #print(s.hexdigest())
    #print(text)
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
    tmp1 = hashpuf(PUF(),"GuoChengLee")
    tmp2 = hashpuf(PUF(),UID())
    tmp3 = hashpuf(PUF(), tmp2+tmp1)
    print(tmp1)
    print(tmp2)
    print(tmp3)
    
main()