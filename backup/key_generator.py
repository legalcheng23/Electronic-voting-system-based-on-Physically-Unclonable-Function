from Crypto import Random
from Crypto import PublicKey
from Crypto.PublicKey import RSA
import socket

secretCode = 'project'

# dictionary, key = hash of public key, value = tuple of public and private key
keyDict = {}


def generate_key():
    print('generate new key')
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024)

    # RSA private key
    private_key = rsa_key.export_key(passphrase=secretCode, pkcs=8,
                                     protection='scryptAndAES128-CBC')

    # RSA public key
    public_key = rsa_key.public_key().export_key()

    keyDict[hash(public_key)] = (public_key, private_key)
    return public_key


def create_socket():
    HOST = '127.0.0.1'
    PORT = 8000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)

    while True:
        conn, addr = server.accept()
        while True:
            client_msg = str(conn.recv(1024), encoding='utf-8')

            if len(client_msg) == 0:
                conn.close()
                print('client connection closed')
                break

            elif hash(client_msg) in keyDict:  # received public key from voter

                return_msg = keyDict[hash(client_msg)][1]  # return private key to voter

                print('public key exists, returning private key')
                print('returning msg:\n', return_msg, '\n')
                conn.sendall(return_msg)
            else:  # receive request of public key
                print('received client msg:\n', client_msg, '\n')

                return_msg = generate_key()  # return a public key
                print('returning msg:\n', str(return_msg), '\n')

                conn.sendall(return_msg)


create_socket()
input()
