##########
# Imports
##########
from tkinter import Tk, Label, Entry, Button, mainloop, PhotoImage, Frame,\
    NORMAL, DISABLED, RIGHT, LEFT, TOP, BOTTOM, END, X, Y, BOTH, MULTIPLE,\
    Listbox, messagebox, Text, Scrollbar
from tkinter.simpledialog import askstring
import mysql.connector

# Variables
db_list = []


#########
# Functions
#########
def handle_resize(event):
    if (root.winfo_height() != 1 and root.winfo_height() < 500):
        close_greet_window()


def delete_last_log():
    log_box.config(state=NORMAL)
    log_box.delete("end-2l", END)
    log_box.insert(END, "\n")
    log_box.config(state=DISABLED)


def add_log(query):
    log_box.config(state=NORMAL)
    log_box.insert(END, f"{query}\n")
    log_box.config(state=DISABLED)


##########
# Mysql
##########
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)
mycursor = mydb.cursor()


def db_query(query):
    add_log(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult


##########
# Button Functions
##########
def create_db():
    name = askstring(title='Add Database', prompt='Database name?')
    if name is not None:
        if(name.strip() == ""):
            messagebox.showerror("Error", "Database Name is required!")
        elif(" " in name):
            messagebox.showerror("Error",
                                 "Spaces not Allowed in Database Name!")
        else:
            try:
                db_query(f"CREATE DATABASE {name};")
                database_list.insert(END, name)
                global db_list
                db_list += [name]
                return name
            except:
                delete_last_log()
                messagebox.showerror("Error",
                                     ("Failed to create database! Make sure"
                                      " your database don't contain any"
                                      " invalid characters."))


def delete_db():
    selection = database_list.curselection()

    try:
        selection = int(selection[0])

        global db_list
        db_query(f"DROP DATABASE {db_list[selection]};")
        db_list.pop(selection)
        database_list.delete(selection)
    except:
        delete_last_log()
        messagebox.showerror("Error",
                             "Failed to delete!")


def select_db():
    selection = database_list.curselection()

    selection = int(selection[0])

    global db_list
    add_log(f"USE DATABASE {db_list[selection]};")
    mydb.database = db_list[selection]


def edit_db():
    messagebox.showerror(title="YES", message="😀😁😏😬🥺")


def close_greet_window():
    user_panel.pack_forget()


##########
# Tkinter GUI
##########
root = Tk()
root.title("Database Manager")
# root.resizable(False, False)
root.geometry("1280x720")
root.minsize(800, 400)
root.bind("<Configure>", handle_resize)


################################ User Section ################################
user_section = Frame(root, borderwidth=2, relief="ridge")
user_section.pack(side=LEFT)

################################# User Panel #################################
user_panel = Frame(user_section)
user_panel.pack(side=TOP)

close_btn = Button(user_panel,
                   borderwidth=0,
                   text="X",
                   command=close_greet_window)
close_btn.pack(side=TOP, padx=(250, 0))

user_icon_img = PhotoImage(file="UI/User Icon.png")
user_icon = Label(user_panel,
                  image=user_icon_img)
user_icon.pack()

welcome_label = Label(user_panel,
                      highlightthickness=0,
                      borderwidth=0,
                      pady=0,
                      text="Welcome",
                      font=("Arial", 12))
welcome_label.pack()

username_label = Label(user_panel,
                       highlightthickness=0,
                       borderwidth=0,
                       pady=0,
                       text="Vipul",
                       font=("Arial", 20))
username_label.pack()

################################ Log Section #################################
log_section = Frame(user_section)
log_section.pack(side=BOTTOM)

log_title_bar = Frame(log_section)
log_title_bar.pack(side=TOP, fill=X)

log_label = Label(log_title_bar,
                  text="Logs:",
                  font=("Arial", 12))
log_label.pack(side=LEFT)

log_box = Text(log_section,
               width=35,
               height=50,
               bd=0,
               bg="#C4C4C4")
log_box.pack(side=TOP)
log_box.config(state=DISABLED)

############################## Database Section ##############################
database_section = Frame(root,
                         bg="white")
database_section.pack(side=LEFT, fill=BOTH, expand=True)

################################# Title Bar ##################################
title_bar = Frame(database_section)
title_bar.pack(side=TOP, fill=X)

title_label = Label(title_bar,
                    text="Choose Database:",
                    font=("Arial", 28))
title_label.pack(side=LEFT)

add_btn_img = PhotoImage(file="UI/Create Button.png")
add_btn = Button(title_bar,
                 image=add_btn_img,
                 borderwidth=0,
                 command=create_db)
add_btn.pack(side=RIGHT, padx=25)

############################### Database Panel ###############################
database_panel = Frame(database_section)
database_panel.pack(side=TOP, fill=BOTH, expand=True)

database_scroll = Scrollbar(database_panel)
database_scroll.pack(side=RIGHT, fill=Y)

database_list = Listbox(database_panel,
                        yscrollcommand=database_scroll.set,
                        bd=0,
                        font=('Arial', 14),
                        highlightcolor="white",
                        bg="white")

for db_name in db_query("SHOW DATABASES;"):
    db_list += db_name
    database_list.insert(END, db_name)

database_list.pack(side=LEFT, fill=BOTH, expand=True)
database_scroll.config(command=database_list.yview)

################################# Action Bar #################################
action_bar = Frame(database_section)
action_bar.pack(side=BOTTOM, fill=X)

delete_icon_img = PhotoImage(file="UI/Delete Button.png")
delete_btn = Button(action_bar,
                    image=delete_icon_img,
                    font=('Arial', 16),
                    borderwidth=0,
                    command=delete_db)
delete_btn.pack(side=RIGHT, padx=(0, 25))

edit_icon_img = PhotoImage(file="UI/Edit Button.png")
edit_btn = Button(action_bar,
                  image=edit_icon_img,
                  font=('Arial', 16),
                  borderwidth=0,
                  command=edit_db)
edit_btn.pack(side=RIGHT, padx=10)

select_icon_img = PhotoImage(file="UI/Select Button.png")
select_btn = Button(action_bar,
                    image=select_icon_img,
                    font=('Arial', 16),
                    borderwidth=0,
                    command=select_db)
select_btn.pack(side=RIGHT)

mainloop()
