from tkinter import *
from time import *

def update():
    time_string = strftime("%I:%M:%S %p")        ## strftime = used to format time in simple terms
    time_label.config(text=time_string)

    day_string = strftime("%A")
    day_label.config(text=day_string)

    date_string = strftime("%B %a, %Y")
    date_label.config(text=date_string)

    window.after(1000,update)

window = Tk()
window.title("Clock by Samuel Mwangi")

time_label= Label(window, font=("arial",50),fg="green",bg="black")
time_label.pack()

day_label= Label(window, font=("calibri",20),fg="green")
day_label.pack()

date_label= Label(window, font=("cambira",15),fg="green")
date_label.pack()

name_label= Label(window, text="made by github.com/scriptedsyntax",font=("arial",10),fg="black")
name_label.pack()

update()
window.mainloop()

