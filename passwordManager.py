import customtkinter as CTk
import random
import string
import csv
from cryptography.fernet import Fernet
import base64
import os

#temporary passwords list
passwords=[["!!!Username", "Note", "Password"]]
loggedIn=False

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
    textOutput.delete(1.0,CTk.END)
    
    try:
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKey:
            key = dataKey.read()
            
        #initalize key
        fernet=Fernet(key)
        #open encrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as encryptedFile:
            encryptedData=encryptedFile.read()   
        #decrypt data
        decryptedData=fernet.decrypt(encryptedData) #this line should decrypt data but it freezes program and encryption doesn't work
        #writing unencrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as encryptedFileTwo:
            encryptedFileTwo.write(decryptedData) #should be decryptedData
        #output decrypted passwords to GUI
        with open(os.path.join(working_path,"data.csv"), newline='') as decryptedFile:
            reader=csv.reader(decryptedFile, delimiter=' ', quotechar='|')
            counter=1
            for row in reader:
                rowList=row[0].split(',')   
                if rowList != ["!!!Username", "Note", "Password"]:
                    if rowList not in passwords:
                        passwords.append(rowList)
                    labeledPasswordEntry=str(counter) + ") " + "Username: " + rowList[0] + " | " + "Note: " + rowList[1] + " | " + "Password: " + rowList[2]
                    textOutput.insert(CTk.END, labeledPasswordEntry)
                    textOutput.insert(CTk.END, "\n")
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
            dataKey.close()
        #initalize key
        fernet=Fernet(key)
        #open encrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as encryptedFile:
            encryptedData=encryptedFile.read()
            encryptedFile.close()
        #decrypt data
        decryptedData=fernet.decrypt(encryptedData)
        #writing unencrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as encryptedFileTwo:
            encryptedFileTwo.write(decryptedData)
            encryptedFileTwo.close()
        with open(os.path.join(working_path,"exportedPasswords.csv") , 'wb') as exportedFile:
            exportedFile.write(decryptedData)
            exportedFile.close()
        #encrypt data again
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKeyTwo:
            key = dataKeyTwo.read()
            dataKeyTwo.close()
        #initalize key
        fernet=Fernet(key)
        #open unencrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as unencryptedFile:
            unencryptedData=unencryptedFile.read()
            unencryptedFile.close()
        #encrypted data
        encryptedData=fernet.encrypt(unencryptedData)
        #writing encrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as unencryptedFileTwo:
            unencryptedFileTwo.write(encryptedData)
            unencryptedFileTwo.close()
        #output export
        textOutput.delete(1.0,CTk.END)
        textOutput.insert(CTk.END, "Exported.")
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
        textOutput.delete(1.0, CTk.END)
        textOutput.insert(CTk.END, "Can't start username with '!' or ' '.")
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
        data.close()
    #open key file
    try:
        with open(os.path.join(working_path,"dataKey.key"), 'rb') as dataKey:
            key = dataKey.read()
            dataKey.close()
        #initalize key
        fernet=Fernet(key)
        #open unencrypted file
        with open(os.path.join(working_path,"data.csv"), 'rb') as dataTwo:
            unencryptedData=dataTwo.read()
            dataTwo.close()
        #encrypted data
        encryptedData=fernet.encrypt(unencryptedData)
        #writing encrypted data
        with open(os.path.join(working_path,"data.csv"), 'wb') as dataThree:
            dataThree.write(encryptedData)
            dataThree.close()
    except:
        #creates dataKey file and reruns function
        key=Fernet.generate_key()
        with open(os.path.join(working_path,"dataKey.key"), 'wb') as dataKey:
            dataKey.write(key)
            dataKey.close()
        writeToCSV()
    return

#searches entries that contain search term
def search():   
    textOutput.delete(1.0,CTk.END)
    textOutput.insert(CTk.END, "Search Results: ")
    textOutput.insert(CTk.END, "\n")
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
                        textOutput.insert(CTk.END, labeledPasswordEntry)
                        textOutput.insert(CTk.END, "\n")
                        counter=counter+1
    return

