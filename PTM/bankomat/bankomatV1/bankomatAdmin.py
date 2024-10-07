from tkinter import *
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bankomat"
)

cursor = mydb.cursor()

def openAtmWindow(login):
    root = Tk()
    root.geometry("400x350")
    root.resizable(False, False)
    root.title("ATM Management")

    cursor.execute("SELECT Money FROM bank LIMIT 1")
    bankMoney = cursor.fetchone()[0]

    cursor.execute("SELECT MoneyInBankomat FROM bank LIMIT 1")
    MoneyInBankomat = cursor.fetchone()[0]

    def updateData():
        nonlocal bankMoney, MoneyInBankomat
        try:
            addMoney = int(entMoney.get())

            if addMoney > bankMoney:
                messagebox.showerror("Error", "Not enough money in bank!")
                return

            cursor.execute("UPDATE bank SET Money = Money - %s", (addMoney,))
            cursor.execute("UPDATE bank SET MoneyInBankomat = MoneyInBankomat + %s", (addMoney,))
            mydb.commit()

            cursor.execute("SELECT Money FROM bank LIMIT 1")
            bankMoney = cursor.fetchone()[0]

            cursor.execute("SELECT MoneyInBankomat FROM bank LIMIT 1")
            MoneyInBankomat = cursor.fetchone()[0]

            bankMoneyLbl.config(text="Money In Bank:\n" + str(bankMoney))
            bankomatMoneyLbl.config(text="Money In Bankomat:\n" + str(MoneyInBankomat))

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")

    def topUpUser():
        nonlocal bankMoney 
        try:
            username = entUsername.get()
            topUpAmount = int(entTopUpAmount.get()) 

            cursor.execute("SELECT Money FROM fuser WHERE login = %s", (username,))
            result = cursor.fetchone()

            if result:
                user_balance = result[0]

                if topUpAmount > bankMoney:
                    messagebox.showerror("Error", "Not enough money in the bank for this operation!")
                    return

                new_balance = user_balance + topUpAmount
                cursor.execute("UPDATE fuser SET Money = %s WHERE login = %s", (new_balance, username))
                
                bankMoney -= topUpAmount
                cursor.execute("UPDATE bank SET Money = %s", (bankMoney,))
                mydb.commit()

                messagebox.showinfo("Success", f"User {username}'s balance updated successfully!")
            else:
                messagebox.showerror("Error", "User not found!")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")

    mainlbl = Label(root, text="Add Amount to ATM", font=("Arial", 14))
    bankomatMoneyLbl = Label(root, text="Money In Bankomat:\n" + str(MoneyInBankomat))
    bankMoneyLbl = Label(root, text="Money In Bank:\n" + str(bankMoney))
    entMoney = Entry(root)
    btnSubmit = Button(root, text="Top Up ATM", command=updateData)

    if login == "SuperAdmin":
        lblUser = Label(root, text="Top Up User Balance", font=("Arial", 14))
        lblUsername = Label(root, text="Username:")
        entUsername = Entry(root)
        lblTopUpAmount = Label(root, text="Amount to Add:")
        entTopUpAmount = Entry(root)
        btnTopUpUser = Button(root, text="Top Up User", command=topUpUser)

        mainlbl.place(x=100, y=0)
        bankMoneyLbl.place(x=50, y=80)
        bankomatMoneyLbl.place(x=225, y=80)
        entMoney.place(x=125, y=125)
        btnSubmit.place(x=149, y=160)

        lblUser.place(x=100, y=200)
        lblUsername.place(x=50, y=230)
        entUsername.place(x=125, y=230)
        lblTopUpAmount.place(x=50, y=260)
        entTopUpAmount.place(x=150, y=260)
        btnTopUpUser.place(x=150, y=290)
    else:
        mainlbl.place(x=100, y=0)
        bankMoneyLbl.place(x=50, y=80)
        bankomatMoneyLbl.place(x=225, y=80)
        entMoney.place(x=125, y=125)
        btnSubmit.place(x=149, y=160)

        noAccessLbl = Label(root, text="You do not have permission to top up user balances.", fg="red")
        root.geometry("400x280")
        noAccessLbl.place(x=50, y=220)

    loginlbl = Label(root, text=f"Logged in as:\n {login}")
    loginlbl.pack(anchor=NE)

    root.mainloop()
