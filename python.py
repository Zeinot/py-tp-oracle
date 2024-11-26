import tkinter as tk
from tkcalendar import Calendar

root = tk.Tk()


# Title label
tk.Label(root, text='Add Student').grid(row=3, column=0, columnspan=2)

# Input fields
tk.Label(root, text='Nom').grid(row=4, column=0)
tk.Label(root, text='Prenom').grid(row=5, column=0)
e1 = tk.Entry(root)
e2 = tk.Entry(root)
e1.grid(row=4, column=1)
e2.grid(row=5, column=1)


date = tk.Label(root, text="")
date.grid(row=2, column=0, columnspan=2, )
# Add Calendar using grid
cal = Calendar(root, selectmode='day')
cal.grid(row=0, column=0, columnspan=2)

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())

# Add Button and Label using grid
tk.Button(root, text="Select Birthday", command=grad_date).grid(row=1, column=0, columnspan=2)

# Button
button = tk.Button(root, text='Add', width=25)
button.grid(row=6, column=0, columnspan=2)

root.mainloop()