#generates random 15 character password and outputs it
def generateStrongPassword():
    generatePasswordOutput.delete(1.0,CTk.END)
    characters = string.ascii_letters + string.digits + string.punctuation
    generatedPassword = ''.join(random.choice(characters) for i in range(15))
    generatePasswordOutput.insert(CTk.END, generatedPassword)
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
        masterPasswordKey.close()
    if passwordVar.get() != decryptedMasterPassword:
        loginWindowOutput.delete(1.0,CTk.END)
        loginWindowOutput.insert(CTk.END, "Wrong Password")
    if passwordVar.get() == decryptedMasterPassword:
        global loggedIn
        loggedIn=True
        loginWindow.destroy()
    return decryptedMasterPassword

#destroy setup window 
def destroySetupWindow():
    setupWindow.destroy()

#creates help window
def getHelp():
    def destroyHelpWindow():
        helpWindow.destroy()
    helpWindow=CTk.CTk()
    helpWindow.title("Help")
    helpWindow.geometry("310x200")
    helpWindow.resizable(False, False)
    helpWindow.eval('tk::PlaceWindow . center')
    helpWindowLabel=CTk.CTkLabel(master=helpWindow, text="To reset the password, click reset on the\nlogin screen. This will erase all data \n and reset the program.")
    helpWindowLabel.place(x=25,y=40)
    helpWindowReturnButton=CTk.CTkButton(master=helpWindow, text="Return", command=destroyHelpWindow)
    helpWindowReturnButton.place(x=90, y=120)
    helpWindow.mainloop()
    return

#reset password
def reset():
    def destroyResetWindow():
        resetWindow.destroy()
    #overwrites all files to blank
    def deleteAllData():
        destroyResetWindow()
        try:
            with open(os.path.join(working_path,"data.csv"), 'wb') as dataFile:
                dataFile.write(b'')
                dataFile.close()
            with open(os.path.join(working_path,"dataKey.key"), 'wb') as dataKeyFile:
                dataKeyFile.write(b'')
                dataKeyFile.close()
            with open(os.path.join(working_path,"masterPasswordKey.key"), 'wb') as masterPasswordKeyFile:
                masterPasswordKeyFile.write(b'')
                masterPasswordKeyFile.close()
            with open(os.path.join(working_path,"masterPassword.key"), 'wb') as masterPasswordFile:
                masterPasswordFile.write(b'')
                masterPasswordFile.close()
            loginWindow.destroy()
            window.destroy()
        except:
            pass
    resetWindow=CTk.CTk()
    resetWindow.title("Reset")
    resetWindow.geometry("310x200")
    resetWindow.resizable(False, False)
    resetWindow.eval('tk::PlaceWindow . center')
    resetWindowLabel=CTk.CTkLabel(master=resetWindow, text="Are you sure you want to erase all data. \n This will erase all data and reset \n the program.")
    resetWindowLabel.place(x=35,y=40)
    eraseButton=CTk.CTkButton(master=resetWindow, text="Erase", command=deleteAllData)
    eraseButton.place(x=85, y=110)
    returnButton=CTk.CTkButton(master=resetWindow, text="Return", command=destroyResetWindow)
    returnButton.place(x=85, y=150)
    resetWindow.mainloop()

