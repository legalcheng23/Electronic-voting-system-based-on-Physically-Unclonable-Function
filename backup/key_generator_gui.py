from Crypto import Random
from Crypto import PublicKey
from Crypto.PublicKey import RSA
import socket
import tkinter as tk
import threading

secretCode = 'project'

# dictionary, key = hash of public key, value = tuple of public and private key
keyDict = {}
window = tk.Tk()
window.geometry('600x400')
window.title('key_generator')

label1 = tk.Label(window, text='generated key pairs')
label1.grid(row=1)


def generate_key():
    random_generator = Random.new().read
    rsa_key = RSA.generate(1024)

    # RSA private key
    private_key = rsa_key.export_key(passphrase=secretCode, pkcs=8,
                                     protection='scryptAndAES128-CBC')

    # RSA public key
    public_key = rsa_key.public_key().export_key()

    keyDict[hash(public_key)] = (public_key, private_key)
    print('generated key pairs:\n', public_key.decode(), '\n', private_key.decode())

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
            client_msg = conn.recv(1024)

            if len(client_msg) == 0:
                conn.close()
                print('client connection closed')
                break

            elif hash(client_msg) in keyDict:  # received public key from voter

                return_msg = keyDict[hash(client_msg)][1]  # return private key to voter

                print('public key exists, returning private key')
                print('received msg:\n', client_msg)
                print('returning msg:\n', return_msg, '\n')
                conn.sendall(return_msg)
                conn.close()
                break
            else:  # receive request of public key
                print('received client msg:\n', client_msg, '\n')

                return_msg = generate_key()  # return a public key
                print('returning msg:\n', str(return_msg), '\n')

                conn.sendall(return_msg)
                conn.sendall('\n'.encode())


def start():
    thread = threading.Thread(target=create_socket)
    thread.start()


btn_start = tk.Button(window, text='start', command=start)
btn_start.grid(row=0)
window.mainloop()
# create_socket()
input()
