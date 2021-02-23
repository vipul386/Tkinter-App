from tkinter import Tk, Label, Entry, Button, Frame
from tkinter.simpledialog import askstring
import mysql.connector

# Variables
password = "mk303"
table_name = "students"

# Mysql Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="manish"
)
mycursor = mydb.cursor()


def db_query(query):
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    mydb.commit()
    return myresult


# Functions
def setTextInput(text, entry):
    entry.delete(0, "end")
    entry.insert(0, text)


# Button Function
def select():
    data = db_query(f"select * from {table_name} where id= {id_entry.get()};")
    setTextInput(data[0][0], id_entry)
    setTextInput(data[0][1], name_entry)
    setTextInput(data[0][2], marks_entry)


def insert():
    db_query(
        f"insert into {table_name} "
        "values "
        f"({id_entry.get()}, '{name_entry.get()}', {marks_entry.get()});")


def update():
    db_query(
        f"update {table_name} set "
        f"id= {id_entry.get()}, "
        f"name= '{name_entry.get()}', marks= {marks_entry.get()} "
        f"where id = {id_entry.get()};")


def delete():
    db_query(f"delete from {table_name} where id= {id_entry.get()}")


root = Tk()
root.title("Manish ka App h")
root.geometry("300x150")
root.minsize(300, 150)
root.withdraw()
layout1 = Frame(root)
layout1.pack(pady=20)
layout2 = Frame(root)
layout2.pack(pady=(0, 8))

auth = askstring(title="Authentication", prompt="Password?" + 80 * " ")
if (auth == password):
    root.deiconify()
    Label(layout1, text="ID: ").grid(row=1, column=1, padx=8)
    Label(layout1, text="Name: ").grid(row=2, column=1, padx=8)
    Label(layout1, text="Marks: ").grid(row=3, column=1, padx=8)

    id_entry = Entry(layout1)
    id_entry.grid(row=1, column=2, padx=8)
    name_entry = Entry(layout1)
    name_entry.grid(row=2, column=2, padx=8)
    marks_entry = Entry(layout1)
    marks_entry.grid(row=3, column=2, padx=8)

    Button(layout2, text="Select", command=select).pack(side="left", padx=2)
    Button(layout2, text="Insert", command=insert).pack(side="left", padx=2)
    Button(layout2, text="Update", command=update).pack(side="left", padx=2)
    Button(layout2, text="Delete", command=delete).pack(side="left", padx=2)

else:
    root.destroy()

root.mainloop()
