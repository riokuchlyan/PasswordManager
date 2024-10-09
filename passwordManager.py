import tkinter as tk
import random
import string
import csv
from cryptography.fernet import Fernet
import base64
import os

#global variables
passwords=[["!!!Username", "Note", "Password"]]
masterPassword=''

#create directories for data
absolute_path = os.path.dirname(__file__)
relative_path="password_manager_data"
working_path=os.path.join(absolute_path, relative_path)
try:
    os.makedirs(working_path)
except:
    pass

#read csv file and show in window and sync passwords list
def initialization():
    textOutput.delete(1.0,tk.END)
    try:
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKey:
            key = dataKey.read()
        #initalize key
        fernet=Fernet(key)
        #open encrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as encryptedFile:
            encryptedData=encryptedFile.read()
        #decrypt data
        decryptedData=fernet.decrypt(encryptedData)
        #writing unencrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as encryptedFileTwo:
            encryptedFileTwo.write(decryptedData)
        #output decrypted passwords to GUI
        with  open(os.path.join(working_path,"data.csv"), newline='') as decryptedFile:
            reader=csv.reader(decryptedFile, delimiter=' ', quotechar='|')
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
        #encrypt data again
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKeyTwo:
            key = dataKeyTwo.read()
        #initalize key
        fernet=Fernet(key)
        #open unencrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as unencryptedFile:
            unencryptedData=unencryptedFile.read()
        #encrypted data
        encryptedData=fernet.encrypt(unencryptedData)
        #writing encrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as unencryptedFileTwo:
            unencryptedFileTwo.write(encryptedData)
        return
    except:
        return

#exports csv
def export():
    try:
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKey:
            key = dataKey.read()
        #initalize key
        fernet=Fernet(key)
        #open encrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as encryptedFile:
            encryptedData=encryptedFile.read()
        #decrypt data
        decryptedData=fernet.decrypt(encryptedData)
        #writing unencrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as encryptedFileTwo:
            encryptedFileTwo.write(decryptedData)
        with open(os.path.join(working_path,"exportedPasswords.csv") , 'wb') as exportedFile:
            exportedFile.write(decryptedData)
        #encrypt data again
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKeyTwo:
            key = dataKeyTwo.read()
        #initalize key
        fernet=Fernet(key)
        #open unencrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as unencryptedFile:
            unencryptedData=unencryptedFile.read()
        #encrypted data
        encryptedData=fernet.encrypt(unencryptedData)
        #writing encrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as unencryptedFileTwo:
            unencryptedFileTwo.write(encryptedData)
        #output export
        textOutput.delete(1.0,tk.END)
        textOutput.insert(tk.END, "Exported.")
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
    with open(os.path.join(working_path,"data.csv"), 'w', newline='') as data:
        writer=csv.writer(data)
        passwords.sort()
        writer.writerows(passwords)
    #open key file
    try:
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKey:
            key = dataKey.read()
        #initalize key
        fernet=Fernet(key)
        #open unencrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as dataTwo:
            unencryptedData=dataTwo.read()
        #encrypted data
        encryptedData=fernet.encrypt(unencryptedData)
        #writing encrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as dataThree:
            dataThree.write(encryptedData)
    except:
        #creates dataKey file and reruns function
        key=Fernet.generate_key()
        with open(os.path.join(working_path,"dataKey.key"), 'wb') as dataKey:
            dataKey.write(key)
        writeToCSV()
    return

#searches entries that contain search term
def search():   
    textOutput.delete(1.0,tk.END)
    textOutput.insert(tk.END, "Search Results: ")
    textOutput.insert(tk.END, "\n")
    counter=1
    addedToSearch=[]
    searchItem=searchVar.get()
    #search algorithm
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
    with open(os.path.join(working_path,"masterPasswordKey.key"), 'rb') as masterPasswordKey:
        #get key for decryption
        key=masterPasswordKey.read()
        fernet=Fernet(key)
        decryptedMasterPassword=fernet.decrypt(masterPasswordEncrypted).decode()
    if passwordVar.get() != decryptedMasterPassword:
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
    def destroyHelpWindow():
        helpWindow.destroy()
    helpWindow=tk.Tk()
    helpWindow.title("Help")
    helpWindow.geometry("310x200")
    helpWindow.resizable(False, False)
    helpWindow.eval('tk::PlaceWindow . center')
    helpWindowLabel=tk.Label(helpWindow, text="To reset the password, click reset on the\nlogin screen. This will erase all data \n and reset the program.")
    helpWindowLabel.place(x=25,y=40)
    helpWindowReturnButton=tk.Button(helpWindow, text="Return", command=destroyHelpWindow)
    helpWindowReturnButton.place(x=115, y=120)
    helpWindow.mainloop()
    return

