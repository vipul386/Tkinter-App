##########
# Imports
##########
from tkinter import Tk, Label, Entry, Button, mainloop, PhotoImage, Frame,\
    NORMAL, DISABLED, RIGHT, LEFT, TOP, BOTTOM, END, X, Y, BOTH, MULTIPLE,\
    Listbox, messagebox, Text, Scrollbar, Toplevel, Spinbox
from tkinter.simpledialog import askstring, askinteger
import mysql.connector
from utilities import ScrollableFrame

# Variables
db_list = []
tables_list = []
font_family = "Open Sans"


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
    try:
        myresult = mycursor.fetchall()
    except:
        return
    return myresult


def show_db():
    data_list.delete(0, END)
    for db_name in db_query("SHOW DATABASES;"):
        data_list.insert(END, db_name)
        global db_list
        db_list += db_name


def show_tables():
    data_list.delete(0, END)
    for table_name in db_query("SHOW TABLES;"):
        data_list.insert(END, table_name)
        global tables_list
        tables_list += table_name


def create_column(column_len):
    data = {}
    window = Toplevel()
    window.title("Create Table")
    table_section = Frame(window)
    table_section.pack()
    Label(table_section, text="Enter Table name:").pack(side=LEFT)
    table_name = Entry(table_section)
    table_name.pack(side=LEFT)
    column_section = Frame(window)
    column_section.pack()

    for column_index in range(0, column_len):
        row = column_index + 1
        Label(column_section, text=row).grid(row=row, column=0)
        Label(column_section, text="Column Name:").grid(row=0, column=1)
        column_name = Entry(column_section)
        column_name.grid(row=row, column=1, padx=10)

        Label(column_section, text="Column Datatype:").grid(row=0, column=2)
        column_dtype = Entry(column_section)
        column_dtype.grid(row=row, column=2, padx=10)

        Label(column_section, text="Column Constraints:").grid(row=0, column=3)
        column_constraints = Entry(column_section)
        column_constraints.grid(row=row, column=3, padx=10)

        data[column_name] = {
            "Data Type": column_dtype,
            "Constraints": column_constraints}

    def create():
        col_names = []
        col_dtype = []
        col_constraints = []
        query = ""

        for name in data:
            col_names.append(name.get())
            col_dtype.append(data[name]['Data Type'].get())
            col_constraints.append(data[name]['Constraints'].get())

        for i in range(0, column_len):
            query = query + \
                f"{col_names[i]} {col_dtype[i]} {col_constraints[i]}, "
            if (i + 1 == column_len):
                query = query[:-2]

        try:
            db_query(f"CREATE TABLE {table_name.get()}({query}); ")
            data_list.insert(END, table_name.get())
            global tables_list
            tables_list += [table_name.get()]

        except Exception as e:
            add_log(f"\nERROR:\n{e}\n")

    Button(window, text="Create", command=create).pack()


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
                data_list.insert(END, name)
                global db_list
                db_list += [name]
            except:
                delete_last_log()
                messagebox.showerror("Error",
                                     ("Failed to create database! Make sure"
                                      " your database don't contain any"
                                      " invalid characters."))


def delete_db():
    selection = data_list.curselection()

    try:
        selection = int(selection[0])
        global db_list

        confirmation = messagebox.askquestion('Delete DB',
                                              'Do you really want to '
                                              f'delete {db_list[selection]}')

        if(confirmation == 'yes'):
            db_query(f"DROP DATABASE {db_list[selection]};")
            db_list.pop(selection)
            data_list.delete(selection)

    except IndexError:
        messagebox.showerror("Error",
                             "Please choose database first!")
    except:
        delete_last_log()
        messagebox.showerror("Error",
                             "Failed to delete!")


def select_db():
    selection = data_list.curselection()

    selection = int(selection[0])

    global db_list
    add_log(f"USE {db_list[selection]};")
    mydb.database = db_list[selection]
    title_label.config(text="Select Tables")
    create_btn.config(command=create_table)
    delete_btn.config(command=delete_table)
    select_btn.config(command=select_table)
    show_tables()


def edit_db():
    messagebox.showwarning(title="NO!", message="😬No")


def create_table():
    col_len = askinteger(title="Create Column",
                         prompt="How many columns you want?")
    if col_len > 30:
        messagebox.showwarning(title="Error", message="Max limit is 30!")
    elif col_len <= 0:
        messagebox.showwarning(title="Error", message="Min limit is 1!")
    else:
        create_column(col_len)


