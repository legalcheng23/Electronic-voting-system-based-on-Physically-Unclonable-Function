import pickle

from Crypto import Random
from Crypto import PublicKey
from Crypto.PublicKey import RSA
import socket
import tkinter as tk
import threading
import base64

secretCode = 'project'

# dictionary, key = hash of public key, value = tuple of public and private key

keyDict = {}  # old, to be deleted
keys = []  # new
window = tk.Tk()
window.geometry('600x400')
window.title('key_generator')

label1 = tk.Label(window, text='generated key pairs')
label1.grid(row=1)


def generate_key():

    random_generator = Random.new().read
    rsa_key = RSA.generate(2048)

    # RSA private key
    private_key = rsa_key.export_key(passphrase=secretCode, pkcs=8,
                                     protection='scryptAndAES128-CBC')

    # RSA public key
    public_key = rsa_key.public_key().export_key()

    keyDict[hash(public_key)] = (public_key, private_key)

    label_text = public_key.decode(encoding='utf-8').split(sep='\n')[1]
    label_text2 = private_key.decode(encoding='utf-8').split(sep='\n')[1]
    label = tk.Label(text=label_text)
    label.grid()
    label2 = tk.Label(text=label_text2)
    label2.grid()
    label3 = tk.Label(text=" ")
    label3.grid()
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

            elif client_msg == 'msg from voter':
                print('msg from voter')

                # prepare to receive public key
                out_msg = 'msg from key generator'
                conn.sendall(out_msg.encode('utf-8'))

                in_msg = conn.recv(4096)
                in_msg = pickle.loads(in_msg)

                try:
                    print(type(in_msg))
                    public_key = RSA.import_key(in_msg)
                    if in_msg in keys:
                        out_msg = 'public key already stored'
                        conn.sendall(out_msg.encode('utf-8'))
                        print('public key already stored')
                        # conn.close()
                        continue
                    else:
                        keys.append(in_msg)
                        out_msg = 'successfully storing key'
                        conn.sendall(out_msg.encode('utf-8'))
                        print('successfully storing key')
                        # conn.close()
                        continue

                except(ValueError, IndexError, TypeError) as e:
                    print(e)
                    out_msg = 'error parsing public key'
                    conn.sendall(out_msg.encode('utf-8'))
                    # conn.close()



def start():
    thread = threading.Thread(target=create_socket)
    thread.start()


btn_start = tk.Button(window, text='start', command=start)
btn_start.grid(row=0)
window.mainloop()
# create_socket()
input()
