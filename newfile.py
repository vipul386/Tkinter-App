from tkinter import *
from tkinter.simpledialog import *

#Variables
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
    add_log(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult


# Button Function
def insert():
	db_query(f"insert into {tabe_name} values({id_entry.get()}, {name_entry.get()}, {marks_entry.get()} )")


def update():
	db_query(f"update {table_name} set {id_entry.get()}, {name_entry.get()}, {marks_entry.get()} where id = {id_entry}")


def delete():
	db_query(f"delete from {table_name} where id = {id_entry}")


root = Tk()

auth = askstring(title="Authentication", prompt="Password?")
if (auth.get() == password):
	Label(root, text="ID: ").grid(row=1, column=1)
	Label(root, text="Name: ").grid(row=2, column=1)
	Label(root, text="Marks: ").grid(row=3, column=1)

	id_entry = Entry(root)
	id_entry.grid(row=1, column=2)
	name_entry = Entry(root)
	name_entry.grid(row=2, column=2)
	marks_entry = Entry(root)
	marks_entry.grid(row=3, column=2)
	
	Button(root, text="Insert", command=insert).grid(row=4, column=1)
	Button(root, text="Update", command=update).grid(row=4, column=2)
	Button(root, text="Delete", command=delete).grid(row=4, column=3)

root.mainloop()