def delete_table():
    selection = data_list.curselection()
    try:
        selection = int(selection[0])
        global tables_list
        db_query(f"DROP TABLE {tables_list[selection]};")
        tables_list.pop(selection)
        data_list.delete(selection)
    except IndexError:
        messagebox.showerror("Error",
                             "Please choose table first!")
    except:
        delete_last_log()
        messagebox.showerror("Error",
                             "Failed to delete!")


def select_table():
    selection = data_list.curselection()
    selection = int(selection[0])

    global tables_list
    table_data = db_query(f"SELECT * FROM {tables_list[selection]};")

    table_window = Toplevel()
    table_window.state("zoomed")
    table_window.minsize(400, 100)
    scroll_view = ScrollableFrame(table_window)
    column_names = mycursor.column_names

    for index, name in enumerate(column_names):
        Label(scroll_view.scrollable_frame, text=name).grid(
            row=0, column=index + 1)

    for count, data in enumerate(table_data):
        column_len = len(data)
        for column_index in range(0, column_len):
            Label(scroll_view.scrollable_frame, text=data[column_index]).grid(
                row=count + 1, column=column_index + 1)

    scroll_view.pack(fill=BOTH, expand=True)


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
user_section = Frame(root, borderwidth=1, relief="ridge")
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
                      font=(font_family, 12))
welcome_label.pack()

username_label = Label(user_panel,
                       highlightthickness=0,
                       borderwidth=0,
                       pady=0,
                       text="Vipul",
                       font=(font_family, 20))
username_label.pack()

################################ Log Section #################################
log_section = Frame(user_section)
log_section.pack(side=BOTTOM)

log_title_bar = Frame(log_section, borderwidth=1, relief="sunken")
log_title_bar.pack(side=TOP, fill=X)

log_label = Label(log_title_bar,
                  text="Logs:",
                  font=(font_family, 12))
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
                    text="Choose Database",
                    font=(font_family, 28))
title_label.pack(side=LEFT)

create_btn_img = PhotoImage(file="UI/Create Button.png")
create_btn = Button(title_bar,
                    image=create_btn_img,
                    borderwidth=0,
                    command=create_db)
create_btn.pack(side=RIGHT, padx=25)

############################### Database Panel ###############################
database_panel = Frame(database_section)
database_panel.pack(side=TOP, fill=BOTH, expand=True)

database_scroll = Scrollbar(database_panel)
database_scroll.pack(side=RIGHT, fill=Y)

data_list = Listbox(database_panel,
                    yscrollcommand=database_scroll.set,
                    bd=0,
                    font=(font_family, 14),
                    highlightcolor="white",
                    bg="white")

show_db()

data_list.pack(side=LEFT, fill=BOTH, expand=True)
database_scroll.config(command=data_list.yview)

################################# Action Bar #################################
action_bar = Frame(database_section)
action_bar.pack(side=BOTTOM, fill=X)

delete_icon_img = PhotoImage(file="UI/Delete Button.png")
delete_btn = Button(action_bar,
                    image=delete_icon_img,
                    font=(font_family, 16),
                    borderwidth=0,
                    command=delete_db)
delete_btn.pack(side=RIGHT, padx=(0, 25))

edit_icon_img = PhotoImage(file="UI/Edit Button.png")
edit_btn = Button(action_bar,
                  image=edit_icon_img,
                  font=(font_family, 16),
                  borderwidth=0,
                  command=edit_db)
edit_btn.pack(side=RIGHT, padx=(0, 10))

insert_icon_img = PhotoImage(file="UI/Insert Button.png")
insert_btn = Button(action_bar,
                    image=insert_icon_img,
                    font=(font_family, 16),
                    borderwidth=0,
                    command=edit_db)
insert_btn.pack(side=RIGHT, padx=(0, 10))

select_icon_img = PhotoImage(file="UI/Select Button.png")
select_btn = Button(action_bar,
                    image=select_icon_img,
                    font=(font_family, 16),
                    borderwidth=0,
                    command=select_db)
select_btn.pack(side=RIGHT, padx=(0, 10))

back_icon_img = PhotoImage(file="UI/Back Button.png")
back_btn = Button(action_bar,
                  image=back_icon_img,
                  font=(font_family, 16),
                  borderwidth=0,
                  command=select_db)
back_btn.pack(side=LEFT, padx=(25, 0))

mainloop()
