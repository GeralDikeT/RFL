from tkinter import *
from tkinter import messagebox
import mysql.connector

adminPassword = 881

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bankomat"
    )

cursor = mydb.cursor()

def registration(lg, ps, is_admin):
    if is_admin:
        cursor.execute("SELECT COUNT(*) FROM fadmin WHERE login = %s;", (lg,))
        result = cursor.fetchone()[0]
        if result:
            messagebox.showerror("", "This login Already In Use!")
            login.delete(0, "end")
        else:
            cursor.execute("INSERT INTO fadmin(login, password) VALUES(%s, %s)", (lg, ps))
            mydb.commit()
            messagebox.showinfo("", "You Are Registered, Welcome To Our Company!")
            print(lg, ps, "Registered as Admin")
    else:
        cursor.execute("SELECT COUNT(*) FROM fuser WHERE login = %s;", (lg,))
        result = cursor.fetchone()[0]
        if result:
            messagebox.showerror("", "This login Already In Use!")
            login.delete(0, "end")
        else:
            cursor.execute("INSERT INTO fuser(login, password, Money) VALUES(%s, %s, %s)", (lg, ps, 5000))
            mydb.commit()
            select_query = "SELECT Clients FROM bank LIMIT 1"
            cursor.execute(select_query)
            current_num_clients = cursor.fetchone()[0]
            cursor.execute("UPDATE bank SET Clients = %s", (current_num_clients + 1 ,))
            mydb.commit()
            messagebox.showinfo("", "You Are Registered, Welcome!")
            print(lg, ps, "Registered as User")

def dataCheck():
    loginT = login.get()
    passwordT = password.get()
    passwordX2T = passwordX2.get()
    secretCodeT = secretCode.get()
    user_type = user_type_var.get()

    if loginT == "" or passwordT == "" or passwordX2T == "":
        messagebox.showerror("Error", "You Have Empty Fields!")
    else:
        if len(loginT) < 4:
            messagebox.showerror("Error", "Login Must Be Longer!")
        elif len(passwordT) < 8:
            messagebox.showerror("Error", "Password Must Be Longer!")
        elif passwordT != passwordX2T:
            messagebox.showerror("Error", "Passwords Do Not Match!")
        else:
            if user_type == "Admin":
                if secretCodeT != "" and int(secretCodeT) == adminPassword:
                    registration(loginT, passwordT, True)
                elif secretCodeT == "" or int(secretCodeT) != adminPassword:
                    messagebox.showerror("Error", "Secret Code Incorrect!")
            else: 
                registration(loginT, passwordT, False)

root = Tk()
root.geometry("425x250")
root.resizable(False, False)

loginlbl = Label(text="Login:")
login = Entry()
passwordlbl = Label(text="Password:")
password = Entry(show="*")
passwordX2lbl = Label(text="Confirm Password:")
passwordX2 = Entry(show="*")

lblForAdmin = Label(text="Secret Code:")
secretCode = Entry()

regQuestion = Label(text="Register As Admin Or User?")
register = Button(text="Register", width=20, command=dataCheck)

user_type_var = StringVar(value="User") 

rbtn = Radiobutton(text="Admin", variable=user_type_var, value="Admin", command=lambda: (lblForAdmin.place(x=20, y=185), secretCode.place(x=20, y=205)))
rbtn1 = Radiobutton(text="User", variable=user_type_var, value="User", command=lambda: (lblForAdmin.place_forget(), secretCode.place_forget(), secretCode.delete(0, "end")))

loginlbl.place(x=20, y=20)
login.place(x=20, y=40)
passwordlbl.place(x=20, y=75)
password.place(x=20, y=95)
passwordX2lbl.place(x=20, y=130)
passwordX2.place(x=20, y=150)
regQuestion.place(x=210, y=90)
register.place(x=210, y=144)
rbtn.place(x=206, y=115)
rbtn1.place(x=312, y=115)

root.mainloop()
