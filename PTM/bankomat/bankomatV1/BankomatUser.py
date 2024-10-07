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

def openUserWindow(login):
    root = Tk()
    root.geometry("400x400") 
    root.resizable(False, False)
    root.title("ATM Withdrawal")

    cursor.execute("SELECT Money FROM fuser WHERE login = %s", (login,))
    result = cursor.fetchone()
    if result:
        user_balance = result[0]
    else:
        messagebox.showerror("Error", "User not found.")
        root.quit()
        return

    cursor.execute("SELECT MoneyInBankomat FROM bank LIMIT 1")
    atm_balance = cursor.fetchone()[0]

    total_withdrawn = 0
    all_withdrawn_notes = {}

    def update_balance(withdraw_amount):
        nonlocal user_balance, atm_balance, total_withdrawn
        if withdraw_amount <= 0:
            return
        
        if withdraw_amount > user_balance:
            messagebox.showerror("Error", "Insufficient funds in your account.")
            return
        
        if withdraw_amount % 10 != 0:
            messagebox.showerror("Error", "Amount must be a multiple of 10.")
            return
        
        if withdraw_amount > atm_balance:
            messagebox.showerror("Error", "Insufficient funds in the ATM.")
            return

        user_balance -= withdraw_amount
        cursor.execute("UPDATE fuser SET Money = %s WHERE login = %s", (user_balance, login))
        mydb.commit()

        atm_balance -= withdraw_amount
        cursor.execute("UPDATE bank SET MoneyInBankomat = %s", (atm_balance,))
        mydb.commit()

        total_withdrawn += withdraw_amount

        banknotes = [500, 200, 100, 50, 20, 10]
        banknote_distribution = {}
        remaining_amount = withdraw_amount

        for note in banknotes:
            if remaining_amount <= 0:
                break
            count = remaining_amount // note
            if count > 0:
                banknote_distribution[note] = count
                remaining_amount -= note * count

        current_banknote_message = "\n".join([f"{count} x {note}" for note, count in banknote_distribution.items()])

        for note, count in banknote_distribution.items():
            if note in all_withdrawn_notes:
                all_withdrawn_notes[note] += count
            else:
                all_withdrawn_notes[note] = count

        all_banknotes_message = "\n".join([f"{count} x {note}" for count, note in all_withdrawn_notes.items()])

        messagebox.showinfo("Withdrawn Banknotes", 
                            f"You have withdrawn:\n{current_banknote_message}\n\nAll Withdrawn:\n{all_banknotes_message}")

        logLbl.config(text=f"User: {login}\nBalance: {user_balance}")
        totalLbl.config(text=f"Total Withdrawn: {total_withdrawn}")

    def custom_withdraw():
        try:
            withdraw_amount = int(amount_entry.get())
            update_balance(withdraw_amount)
            amount_entry.delete(0, END) 
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    logLbl = Label(root, text=f"User: {login}\nBalance: {user_balance}", anchor=NE)
    logLbl.place(x=10, y=10)

    Label(root, text="Enter amount to withdraw:", font=("Arial", 12)).place(x=10, y=40)

    amount_entry = Entry(root)
    amount_entry.place(x=10, y=70, width=180)

    btn_withdraw = Button(root, text="Withdraw Amount", command=custom_withdraw)
    btn_withdraw.place(x=200, y=70)

    Label(root, text="Or select a quick amount:", font=("Arial", 12)).place(x=10, y=110)

    btn10 = Button(root, text="10zl", command=lambda: update_balance(10))
    btn20 = Button(root, text="20zl", command=lambda: update_balance(20))
    btn50 = Button(root, text="50zl", command=lambda: update_balance(50))
    btn100 = Button(root, text="100zl", command=lambda: update_balance(100))
    btn200 = Button(root, text="200zl", command=lambda: update_balance(200))
    btn500 = Button(root, text="500zl", command=lambda: update_balance(500))

    btn10.place(x=10, y=150)
    btn20.place(x=130, y=150)
    btn50.place(x=250, y=150)
    btn100.place(x=10, y=200)
    btn200.place(x=130, y=200)
    btn500.place(x=250, y=200)

    totalLbl = Label(root, text=f"Total Withdrawn: {total_withdrawn}")
    totalLbl.place(x=10, y=320)

    root.mainloop()

