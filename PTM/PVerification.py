from tkinter import *
from datetime import datetime
weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]

def validate_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def controlNumberCheck(Pesel):
    ControlNumber = 0
    i = 0
    while i < 10:
        ControlNumber += int(Pesel[i]) * int(weights[i])
        i += 1
    return -(ControlNumber % 10 - 10)

def verification(pesel):
    date = "19" + pesel[0:2] + "-" + pesel[2:4] + "-" + pesel[4:6]
    if len(pesel) != 11:
        response.place(x=70, y=115)
        response.config(text="There Should Be 11 Symbols!")
    elif not validate_date(date):
        response.place(x=100, y=115)
        response.config(text="Date Is Not Correct!")
    else:
        if int(pesel[-1]) == int(controlNumberCheck(pesel)):
            response.place(x=101, y=115)
            response.config(text="It Is Correct Pesel!")
        else:
            response.place(x=92, y=115)
            response.config(text="It Is Not Correct Pesel!")



def CheckbuttonClicked():
    verification(Entry.get(entryForPesel))


root = Tk()
root.geometry("300x200")
root.resizable(False, False)

text1 = Label(text="Enter Your Pesel:")
entryForPesel = Entry()
verificationbtn = Button(text="Check Authenticity", command=CheckbuttonClicked)
response = Label(text="")

text1.place(x=105, y=35)
entryForPesel.place(x=90, y=60)
verificationbtn.place(x=97, y=85)


root.mainloop()