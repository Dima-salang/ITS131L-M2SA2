import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import os
from PIL import Image, ImageTk

login_flag = False
username = None
password = None
db = "M2SA2_GRP3"

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
root = tkb.Window(themename="superhero")
root.title("CRUD Application")
root.geometry("1500x700")  # Adjust the initial size of the window
root.withdraw()

root.maxsize(1500, 700)
root.minsize(1500, 700)

crud_notebook = tkb.Notebook(root, bootstyle="warning")
crud_notebook.pack(fill='both', expand=1)


# function to establish a connection to the MySQL server. Returns a connector object.
def db_conn(username, passwd, db):
    try:
        print(username)
        print(passwd)
        print(db)

        conn = mysql.connector.connect(
            host="localhost",
            username=username,
            password=passwd,
            db=db
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error Authenticating", message=f"Error: {err}")


# function to build the database first
def build_db(username, passwd):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            username=username,
            password=passwd
        )

        cursor = conn.cursor()
        create_db = """
                    CREATE DATABASE IF NOT EXISTS M2SA2_GRP3;
                    """
        
        cursor.execute(create_db)

        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error creating database", message=f"Error creating database: {err}")
        return     


def show_login_form():
    global login_flag
    login_flag = False # indicates whether the login is successful or not.
    login_window = tkb.Toplevel(root)
    login_window.title("MySQL Login")
    login_window.geometry("500x300")
    login_window.maxsize(500, 300)
    login_window.minsize(500, 300)

    def on_close():
        login_window.destroy() # we destroy the login_window first
        root.destroy()  # Close the root window if login window is closed without logging in

    login_window.protocol("WM_DELETE_WINDOW", on_close)

    crud_title = tkb.Label(login_window, text="Simple CRUD", font=("Helvetica", 28))
    crud_title.grid(row=0, column=2, columnspan=2)

    tkb.Label(login_window, text="MySQL Username:").grid(row=1, column=0, pady=(10,10))
    username_entry = tkb.Entry(login_window, bootstyle="primary")
    username_entry.grid(row=1, column=2, columnspan=2)

    tkb.Label(login_window, text="MySQL Password:").grid(row=2, column=0)
    password_entry = tkb.Entry(login_window, show="*", bootstyle="primary")
    password_entry.grid(row=2, column=2, columnspan=2)

    def login_callback():
        global username, password
        username = username_entry.get()
        password = password_entry.get()
        login_success = login(username, password, login_window)
        if login_success:
            init_tables()
            populate_table()
        clear_fields()

    login_button = tkb.Button(login_window, text="Login", command=login_callback,style="success")
    login_button.grid(row=3, column=3, sticky=tk.W)

    def clear_fields():
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    clear_button = tkb.Button(login_window, text="Clear", command=clear_fields, bootstyle="danger")
    clear_button.grid(row=3, column=3, pady=5, padx=35)

    if login_flag == False:
        clear_fields()

    login_window.bind('<Return>', lambda event=None: login_callback())

def login(username, password, window):
    try:
        build_db(username, password)
        conn = db_conn(username, password, "M2SA2_GRP3")
        conn.close()  # Close the connection as we just want to check if we can connect
        messagebox.showinfo("Login Success", "You are now logged in.")
        window.destroy()
        root.deiconify()
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Login Failed", "Invalfac_no Credentials! Could not connect to MySQL: {}".format(err))
        return False


show_login_form()  # Call to display the login form