#overwrites all files to blank
def deleteAllData():
    try:
        with open(os.path.join(working_path,"data.csv"), 'wb') as dataFile:
            dataFile.write(b'')
        with open(os.path.join(working_path,"dataKey.key"), 'wb') as dataKeyFile:
            dataKeyFile.write(b'')
        with open(os.path.join(working_path,"masterPasswordKey.key"), 'wb') as masterPasswordKeyFile:
            masterPasswordKeyFile.write(b'')
        with open(os.path.join(working_path,"masterPassword.key"), 'wb') as masterPasswordFile:
            masterPasswordFile.write(b'')
        loginWindow.destroy()
        os._exit
        quit()
    except:
        pass

#reset password
def reset():
    def destroyResetWindow():
        resetWindow.destroy()
    resetWindow=tk.Tk()
    resetWindow.title("Reset")
    resetWindow.geometry("310x200")
    resetWindow.resizable(False, False)
    resetWindow.eval('tk::PlaceWindow . center')
    resetWindowLabel=tk.Label(resetWindow, text="Are you sure you want to erase all data. \n This will erase all data \n and reset the program.")
    resetWindowLabel.place(x=25,y=40)
    eraseButton=tk.Button(resetWindow, text="Erase", command=deleteAllData)
    eraseButton.place(x=120, y=110)
    returnButton=tk.Button(resetWindow, text="Return", command=destroyResetWindow)
    returnButton.place(x=120, y=150)
    resetWindow.mainloop()

#initial code starts here
#loginScreen
try:
    reader = open(os.path.join(working_path,"masterPassword.key"), 'rb')
    masterPasswordEncrypted=reader.read()
    reader.close()
    if masterPasswordEncrypted != b'':
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
        resetButton=tk.Button(loginWindow, text="Reset", command=reset)
        askPasswordLabel.place(x=10,y=80)
        askPasswordInput.place(x=120, y=80)
        askPasswordButton.place(x=230, y=80)
        loginWindowOutput.place(x=100,y=120)
        resetButton.place(x=120,y=160)
        loginWindow.mainloop()
    else:
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
        with open(os.path.join(working_path,"masterPassword.key"), 'wb') as file:
            #encrypt and write masterpassword to txt file
            unencryptedMasterPassword=setupPasswordVar.get()
            unencryptedMasterPasswordBytes=unencryptedMasterPassword.encode("utf-8")
            key=base64.urlsafe_b64encode(unencryptedMasterPasswordBytes.ljust(32)[:32])
            with open(os.path.join(working_path,"masterPasswordKey.key"), 'wb') as fileTwo:
                fileTwo.write(key)
            fernet=Fernet(key)
            encryptedMasterPassword=fernet.encrypt(unencryptedMasterPassword.encode())
            file.write(encryptedMasterPassword)
 
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
    with open(os.path.join(working_path,"masterPassword.key"), 'wb') as file:
        #encrypt and write masterpassword to txt file
        unencryptedMasterPassword=setupPasswordVar.get()
        unencryptedMasterPasswordBytes=unencryptedMasterPassword.encode("utf-8")
        key=base64.urlsafe_b64encode(unencryptedMasterPasswordBytes.ljust(32)[:32])
        with open(os.path.join(working_path,"masterPasswordKey.key"), 'wb') as fileTwo:
            fileTwo.write(key)
        fernet=Fernet(key)
        encryptedMasterPassword=fernet.encrypt(unencryptedMasterPassword.encode())
        file.write(encryptedMasterPassword)

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
showAllButton=tk.Button(window, text="Return", command=initialization)
deleteItemLabel=tk.Label(window, text="Enter item number to delete: ")
deleteItemInput=tk.Entry(window, width=5, textvariable=deleteVar)
deleteItemButton=tk.Button(window, text="Delete", command=delete)
helpButton=tk.Button(window, text="Help", command=getHelp)
exportButton=tk.Button(window, text="Export", command=export)

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
exportButton.place(x=460, y=550)
window.update()

#starts main GUI and initializaiton 
initialization()
window.mainloop()