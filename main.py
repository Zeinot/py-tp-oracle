import oracledb
import tkinter as tk
from tkinter import simpledialog, Toplevel
from tkcalendar import Calendar

user = "directeur"
pwd = "admin"
connection = oracledb.connect(
    user=user,
    password=pwd,
    host="localhost",
    port=1521,
    service_name="scolarite")
cursor = connection.cursor()

def SelectStudents():
    cursor.execute("SELECT IdEt, NomEt, PrenomEt, TO_CHAR(DateNais, 'DD-MON-YYYY') FROM Etudiant")
    rows = cursor.fetchall()
    return rows

def refresh_student_listbox():
    students = SelectStudents()
    student_listbox.delete(0, tk.END)  # Clear the listbox
    for student in students:
        student_listbox.insert(tk.END, f"{student[0]} | {student[1]} {student[2]} | {student[3]}")

def delete_student():
    selected_student = student_listbox.get(tk.ACTIVE)
    if selected_student:
        student_id = selected_student.split(" | ")[0]
        cursor.execute(f"DELETE FROM Etudiant WHERE IdEt = :id", {"id": student_id})
        connection.commit()
        refresh_student_listbox()

def open_edit_popup():
    selected_student = student_listbox.get(tk.ACTIVE)
    if selected_student:
        parts = selected_student.split(" | ")
        student_id = parts[0]
        name_parts = parts[1].split()
        nom = name_parts[0]
        prenom = name_parts[1] if len(name_parts) > 1 else ""
        birthday = parts[2] if len(parts) > 2 else ""

        edit_popup = Toplevel(root)
        edit_popup.title("Edit Student")

        tk.Label(edit_popup, text="Enter new Nom:").grid(row=0, column=0)
        new_nom_entry = tk.Entry(edit_popup)
        new_nom_entry.grid(row=0, column=1)
        new_nom_entry.insert(0, nom)

        tk.Label(edit_popup, text="Enter new Prenom:").grid(row=1, column=0)
        new_prenom_entry = tk.Entry(edit_popup)
        new_prenom_entry.grid(row=1, column=1)
        new_prenom_entry.insert(0, prenom)

        tk.Label(edit_popup, text="Select new Birthday:").grid(row=2, column=0, columnspan=2)
        cal = Calendar(edit_popup, selectmode='day', date_pattern='dd-mm-yyyy')
        cal.grid(row=3, column=0, columnspan=2)

        def update_student():
            new_nom = new_nom_entry.get()
            new_prenom = new_prenom_entry.get()
            new_birthday = cal.get_date()
            
            if new_nom and new_prenom and new_birthday:
                cursor.execute(f"""
                    UPDATE Etudiant SET NomEt = :nom, PrenomEt = :prenom, DateNais = TO_DATE(:birthday, 'DD-MM-YYYY')
                    WHERE IdEt = :id
                """, {"nom": new_nom, "prenom": new_prenom, "birthday": new_birthday, "id": student_id})
                connection.commit()
                refresh_student_listbox()
                edit_popup.destroy()

        tk.Button(edit_popup, text="Update", command=update_student).grid(row=4, column=0, columnspan=2)

# UI
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
date.grid(row=2, column=0, columnspan=2)
# Add Calendar using grid
cal = Calendar(root, selectmode='day')
cal.grid(row=0, column=0, columnspan=2)

def grad_date():
    date.config(text="Selected Date is: " + cal.get_date())

# Add Button and Label using grid
tk.Button(root, text="Select Birthday", command=grad_date).grid(row=1, column=0, columnspan=2)

def add_student():
    nom = e1.get()
    prenom = e2.get()
    birthday = cal.get_date()  # Date format from the calendar is 'MM/DD/YYYY'
    # Convert the date format from 'MM/DD/YYYY' to 'DD-MON-YYYY'
    month, day, year = birthday.split('/')
    birthday_formatted = f"{day}-{month_names[int(month)]}-{year}"
    cursor.execute(f"""
        INSERT INTO Etudiant (NomEt, PrenomEt, DateNais)
        VALUES ('{nom}', '{prenom}', TO_DATE('{birthday_formatted}', 'DD-MON-YYYY'))
    """)
    connection.commit()
    print(f"New user Nom: {nom}, Prenom: {prenom}, Birthday: {birthday_formatted}")
    # Clear input fields
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    # Refresh the student listbox
    refresh_student_listbox()

# Map month numbers to abbreviations
month_names = ["", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# Listbox to display students
student_listbox = tk.Listbox(root)
student_listbox.grid(row=7, column=0, columnspan=2, sticky=tk.W+tk.E)

# Buttons
tk.Button(root, text='Add', width=25, command=add_student).grid(row=6, column=0, columnspan=2)
tk.Button(root, text='Delete', width=25, command=delete_student).grid(row=8, column=0, columnspan=2)
tk.Button(root, text='Edit', width=25, command=open_edit_popup).grid(row=9, column=0, columnspan=2)

# Initial refresh of the student listbox
refresh_student_listbox()

root.mainloop()

# Close connections
cursor.close()
connection.close()