#initial code starts here
#loginScreen
try:
    reader = open(os.path.join(working_path,"masterPassword.key"), 'rb')
    masterPasswordEncrypted=reader.read()
    reader.close()
    with open(os.path.join(working_path,"masterPasswordKey.key"), 'rb') as masterPasswordKey:
        #get key for decryption
        key=masterPasswordKey.read()
        fernet=Fernet(key)
        decryptedMasterPassword=fernet.decrypt(masterPasswordEncrypted).decode()
        masterPasswordKey.close()
    if len(decryptedMasterPassword)>0:
        loginWindow=CTk.CTk()
        loginWindow.title("Login")
        loginWindow.geometry("330x200")
        loginWindow.resizable(False, False)
        loginWindow.eval('tk::PlaceWindow . center')
        passwordVar=CTk.StringVar()
        askPasswordLabel=CTk.CTkLabel(master=loginWindow, text="Enter Password: ")
        askPasswordInput=CTk.CTkEntry(master=loginWindow, width=120, textvariable=passwordVar)
        askPasswordButton=CTk.CTkButton(master=loginWindow, width=50, text="Login", command=checkLogin)
        loginWindowOutput=CTk.CTkTextbox(master=loginWindow, height=2, width=120)
        resetButton=CTk.CTkButton(master=loginWindow, width=50, text="Reset", command=reset)
        askPasswordLabel.place(x=45,y=80)
        askPasswordInput.place(x=150, y=80)
        askPasswordButton.place(x=170, y=120)
        loginWindowOutput.place(x=45,y=120)
        resetButton.place(x=230,y=120)
        loginWindow.mainloop()
    else:
        setupWindow=CTk.CTk()
        setupWindow.title("Setup Master Password")
        setupWindow.geometry("310x200")
        setupWindow.resizable(False, False)
        setupWindow.eval('tk::PlaceWindow . center')
        setupPasswordVar=CTk.StringVar()
        setupPasswordLabel=CTk.CTkLabel(master=setupWindow, text="Create your master password. \n This can not be recovered if forgotten.")
        setupPasswordInput=CTk.CTkEntry(master=setupWindow, width=100, textvariable=setupPasswordVar)
        setupPasswordButton=CTk.CTkButton(master=setupWindow, width=100, text="Enter", command=destroySetupWindow)
        setupPasswordLabel.place(x=35, y=55)
        setupPasswordInput.place(x=105,y=100)
        setupPasswordButton.place(x=105, y=150)
        setupWindow.mainloop()
        with open(os.path.join(working_path,"masterPassword.key"), 'wb') as file:
            #encrypt and write masterpassword to txt file
            unencryptedMasterPassword=setupPasswordVar.get()
            unencryptedMasterPasswordBytes=unencryptedMasterPassword.encode("utf-8")
            key=base64.urlsafe_b64encode(unencryptedMasterPasswordBytes.ljust(32)[:32])
            with open(os.path.join(working_path,"masterPasswordKey.key"), 'wb') as fileTwo:
                fileTwo.write(key)
                fileTwo.close()
            fernet=Fernet(key)
            encryptedMasterPassword=fernet.encrypt(unencryptedMasterPassword.encode())
            file.write(encryptedMasterPassword)       
            file.close()
        if len(setupPasswordVar.get())>0:
            loggedIn=True
 
except:
    setupWindow=CTk.CTk()
    setupWindow.title("Setup Master Password")
    setupWindow.geometry("310x200")
    setupWindow.resizable(False, False)
    setupWindow.eval('tk::PlaceWindow . center')
    setupPasswordVar=CTk.StringVar()
    setupPasswordLabel=CTk.CTkLabel(master=setupWindow, text="Create your master password. \n This can not be recovered if forgotten.")
    setupPasswordInput=CTk.CTkEntry(master=setupWindow, width=100, textvariable=setupPasswordVar)
    setupPasswordButton=CTk.CTkButton(master=setupWindow, width=100, text="Enter", command=destroySetupWindow)
    setupPasswordLabel.place(x=35, y=55)
    setupPasswordInput.place(x=105,y=100)
    setupPasswordButton.place(x=105, y=150)
    setupWindow.mainloop()
    with open(os.path.join(working_path,"masterPassword.key"), 'wb') as file:
        #encrypt and write masterpassword to txt file
        unencryptedMasterPassword=setupPasswordVar.get()
        unencryptedMasterPasswordBytes=unencryptedMasterPassword.encode("utf-8")
        key=base64.urlsafe_b64encode(unencryptedMasterPasswordBytes.ljust(32)[:32])
        with open(os.path.join(working_path,"masterPasswordKey.key"), 'wb') as fileTwo:
            fileTwo.write(key)
            fileTwo.close()
        fernet=Fernet(key)
        encryptedMasterPassword=fernet.encrypt(unencryptedMasterPassword.encode())
        file.write(encryptedMasterPassword)       
        file.close()
    if len(setupPasswordVar.get())>0:
        loggedIn=True
        

