import tkinter as tk
import random
import string
import csv

#global variables
passwords=[["!!!Username", "Note", "Password"]]
masterPassword=''

#read csv file and show in window and sync passwords list
def initialization():
    textOutput.delete(1.0,tk.END)
    try:
        with  open('localPasswordManagerData.csv', newline='') as file:
            reader=csv.reader(file, delimiter=' ', quotechar='|')
            counter=1
            for row in reader:
                rowList=row[0].split(',')   
                if rowList != ["!!!Username", "Note", "Password"]:
                    if rowList not in passwords:
                        passwords.append(rowList)
                    labeledPasswordEntry=str(counter) + ") " + "Username: " + rowList[0] + " | " + "Note: " + rowList[1] + " | " + "Password: " + rowList[2]
                    textOutput.insert(tk.END, labeledPasswordEntry)
                    textOutput.insert(tk.END, "\n")
                    counter=counter+1
        return
    except:
        return

#adds entry to passwords list and updates CSV
def addToPasswordsList():
    item=[userNameVar.get(), notesVar.get(), passwordVar.get()]
    for i in passwords:
        if item == i:
            return
    if userNameVar.get()[0]=="!" or userNameVar.get()[0]<"!":
        textOutput.delete(1.0, tk.END)
        textOutput.insert(tk.END, "Can't start username with '!' or ' '.")
        return
    passwords.append(item)

    writeToCSV()
    initialization()
    return

#write and encrypt password data to csv file
def writeToCSV():
    with open('localPasswordManagerData.csv', 'w', newline='') as file:
        writer=csv.writer(file)
        passwords.sort()
        writer.writerows(passwords)
        return

#searches entries that contain search term
def search():   
    textOutput.delete(1.0,tk.END)
    textOutput.insert(tk.END, "Search Results: ")
    textOutput.insert(tk.END, "\n")
    counter=1
    addedToSearch=[]
    searchItem=searchVar.get()

    if searchVar.get() != "":
        for list in passwords:
            for item in list:
                if searchItem in item:
                    if list not in addedToSearch:
                        addedToSearch.append(list)
                        labeledPasswordEntry=str(counter) + ") " + "Username: " + list[0] + " | " + "Note: " + list[1] + " | " + "Password: " + list[2]
                        textOutput.insert(tk.END, labeledPasswordEntry)
                        textOutput.insert(tk.END, "\n")
                        counter=counter+1
    return

#generates random 15 character password and outputs it
def generateStrongPassword():
    generatePasswordOutput.delete(1.0,tk.END)
    characters = string.ascii_letters + string.digits + string.punctuation
    generatedPassword = ''.join(random.choice(characters) for i in range(15))
    generatePasswordOutput.insert(tk.END, generatedPassword)
    return

#delete entry from passwords list and update CSV file
def delete():
    deleteIndex=int(deleteVar.get())
    if deleteIndex != 0:
        try:
            passwords.remove(passwords[deleteIndex])
        except:
            return
    writeToCSV()
    initialization()
    return

#checks for correct master password
def checkLogin():
    if passwordVar.get() != masterPassword[0]:
        loginWindowOutput.delete(1.0,tk.END)
        loginWindowOutput.insert(tk.END, "Wrong Password")
        return
    loginWindow.destroy()
    return

#destroy setup window 
def destroySetupWindow():
    setupWindow.destroy()

#creates help window
def getHelp():
    return

#loginScreen
try:
    with open('login.csv', newline='') as file:
        reader=csv.reader(file, delimiter=' ', quotechar='|')
        for row in reader:
            masterPassword=row

    if masterPassword[0] != '':
        loginWindow=tk.Tk()
        loginWindow.title("Login")
        loginWindow.geometry("310x200")
        loginWindow.resizable(False, False)
        loginWindow.eval('tk::PlaceWindow . center')

        passwordVar=tk.StringVar()
        askPasswordLabel=tk.Label(loginWindow, text="Enter Password: ")
        askPasswordInput=tk.Entry(loginWindow, width=10, textvariable=passwordVar)
        askPasswordButton=tk.Button(loginWindow, text="Login", command=checkLogin)
        loginWindowOutput=tk.Text(loginWindow, height=2, width=15)

        askPasswordLabel.place(x=10,y=80)
        askPasswordInput.place(x=120, y=80)
        askPasswordButton.place(x=230, y=80)
        loginWindowOutput.place(x=100,y=120)

        loginWindow.mainloop()
 
except:
    setupWindow=tk.Tk()
    setupWindow.title("Setup Master Password")
    setupWindow.geometry("310x200")
    setupWindow.resizable(False, False)
    setupWindow.eval('tk::PlaceWindow . center')

    setupPasswordVar=tk.StringVar()
    setupPasswordLabel=tk.Label(setupWindow, text="Create your master password. \n This can not be recovered if forgotten.")
    setupPasswordInput=tk.Entry(setupWindow, width=10, textvariable=setupPasswordVar)
    setupPasswordButton=tk.Button(setupWindow, text="Enter", command=destroySetupWindow)

    setupPasswordLabel.place(x=35, y=55)
    setupPasswordInput.place(x=105,y=100)
    setupPasswordButton.place(x=120, y=150)

    setupWindow.mainloop()

    with open('login.csv', 'w') as file:
        file.write(setupPasswordVar.get())

#mainGUI
window=tk.Tk()
textOutput = tk.Text(window, height = 33, width = 127)
window.title("Password Manager")
window.geometry("900x600")
window.resizable(False, False)
window.eval('tk::PlaceWindow . center')

#variables
userNameVar=tk.StringVar()
notesVar=tk.StringVar()
passwordVar=tk.StringVar()
searchVar=tk.StringVar()
deleteVar=tk.StringVar()

#tkinter widgets
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
deleteItemLabel=tk.Label(window, text="Enter item number to delete: ")
deleteItemInput=tk.Entry(window, width=5, textvariable=deleteVar)
deleteItemButton=tk.Button(window, text="Delete", command=delete)
helpButton=tk.Button(window, text="Help", command=getHelp)

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
deleteItemLabel.place(x=20, y=550)
deleteItemInput.place(x=205, y=550)
deleteItemButton.place(x=265, y=550)
helpButton.place(x=370, y=550)
window.update()

#start program
initialization()

window.mainloop()

#function yet to add: 
    #encrypting and decrypting master password and passwords in CSV files
    #add reset functionality that resets master password and clears csv file