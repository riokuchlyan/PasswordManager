import tkinter as tk
import random
import string
import csv

passwords=[["!Username", "Note", "Password"]]

#read csv file and show in window and sync passwords list
def initialization():
    textOutput.delete(1.0,tk.END)
    try:
        with  open('localPasswordManagerData.csv', newline='') as file:
            reader=csv.reader(file, delimiter=' ', quotechar='|')
            counter=1
            for row in reader:
                rowList=row[0].split(',')   
                if rowList != ["!Username", "Note", "Password"]:
                    if rowList not in passwords:
                        passwords.append(rowList)
                    labeledPasswordEntry=str(counter) + ") " + "Username: " + rowList[0] + " | " + "Note: " + rowList[1] + " | " + "Password: " + rowList[2]
                    textOutput.insert(tk.END, labeledPasswordEntry)
                    textOutput.insert(tk.END, "\n")
                    counter=counter+1
        return
    except:
        return

def addToPasswordsList():
    item=[userNameVar.get(), notesVar.get(), passwordVar.get()]
    for i in passwords:
        if item == i:
            return
    passwords.append(item)

    #write and encrypt password data to csv file
    with open('localPasswordManagerData.csv', 'w', newline='') as file:
        writer=csv.writer(file)
        passwords.sort()
        writer.writerows(passwords)

    initialization()

def search():   
    textOutput.delete(1.0,tk.END)
    textOutput.insert(tk.END, "Search Results: ")
    textOutput.insert(tk.END, "\n")
    counter=1
    addedToSearch=[]
    searchItem=searchVar.get()

    #searching algorithm
    for list in passwords:
        for item in list:
            if searchItem in item:
                if item not in addedToSearch:
                    addedToSearch.append(list)
                    labeledPasswordEntry=str(counter) + ") " + "Username: " + list[0] + " | " + "Note: " + list[1] + " | " + "Password: " + list[2]
                    textOutput.insert(tk.END, labeledPasswordEntry)
                    textOutput.insert(tk.END, "\n")
                    counter=counter+1
    return

def generateStrongPassword():
    generatePasswordOutput.delete(1.0,tk.END)
    characters = string.ascii_letters + string.digits + string.punctuation
    generatedPassword = ''.join(random.choice(characters) for i in range(15))
    generatePasswordOutput.insert(tk.END, generatedPassword)
    return

def job():
    window.after(2000, job)


#GUI
window=tk.Tk()
textOutput = tk.Text(window, height = 33, width = 127)
window.title("Password Manager")
window.geometry("900x550")
window.resizable(False, False)
window.eval('tk::PlaceWindow . center')


#variables
userNameVar=tk.StringVar()
notesVar=tk.StringVar()
passwordVar=tk.StringVar()
searchVar=tk.StringVar()

#label and buttons
entryLabelUsername=tk.Label(window, text="Username: ")
entryInputUsername=tk.Entry(window, textvariable=userNameVar)
entryLabelNote=tk.Label(window, text="Note: ")
entryInputNote=tk.Entry(window, textvariable=notesVar)
entryLabelPassword=tk.Label(window, text="Password: ")
entryInputPassword=tk.Entry(window, textvariable=passwordVar)
addButton=tk.Button(window, text="Add", command=addToPasswordsList)
searchBoxLabel=tk.Label(window, text="Search: ")
searchBoxInput=tk.Entry(window, textvariable=searchVar)
searchButton=tk.Button(window, text="Search", command=search)
generatePasswordLabel=tk.Label(window, text="Generate Strong Password: ")
generatePasswordButton=tk.Button(window, text="Generate", command=generateStrongPassword)
generatePasswordOutput=tk.Text(window, height = 1.5, width = 17)
showAllButton=tk.Button(window, text="Show All", command=initialization)

#place tkinter widgets
textOutput.place(x=0,y=0)
entryLabelUsername.place(x=20, y=450)
entryInputUsername.place(x=90, y=450)
entryLabelNote.place(x=300, y=450)
entryInputNote.place(x=340, y=450)
entryLabelPassword.place(x=550, y=450)
entryInputPassword.place(x=620, y=450)
addButton.place(x=830, y=450)
searchBoxLabel.place(x=20, y=500)
searchBoxInput.place(x=75, y=500)
searchButton.place(x=270, y=500)
generatePasswordLabel.place(x=370, y=500)
generatePasswordOutput.place(x=545, y=500)
generatePasswordButton.place(x=680, y=500)
showAllButton.place(x=800, y=500)
window.update()

initialization()

window.after(2000, job)

while True:
    window.update()

"""
functions to include:
hashing and encrypting given passwords
search function
delete inputs
"""

#fix search function and fix bug where adding element with space in front breaks program