#mainGUI
window=CTk.CTk()
textOutput = CTk.CTkTextbox(master=window, height = 440, width = 900)
window.title("Password Manager")
window.geometry("900x600")
window.resizable(False, False)
window.eval('tk::PlaceWindow . center')

#variables
userNameVar=CTk.StringVar()
notesVar=CTk.StringVar()
passwordVar=CTk.StringVar()
searchVar=CTk.StringVar()
deleteVar=CTk.StringVar()

#tkinter widgets
entryLabelUsername=CTk.CTkLabel(master=window, text="Username: ")
entryInputUsername=CTk.CTkEntry(master=window, textvariable=userNameVar)
entryLabelNote=CTk.CTkLabel(master=window, text="Note: ")
entryInputNote=CTk.CTkEntry(master=window, textvariable=notesVar)
entryLabelPassword=CTk.CTkLabel(master=window, text="Password: ")
entryInputPassword=CTk.CTkEntry(master=window, textvariable=passwordVar)
addButton=CTk.CTkButton(master=window, text="Add", command=addToPasswordsList)
searchBoxLabel=CTk.CTkLabel(master=window, text="Search: ")
searchBoxInput=CTk.CTkEntry(master=window, textvariable=searchVar)
searchButton=CTk.CTkButton(master=window, text="Search", command=search)
generatePasswordLabel=CTk.CTkLabel(master=window, text="Generate Strong Password: ")
generatePasswordButton=CTk.CTkButton(master=window, text="Generate", command=generateStrongPassword)
generatePasswordOutput=CTk.CTkTextbox(master=window, height = 1.5, width = 130)
showAllButton=CTk.CTkButton(master=window, text="Return", command=initialization)
deleteItemLabel=CTk.CTkLabel(master=window, text="Enter item number to delete: ")
deleteItemInput=CTk.CTkEntry(master=window, width=5, textvariable=deleteVar)
deleteItemButton=CTk.CTkButton(master=window, text="Delete", command=delete)
helpButton=CTk.CTkButton(master=window, text="Help", command=getHelp)
exportButton=CTk.CTkButton(master=window, text="Export", command=export)

#place tkinter widgets
textOutput.place(x=0,y=0)
entryLabelUsername.place(x=20, y=450)
entryInputUsername.place(x=90, y=450)
entryLabelNote.place(x=250, y=450)
entryInputNote.place(x=290, y=450)
entryLabelPassword.place(x=450, y=450)
entryInputPassword.place(x=520, y=450)
addButton.place(x=730, y=450)
searchBoxLabel.place(x=20, y=500)
searchBoxInput.place(x=75, y=500)
searchButton.place(x=230, y=500)
generatePasswordLabel.place(x=400, y=500)
generatePasswordOutput.place(x=580, y=500)
generatePasswordButton.place(x=730, y=500)
showAllButton.place(x=730, y=550)
deleteItemLabel.place(x=20, y=550)
deleteItemInput.place(x=205, y=550)
deleteItemButton.place(x=265, y=550)
helpButton.place(x=420, y=550)
exportButton.place(x=580, y=550)

#starts main GUI and initializaiton 
initialization()
try:
    reader = open(os.path.join(working_path,"masterPassword.key"), 'rb')
    masterPasswordEncrypted=reader.read()
    reader.close()
    if loggedIn:
        window.mainloop()
except:
    pass