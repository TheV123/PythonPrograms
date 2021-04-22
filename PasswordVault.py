import sqlite3, hashlib
from sqlite3.dbapi2 import Cursor
from tkinter import *
from typing import Match
from tkinter import simpledialog
from functools import partial

#Database Code
with sqlite3.connect("password_vault.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

#create Popup
def popUp(text):
    answer = simpledialog.askstring("Input String", text)
    return answer


#Initiate Window
window = Tk()
window.title("Password Vault")

def hashPassword(input):
    hash = hashlib.sha3_256(input) #hashes password using sha3_256
    hash = hash.hexdigest()

    return hash
#First time using the app-  First Screen
def firstScreen():
    window.geometry("250x150")

    label = Label(window, text= "Create Master Password")
    label.config(anchor= CENTER)
    label.pack()

    text = Entry(window, width= 20, show= "*")
    text.pack()
    text.focus()

    label1 = Label(window, text= "Re-enter Master Password")
    label1.pack()

    text1 = Entry(window, width = 20, show= "*")
    text1.pack()
    text1.focus()

    label2 = Label(window)
    label2.pack()
    #Saves the password
    def savePassword():
        if text.get() == text1.get():
            hashedPassword = hashPassword(text.get().encode('utf-8')) 
            #adds password into database when the user presses submit
            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashedPassword)])
            db.commit()

            passwordVault()
        else:
            label2.config(text = "Passwords do not Match")

    button = Button(window, text= "Save", command= savePassword)
    button.pack(pady= 5)
#Normal Login Screen
def loginScreen():
    window.geometry("250x100")
    
    label = Label(window, text= "Enter Master Password")
    label.config(anchor= CENTER)
    label.pack()

    text = Entry(window, width= 20, show= "*")
    text.pack()
    text.focus()

    label1 = Label(window)
    label1.pack()

    def getMasterPassword():
        checkHashedPassword = hashPassword(text.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    #Checks if passwords match
    def checkPassword():
        match = getMasterPassword()
        
        print(match)
        if match:
            passwordVault()
        else:
            text.delete(0, "end")
            label1.config(text= "Wrong Password")

    button = Button(window, text= "Submit", command= checkPassword)
    button.pack(pady= 5)
#Password Vault
def passwordVault():
    #clears the previous window
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        #text that is given to popUp func
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"
        #set text to variables
        website = popUp(text1)
        username = popUp(text2)
        password = popUp(text3)
        #insert text into database
        insert_fields = """INSERT INTO vault(website,username,password)
        VALUES(?,?,?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordVault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE ID = ?", (input,))
        db.commit()
        passwordVault()

    window.geometry("800x350")

    label2 = Label(window, text= "Password Vault")
    label2.grid(column= 1)

    btn = Button(window, text ="+", command= addEntry)
    btn.grid(column= 1, pady= 10)

    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx= 88)
    lbl = Label(window, text="Username")
    lbl.grid(row=2, column=1, padx= 88)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx= 88)

    cursor.execute("SELECT * FROM vault")
    #displays text using database using a loop 
    if (cursor.fetchall()!=  None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()
            #creates an array with all the entries and checks them
            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=i+3)
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl1.grid(column=1, row=i+3)
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl1.grid(column=2, row=i+3)
            #takes array with current array and id and deletes it
            btn = Button(window, text="Delete", command= partial(removeEntry, array[i][0]))
            btn.grid(column= 3, row= i+3, pady=10)
            
            i = i+ 1

            cursor.execute("SELECT * FROM vault")
            if(len(cursor.fetchall()) <= i):
                break

#Declaring functions
cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    firstScreen()
window.mainloop()