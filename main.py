import tkinter as tk

passwords=[]

def addToPasswordsList(username, note, password):
    item=[username, note, password]
    passwords.append(item)

def job():
    print(passwords)
    window.after(2000, job)

#GUI
window=tk.Tk()
textOutput = tk.Text(window, height = 500, width = 800)
window.title("Password Manager")
window.geometry("900x500")

#variables
userNameVar=tk.StringVar()
notesVar=tk.StringVar()
passwordVar=tk.StringVar()  

#label and buttons
entryLabelUsername=tk.Label(window, text="Username: ")
entryInputUsername=tk.Entry(window, textvariable=userNameVar)
entryLabelNote=tk.Label(window, text="Note: ")
entryInputNote=tk.Entry(window, textvariable=notesVar)
entryLabelPassword=tk.Label(window, text="Password: ")
entryInputPassword=tk.Entry(window, textvariable=passwordVar)
#button does not work
addButton=tk.Button(window, text="Add", command=addToPasswordsList(userNameVar.get(), notesVar.get(), passwordVar.get()))

#place tkinter widgets
#textOutput.pack()
entryLabelUsername.place(x=20, y=450)
entryInputUsername.place(x=90, y=450)
entryLabelNote.place(x=300, y=450)
entryInputNote.place(x=340, y=450)
entryLabelPassword.place(x=550, y=450)
entryInputPassword.place(x=620, y=450)
addButton.place(x=830, y=450)
window.update()

window.after(2000, job)

while True:
    window.update()


"""
links:
https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
https://www.geeksforgeeks.org/how-to-encrypt-and-decrypt-strings-in-python/

functions include:
generating strong passwords
hashing and encrypting given passwords
exporting passwords to csv
checking weak passwords database to warn against weak passwords
"""