import tkinter as tk
import tkinter.messagebox
import socket
from Crypto import Signature
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA

keyPairs = []  # keys are stored as type 'str'
host = '127.0.0.1'
port_key_generator = 8000
port_votes_calculator = 8001


def create_radio_btn():
    global btn_a, btn_b, btn_c, candidate
    candidate = tk.StringVar()
    btn_a = tk.Radiobutton(text='A', variable=candidate, value='A', width=20)
    btn_b = tk.Radiobutton(text='B', variable=candidate, value='B', width=20)
    btn_c = tk.Radiobutton(text='C', variable=candidate, value='C', width=20)

    btn_a.grid(column=0, row=1)
    btn_b.grid(column=1, row=1)
    btn_c.grid(column=2, row=1)

def vote():
    if(candidate.get() != ""):
        showtext = 'vote for '+candidate.get()+', sure?'
        # tkinter.messagebox.showinfo(message=showtext, title='vote')
        get_rsa_key_pair()
        send_vote(candidate.get().encode())


def create_submit_btn():
    global submit_btn
    submit_btn = tk.Button(text='vote', command=vote)

    submit_btn.grid(column=0, row=2)

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

def send_vote(candidate):
    signature = create_signature(candidate)

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
    length_of_candidate = len(candidate)
    client.sendall(str(length_of_candidate).zfill(4).encode())

    # send hashed message to server
    out_to_server_stream = candidate
    client.sendall(out_to_server_stream)

def create_signature(candidate):
    privateKey = RSA.import_key(keyPairs[0][1], passphrase='project')
    print(type(privateKey))
    print(privateKey)
    h = SHA256.new(candidate)
    signature = pkcs1_15.new(privateKey).sign(h)
    return signature

window = tk.Tk()
window.title('voter')
window.geometry('600x400')

content = tk.Frame(window)
frame = tk.Frame(content, borderwidth=3, relief='ridge', width=50, height=20)

label1 = tk.Label(window, text='voter', bg='yellow', fg='black', width=50)
label1.grid(column=0, row=0, columnspan=3)
create_radio_btn()
create_submit_btn()

window.mainloop()
