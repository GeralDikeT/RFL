from tkinter import *
from tkcalendar import Calendar
from datetime import datetime
import random

root = Tk()
root.geometry("600x260")

weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]


def controlNumberCheck(Pesel):
    ControlNumber = 0
    i = 0
    while i < 10:
        ControlNumber += int(Pesel[i]) * int(weights[i])
        i += 1
    return -(ControlNumber % 10 - 10)

def generatePesel():
    pesel = 0
    gender = ""
    date_str = cal.get_date()
    date_obj = datetime.strptime(date_str, "%m/%d/%y")
    formatted_date = date_obj.strftime("%m-%d-%y")

    pesel = formatted_date[6:8] + formatted_date[0:2] + formatted_date[3:5] + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(1, 9))
    pesel = pesel + str(controlNumberCheck(pesel))

    if int(pesel[9]) % 2 == 0:
        genderlbl.place(x=380, y=160)
        genderlbl.config(text="Your Gender: Women")
    else:
        genderlbl.place(x=390, y=160)
        genderlbl.config(text="Your Gender: Man")

    generatedPesel.config(text="Your Pesel Is: " + pesel)

cal = Calendar(root, selectmode='day',
               year=2020, month=5,
               day=22)
text1 = Label(root, text="Choose Your Birthday: ")
btn = Button(root, text="Generate Pesel", width=20, command=generatePesel)
generatedPesel = Label(text="")
genderlbl = Label(text="")

cal.place(x=30, y=30)
text1.place(x=90, y=5)
btn.place(x=365, y=60)
generatedPesel.place(x=370, y=125)


root.mainloop()