def init_tables():
    

    try:
        global username, password, db
        print("init_tables called db_conn")
        conn = db_conn(username, password, db)
        cursor = conn.cursor()
        
        # create the faculty table
        faculty_table = """
                        CREATE TABLE IF NOT EXISTS FACULTY
                        (
                            fac_no INT PRIMARY KEY AUTO_INCREMENT,
                            fac_lname VARCHAR(20),
                            fac_fname VARCHAR(20),
                            birth_date DATE,
                            hire_date DATE
                        );
                        """
        
        school_table = """
                        CREATE TABLE IF NOT EXISTS SCHOOL
                        (
                            school_no CHAR(4) PRIMARY KEY,
                            school_name VARCHAR(40)
                        );
                        """
        
        payroll_table = """
                        CREATE TABLE IF NOT EXISTS PAYROLL
                        (
                            fac_no INT,
                            FOREIGN KEY(fac_no) REFERENCES FACULTY(fac_no),
                            fac_pay INT,
                            from_date DATE,
                            to_date DATE
                        );
                        """
        
        positions_table = """
                        CREATE TABLE IF NOT EXISTS POSITIONS
                        (
                            fac_no INT,
                            FOREIGN KEY(fac_no) REFERENCES FACULTY(fac_no),
                            pos VARCHAR(50),
                            from_date DATE,
                            to_date DATE
                        );
                        """
        
        coord_table = """
                        CREATE TABLE IF NOT EXISTS COORD
                        (
                            school_no CHAR(4),
                            fac_no INT,
                            from_date DATE,
                            to_date DATE,
                            FOREIGN KEY(school_no) REFERENCES SCHOOL(school_no),
                            FOREIGN KEY(fac_no) REFERENCES FACULTY(fac_no)
                        );
                        """
        
        dept_fac_table = """
                        CREATE TABLE IF NOT EXISTS DEPT_FAC
                        (
                            fac_no INT,
                            school_no CHAR(4),
                            from_date DATE,
                            to_date DATE,
                            FOREIGN KEY(school_no) REFERENCES SCHOOL(school_no),
                            FOREIGN KEY(fac_no) REFERENCES FACULTY(fac_no)
                        );
                        """
        cursor.execute(faculty_table)
        print("CREATED FACULTY TABLE")

        cursor.execute(school_table)
        print("CREATED SCHOOL TABLE")

        cursor.execute(payroll_table)
        print("CREATED PAYROLL TABLE")

        cursor.execute(positions_table)
        print("CREATED POSITIONS TABLE")

        cursor.execute(coord_table)
        print("CREATED COORD TABLE")

        cursor.execute(dept_fac_table)
        print("CREATED DEPT_FAC TABLE")
        
        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error in creating tables", message=f"Error in creating tables: {err}")

def insert_data(fac_no, fac_lname, fac_fname, birth_date, hire_date):
    print(fac_no, fac_lname, fac_fname, birth_date, hire_date)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO FACULTY (fac_no, fac_lname, fac_fname, birth_date, hire_date) VALUES (%s, %s, %s, %s, %s)",
                       (fac_no, fac_lname, fac_fname, birth_date, hire_date))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    finally:
        conn.close()

def update_data(fac_no, fac_lname, fac_fname, birth_date, hire_date):
    global username, password, db
    print("update_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE FACULTY SET fac_lname=%s, fac_fname=%s, birth_date=%s, hire_date=%s WHERE fac_no=%s",
                       (fac_lname, fac_fname, birth_date, hire_date, fac_no))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()



def delete_data(fac_no):
    global username, password, db
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM FACULTY WHERE fac_no=%s", (fac_no,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    finally:
        conn.close()

def clear_entries():
    for entry in [fac_no_entry, fac_lname_entry, fac_fname_entry, birth_date_entry, hire_date_entry]:
        entry.delete(0, tk.END)

def populate_table():
    global username, password, db
    print("populate table called db_conn")
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM FACULTY")
    rows = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", "end", values=row)
    conn.close()

def add_record():
    fac_no_value = fac_no_entry.get()
    fac_lname_value = fac_lname_entry.get()
    fac_fname_value = fac_fname_entry.get()
    birth_date_value = birth_date_entry.get()
    hire_date_value = hire_date_entry.get()
    
    if fac_no_value and fac_lname_value and fac_fname_value and birth_date_value and hire_date_value:
        try:
            insert_data(fac_no_value, fac_lname_value, fac_fname_value, birth_date_value, hire_date_value)
            clear_entries()
            populate_table()
        except:
            print("error")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")

def update_record():
    selected_item = treeview.selection()
    if selected_item:
        update_data(treeview.item(selected_item)['values'][0],
                    fac_lname_entry.get(), fac_fname_entry.get(), birth_date_entry.get(), hire_date_entry.get())
        clear_entries()
        populate_table()
    else:
        messagebox.showerror("Error", "Please select a record to update.")

def delete_record():
    selected_item = treeview.selection()
    if selected_item:
        delete_data(treeview.item(selected_item)['values'][0])
        clear_entries()
        populate_table()
    else:
        messagebox.showerror("Error", "Please select a record to delete.")

def search_records(keyword):
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM FACULTY WHERE fac_lname LIKE %s OR fac_fname LIKE %s OR birth_date LIKE %s OR hire_date LIKE %s"
    cursor.execute(query, ('%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%', '%'+keyword+'%'))
    rows = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", "end", values=row)
    conn.close()

def search_button_click():
    keyword = search_entry.get()
    search_records(keyword)

def select_item(event):
    selected_item = treeview.selection()
    if selected_item:
        values = treeview.item(selected_item[0], 'values')
        fac_no_entry.delete(0, tk.END)
        fac_no_entry.insert(0, values[0])
        fac_lname_entry.delete(0, tk.END)
        fac_lname_entry.insert(0, values[1])
        fac_fname_entry.delete(0, tk.END)
        fac_fname_entry.insert(0, values[2])
        birth_date_entry.delete(0, tk.END)
        birth_date_entry.insert(0, values[3])
        hire_date_entry.delete(0, tk.END)
        hire_date_entry.insert(0, values[4])

