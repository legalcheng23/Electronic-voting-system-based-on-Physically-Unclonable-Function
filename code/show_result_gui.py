# pip install Pillow
import tkinter as tk
from pymongo import MongoClient
from PIL import Image, ImageTk
conn = MongoClient()

db = conn.local
collection = db.vote_result
collection.stats

candidate_1 = 'King Lee'
candidate_2 = 'Teacher Huang'
candidate_3 = 'Student Chu'
window = tk.Tk()
window.title('invoicing')
window.geometry('500x300')
txt1 = ''
txt2 = ''
txt3 = ''

cursor = collection.find_one({'candidate':candidate_1})
if cursor is not None:
    txt1 = ' '+candidate_1+'\nNumber of votes: '+str(cursor['votes'])
    pass

cursor = collection.find_one({'candidate':candidate_2})
if cursor is not None:
    txt2 = ' '+candidate_2+'\nNumber of votes: '+str(cursor['votes'])
    pass

cursor = collection.find_one({'candidate':candidate_3})
if cursor is not None:
    txt3 = ' '+candidate_3+'\nNumber of votes: '+str(cursor['votes'])
    pass

img1 = Image.open('./pic/1.jpg')
img1 = img1.resize((150, 150))
imgTk1 = ImageTk.PhotoImage(img1)
label_img1 = tk.Label(window, image=imgTk1)
label_img1.grid(column=0, row=1)

img2 = Image.open('./pic/2.jpg')
img2 = img2.resize((150, 150))
imgTk2 = ImageTk.PhotoImage(img2)
label_img2 = tk.Label(window, image=imgTk2)
label_img2.grid(column=1, row=1)

img3 = Image.open('./pic/3.jpg')
img3 = img3.resize((150, 150))
imgTk3 = ImageTk.PhotoImage(img3)
label_img3 = tk.Label(window, image=imgTk3)
label_img3.grid(column=2, row=1)

pad = tk.Label(window, text="")
pad.grid(row=0, column=0)

label1= tk.Label(window, text=txt1, font=('Arial', 18))
label1.grid(column=0, row=2)

label2= tk.Label(window, text=txt2, font=('Arial', 18))
label2.grid(column=1, row=2)

label3= tk.Label(window, text=txt3, font=('Arial', 18))
label3.grid(column=2, row=2)

print(txt1)
print(txt2)
print(txt3)
window.mainloop()
