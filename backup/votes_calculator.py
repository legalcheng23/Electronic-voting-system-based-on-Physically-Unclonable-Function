from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import socket

host = '127.0.0.1'
port = 8001


def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)

    while True:
        conn, addr = server_socket.accept()
        in_from_client_stream = conn.recv(4)
        length_of_message = int(in_from_client_stream)
        in_from_client_stream = conn.recv(length_of_message)  # receive public key

        if len(in_from_client_stream) == 0:
            print('received msg is empty')
            conn.close()
            print('connection closed\n')
            return
        else:
            print('received msg:\n', str(in_from_client_stream), '\n')
            global public_key, signature, message
            try:
                public_key = RSA.import_key(in_from_client_stream)
                length_of_message = int(conn.recv(4))
                signature = conn.recv(length_of_message)  # receive signature

                length_of_message = int(conn.recv(4))
                message = conn.recv(length_of_message)  # receive original message

                print('public key:\n', str(public_key), '\n')
                print('signature:\n', str(signature), '\n')
                print('message:\n', str(message), '\n')

            except:
                print('cannot convert received msg to public key')

            try:
                # validate the signature
                h = SHA256.new(message)
                pkcs1_15.new(public_key).verify(h, signature)
                print('signature valid')
            except ValueError:
                print('signature not valid')


create_socket()