def add_placeholder_to(entry: tkb.Entry, placeholder: str, color='grey'):
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)

    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Frames for organization
faculty_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
faculty_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

table_frame = tkb.Frame(faculty_frame, padding="0 70 10 10")
table_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

school_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
school_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

school_table_frame = tkb.Frame(school_frame, padding="0 70 10 10")
school_table_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

payroll_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
payroll_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

payroll_table_frame = tkb.Frame(payroll_frame, padding="0 70 10 10")
payroll_table_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

positions_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
positions_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

positions_table = tkb.Frame(positions_frame, padding="0 70 10 10")
positions_table.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
coord_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_table_frame = tkb.Frame(coord_frame, padding="0 70 10 10")
coord_table_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
dept_fac_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_table = tkb.Frame(dept_fac_frame, padding="0 70 10 10")
dept_fac_table.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))



# Adjusting weights for resizing behavior
root.columnconfigure(1, weight=3)  # Give more weight to the table frame
root.rowconfigure(1, weight=1)

# Search section
search_entry = tkb.Entry(table_frame, width=35)
add_placeholder_to(search_entry, "Search for Records")
search_image = Image.open("search_icon.png")  # Provfac_noe the correct path to your image file
search_image = search_image.resize((12, 12))
search_icon = ImageTk.PhotoImage(search_image)
search_button = tkb.Button(table_frame, compound=tk.LEFT, command=search_button_click,padding=(1,1))
search_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_button.grid(row=0, column=0, padx=(0, 10), sticky=tk.E)

# CRUD Information Section
crud_info_header = tkb.Label(faculty_frame, text="Simple CRUD", font=("Times New Roman", 25, "bold"))
crud_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

# CRUD section with entries and labels below them
crud_info_label = tkb.LabelFrame(faculty_frame, text="INFORMATION", borderwidth=2)
crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# CRUD section with entries and labels below them
crud_section = tkb.Frame(crud_info_label, padding=10)
crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

labels = ["Faculty Number", "Last Name", "First Name", "Birth Date", "Hire Date"]
entries = []
for i, label_text in enumerate(labels):
    label = tkb.Label(crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2*i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(crud_section, width=50)
    entry.grid(row=2*i+1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    entries.append(entry)
    
fac_no_entry, fac_lname_entry, fac_fname_entry, birth_date_entry, hire_date_entry = entries
add_placeholder_to(fac_no_entry, "Enter Faculty Number")
add_placeholder_to(fac_lname_entry, "Enter Last Name")
add_placeholder_to(fac_fname_entry, "Enter First Name")
add_placeholder_to(birth_date_entry, "Enter Birth Date")
add_placeholder_to(hire_date_entry, "Enter Hire Date")

# Load icons for add, update, and delete buttons
add_image = Image.open("add_icon.png")
add_image = add_image.resize((20, 20))
add_icon = ImageTk.PhotoImage(add_image)

update_image = Image.open("update_icon.png")
update_image = update_image.resize((20, 20))
update_icon = ImageTk.PhotoImage(update_image)

delete_image = Image.open("delete_icon.png")
delete_image = delete_image.resize((20, 20))
delete_icon = ImageTk.PhotoImage(delete_image)

# Buttons for CRUD operations
button_icons = [add_icon, update_icon, delete_icon]
button_texts = ["Add", "Update", "Delete"]
commands = [add_record, update_record, delete_record]
buttons_frame = tkb.Frame(crud_info_label, padding=10)
buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
for i, (text, icon, cmd) in enumerate(zip(button_texts, button_icons, commands)):
    button = tkb.Button(buttons_frame, text=text, compound=tk.LEFT, command=cmd)
    button.grid(row=0, column=i, padx=5)

# Treeview for displaying data
treeview = tkb.Treeview(table_frame, columns=("Faculty Number", "Last Name", "First Name", "Birthday", "Hire Date"), show="headings", bootstyle="info")
for col in treeview["columns"]:
    treeview.heading(col, text=col)
    treeview.column(col, anchor=tk.W)
treeview.column("Faculty Number", width=40)
treeview.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Bind select event
treeview.bind('<<TreeviewSelect>>', select_item)

# Initialize database and populate table
crud_notebook.add(faculty_frame, text="Faculty")
crud_notebook.add(school_frame, text="School")
crud_notebook.add(payroll_frame, text="Payrolls")
crud_notebook.add(positions_frame, text="Positions")
crud_notebook.add(coord_frame, text="Coordinators")
crud_notebook.add(dept_fac_frame, text="Department Faculties")

root.mainloop()
