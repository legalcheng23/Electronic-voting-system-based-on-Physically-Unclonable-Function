import socket
import sys

from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

keyPairs = []  # keys are stored as type 'str'
host = '127.0.0.1'
port_key_generator = 8000
port_votes_calculator = 8001


def vote():
    print("您想要投的對象是？\n1.黃老師\n2.羅老師\n3.查老師\n請輸入數字投票")
    person = input()
    return {
        '1': "1",
        '2': "2",
        '3': "3",
    }[person]


def get_rsa_key_pair():
    # create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port_key_generator))
    # send msg to server
    client_msg = 'Msg from voter, want to get RSA key pairs.'
    client.sendall(client_msg.encode())
    # receive msg from server (public Key)
    public_key = str(client.recv(2048), encoding='utf-8')
    print('received server msg:\n', public_key, '\n')

    # send public key to server to get private key
    client_msg = public_key
    client.sendall(client_msg.encode())
    private_key = str(client.recv(2048), encoding='utf-8')
    print('received server msg:\n', private_key, '\n')

    keyPairs.append((public_key, private_key))
    return


def send_vote(signature, data):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port_votes_calculator))

    # send the size of following message
    length_of_public_key = len(str(keyPairs[0][0]).encode())
    client.sendall(str(length_of_public_key).zfill(4).encode())  # 不足位數補0

    # send public key to server
    out_to_server_stream = str(keyPairs[0][0])
    client.sendall(out_to_server_stream.encode())

    # send the size of following message
    length_of_signature = len(signature)
    client.sendall(str(length_of_signature).zfill(4).encode())  # 不足位數補0

    # send signature to server
    out_to_server_stream = signature
    client.sendall(out_to_server_stream)

    # send the size of following message
    length_of_data = len(data)
    client.sendall(str(length_of_data).zfill(4).encode())

    # send hashed message to server
    out_to_server_stream = data
    client.sendall(out_to_server_stream)


# 取得投票號碼
vote = vote()
# str to bytes
data = str.encode(vote)
get_rsa_key_pair()
print('public key size: ', len(str(keyPairs[0][0]).encode()))
print('private key size: ', len(str(keyPairs[0][1]).encode()))
input()
if not keyPairs:
    print('missing rsa key pairs')
else:
    # create and send signature to votes_calculator
    privateKey = RSA.import_key(keyPairs[0][1], passphrase='project')
    print(type(privateKey))
    print(privateKey)
    h = SHA256.new(data)
    signature = pkcs1_15.new(privateKey).sign(h)
    send_vote(signature, data)
input()
