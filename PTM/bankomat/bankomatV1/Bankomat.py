from tkinter import *
from tkinter import messagebox
import mysql.connector
import bankomatAdmin
import BankomatUser
import subprocess

globalAdminLogin = None

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "bankomat"
)

print(mydb)

cursor = mydb.cursor()


def LoginCheck():
    login = loginField.get()
    password = passwordField.get()

    cursor.execute("SELECT login, password FROM fadmin WHERE login = %s", (login,))
    result = cursor.fetchone()

    if result:
        dblogin, dbpassword = result
        if login == dblogin and password == dbpassword:
            globalAdminLogin = login
            root.destroy()
            bankomatAdmin.openAtmWindow(globalAdminLogin)
        else:
            passwordField.delete(0, END)
            loginField.delete(0, END)
            messagebox.showerror("Logging Error", "Uncorrect Login or Password!")
    else: 
        cursor.execute("SELECT login, password FROM fuser WHERE login = %s", (login,))
        result = cursor.fetchone()
        if result:
            dblogin, dbpassword = result
            if login == dblogin and password == dbpassword:
                root.destroy()
                BankomatUser.openUserWindow(login)
        else:
            passwordField.delete(0, END)
            loginField.delete(0, END)
            messagebox.showerror("Logging Error", "Uncorrect Login or Password!")

def Register():
    path = r'D:\my\dess\desc_12.09.2024\Pan_Tomasz_Moch\bankomat\bankomatV1\RegiserWindow.py'
    subprocess.Popen(['python', path])
    root.destroy()

root = Tk()
root.geometry("230x150")
root.resizable(False, False)

textL = Label(text="Login")
loginField = Entry()
textP = Label(text="Password")
passwordField = Entry(show="*")
login = Button(text="Login", command=LoginCheck)
register = Button(text="Register", command=Register)

textL.place(x=95, y=0)
textP.place(x=85, y=40)
loginField.place(x=50, y=20)
passwordField.place(x=50, y=60)
login.place(x=92, y=90)
register.place(x=85, y=120)


root.mainloop()