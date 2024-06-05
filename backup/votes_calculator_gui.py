from Crypto import PublicKey
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import socket
import threading
import tkinter as tk
import tkinter.messagebox

HEADER = 64
host = '127.0.0.1'
print(host)
port = 8001
FORMAT = 'utf-8'
global A, B, C, threadnum, Connectionnum
A = 0
B = 0
C = 0
threadnum = ""
Connectionnum = ""
windows = tk.Tk()
windows.geometry('500x500')
text = tk.StringVar()
text1 = tk.StringVar()
text2 = tk.StringVar()
vote = 'A:' + str(A) + ' B: ' + str(B) + ' C: ' + str(C)
text.set(vote)
text1.set('投票數：' + str(threadnum))
text2.set(Connectionnum)
label = tk.Label(windows, textvariable=text)
label.pack()
label1 = tk.Label(windows, textvariable=text1)
label1.pack()
label2 = tk.Label(windows, textvariable=text2)
label2.pack()


def handle_client(conn, addr):
    global Connectionnum
    print(f"[NEW CONNECTION] {addr} connected.")
    Connectionnum += (str(addr[1]) + "   connected.\n")
    print(Connectionnum)
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
            connected = False
    conn.close()


def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print('listen on port 8001')
    global A, B, C, threadnum, Connectionnum

    def refreshText():
        vote = 'A:' + str(A) + ' B: ' + str(B) + ' C: ' + str(C)
        text.set(vote)
        text1.set('投票數： ' + str(threadnum))
        text2.set(Connectionnum)
        # windows.after(200, refreshText)
        # windows.mainloop()

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
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
                threadnum = threading.activeCount() - 1
                print('activecount = ', threading.activeCount())
                print('public key:\n', str(public_key), '\n')
                print('signature:\n', str(signature), '\n')
                print('message:\n', str(message)[2:3], '\n')
                print(f"[active connections] {threadnum}")
                if str(message)[2:3] == 'A':
                    A = A + 1
                elif str(message)[2:3] == 'B':
                    B = B + 1
                elif str(message)[2:3] == 'C':
                    C = C + 1
                print(' A: ', A, '\n', 'B: ', B, '\n', 'C: ', C, '\n')
            except:
                print('cannot convert received msg to public key')
            try:
                # validate the signature
                h = SHA256.new(message)
                pkcs1_15.new(public_key).verify(h, signature)
                print('signature valid')
                windows.after(200, refreshText)
                # windows.mainloop()
            except ValueError:
                print('signature not valid')


def on_btn_clicked():
    thread = threading.Thread(target=create_socket)
    thread.start()


btn = tk.Button(text='start', command=on_btn_clicked)
btn.pack()
windows.mainloop()
