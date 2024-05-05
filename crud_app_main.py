import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import ttkbootstrap as tkb
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import os
from PIL import Image, ImageTk
import csv
import subprocess

login_flag = False
username = None
password = None
db = "M2SA2_GRP3"

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
root = tkb.Window(themename="superhero")
root.title("CRUD Application")
#slighly Edited the screen size
root.geometry("1700x700")
root.withdraw()

root.maxsize(1700, 700)
root.minsize(1700, 700)

crud_notebook = tkb.Notebook(root, bootstyle="primary")
crud_notebook.pack(fill='both', expand=1)

# Frames for organization
faculty_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
faculty_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

faculty_data_frame = tkb.Frame(faculty_frame)
faculty_data_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

table_frame = tkb.Frame(faculty_data_frame, padding="0 8 10 10")
table_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

faculty_options_frame = tkb.Frame(faculty_data_frame, padding="0 8 10 10")
faculty_options_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

school_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
school_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

school_data_frame = tkb.Frame(school_frame)
school_data_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

school_table_frame = tkb.Frame(school_data_frame, padding="0 8 10 10")
school_table_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

school_options_frame = tkb.Frame(school_data_frame, padding="0 8 10 10")
school_options_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

payroll_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
payroll_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

payroll_data_frame = tkb.Frame(payroll_frame)
payroll_data_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

payroll_table_frame = tkb.Frame(payroll_data_frame, padding="0 8 10 10")
payroll_table_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

payroll_options_frame = tkb.Frame(payroll_data_frame, padding="0 8 10 10")
payroll_options_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

positions_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
positions_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

positions_data_frame = tkb.Frame(positions_frame)
positions_data_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

positions_table_frame = tkb.Frame(positions_data_frame, padding="0 8 10 10")
positions_table_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

positions_options_frame = tkb.Frame(positions_data_frame, padding="0 8 10 10")
positions_options_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
coord_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_data_frame = tkb.Frame(coord_frame)
coord_data_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_table_frame = tkb.Frame(coord_data_frame, padding="0 8 10 10")
coord_table_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_options_frame = tkb.Frame(coord_data_frame, padding="0 8 10 10")
coord_options_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_frame = tkb.Frame(crud_notebook, padding="90 0 0 10")
dept_fac_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_data_frame = tkb.Frame(dept_fac_frame)
dept_fac_data_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_table_frame = tkb.Frame(dept_fac_data_frame, padding="0 8 10 10")
dept_fac_table_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_options_frame = tkb.Frame(dept_fac_data_frame, padding="0 8 10 10")
dept_fac_options_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

crud_notebook.add(faculty_frame, text="Faculty")
crud_notebook.add(school_frame, text="School")
crud_notebook.add(payroll_frame, text="Payrolls")
crud_notebook.add(positions_frame, text="Positions")
crud_notebook.add(coord_frame, text="Coordinators")
crud_notebook.add(dept_fac_frame, text="Department Faculties")



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

# function to check whether the user already initialized the app once to prevent inserting redundant dummy data
def check_init():
    return os.path.exists("init.flag")


def create_dummies():

    try:
        global username, password, db
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        faculty_dummy = """
        INSERT INTO FACULTY (fac_lname, fac_fname, birth_date, hire_date) VALUES
        ('Santos', 'Juan', '1980-05-15', '2005-09-20'),
        ('Garcia', 'Maria', '1975-08-23', '2008-03-10'),
        ('Cruz', 'Miguel', '1982-11-10', '2010-06-28'),
        ('Reyes', 'Jessica', '1978-04-03', '2003-11-15'),
        ('Torres', 'Christian', '1985-10-20', '2015-02-18'),
        ('Dela Cruz', 'Ana', '1970-12-08', '2000-07-05'),
        ('Aquino', 'Mateo', '1987-03-25', '2012-09-30'),
        ('Lopez', 'Jenelyn', '1973-06-17', '2006-12-12'),
        ('Mendoza', 'Daniel', '1984-09-12', '2018-05-22'),
        ('Dizon', 'Amanda', '1976-02-28', '2002-04-14');
        """

        school_dummy = """
        INSERT INTO SCHOOL (school_no, school_name) VALUES
        ('S001', 'SOIT'),
        ('A002', 'ARIDBE'),
        ('S003', 'SCEGE'),
        ('M004', 'SMME'),
        ('E005', 'SEEC'),
        ('I006', 'SIEE'),
        ('C007', 'SCBM');
        """

        payroll_dummy = """
        INSERT INTO PAYROLL (fac_no, fac_pay, from_date, to_date) VALUES
        (1, 50000, '2024-01-01', '2024-01-15'),
        (2, 55000, '2024-01-10', '2024-01-25'),
        (3, 60000, '2024-01-05', '2024-01-20'),
        (4, 52000, '2024-01-15', '2024-01-30'),
        (5, 58000, '2024-01-20', '2024-02-04'),
        (6, 53000, '2024-01-25', '2024-02-09'),
        (7, 57000, '2024-01-01', '2024-01-16'),
        (8, 62000, '2024-01-07', '2024-01-22'),
        (9, 54000, '2024-01-12', '2024-01-27'),
        (10, 56000, '2024-01-17', '2024-02-01');
        """

        positions_dummy = """
        INSERT INTO POSITIONS (fac_no, pos, from_date, to_date) VALUES
        (1, 'Professor', '2024-01-01', '2024-01-15'),
        (2, 'Associate Professor', '2024-01-10', '2024-01-25'),
        (3, 'Assistant Professor', '2024-01-05', '2024-01-20'),
        (4, 'Lecturer', '2024-01-15', '2024-01-30'),
        (5, 'Senior Lecturer', '2024-01-20', '2024-02-04'),
        (6, 'Instructor', '2024-01-25', '2024-02-09'),
        (7, 'Dean', '2024-01-01', '2024-01-16'),
        (8, 'Associate Dean', '2024-01-07', '2024-01-22'),
        (9, 'Assistant', '2024-01-12', '2024-01-27'),
        (10, 'Vice President', '2024-01-17', '2024-02-01');
        """

        coord_dummy = """
        INSERT INTO COORD (school_no, fac_no, from_date, to_date) VALUES
        ('S001', 1, '2024-01-01', '2024-01-15'),
        ('A002', 2, '2024-01-10', '2024-01-25'),
        ('S003', 3, '2024-01-05', '2024-01-20'),
        ('M004', 4, '2024-01-15', '2024-01-30'),
        ('E005', 5, '2024-01-20', '2024-02-04'),
        ('I006', 6, '2024-01-25', '2024-02-09'),
        ('C007', 7, '2024-01-01', '2024-01-16'),
        ('S001', 8, '2024-01-07', '2024-01-22'),
        ('A002', 9, '2024-01-12', '2024-01-27'),
        ('S003', 10, '2024-01-17', '2024-02-01');
        """

        dept_fac_dummy = """
        INSERT INTO DEPT_FAC (fac_no, school_no, from_date, to_date) VALUES
        (1, 'S001', '2024-01-01', '2024-01-15'),
        (2, 'A002', '2024-01-10', '2024-01-25'),
        (3, 'S003', '2024-01-05', '2024-01-20'),
        (4, 'M004', '2024-01-15', '2024-01-30'),
        (5, 'E005', '2024-01-20', '2024-02-04'),
        (6, 'I006', '2024-01-25', '2024-02-09'),
        (7, 'C007', '2024-01-01', '2024-01-16'),
        (8, 'S001', '2024-01-07', '2024-01-22'),
        (9, 'A002', '2024-01-12', '2024-01-27'),
        (10, 'S003', '2024-01-17', '2024-02-01');
        """

        cursor.execute(faculty_dummy)
        print("inserted faculty dummies")

        cursor.execute(school_dummy)
        print("inserted school dummies")

        cursor.execute(payroll_dummy)
        print("inserted payroll dummies")

        cursor.execute(positions_dummy)
        print("inserted positions dummies")

        cursor.execute(coord_dummy)
        print("inserted coord dummies")

        cursor.execute(dept_fac_dummy)
        print("inserted dept_fac dummies")

        conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"{err}")



def create_init():
    print("called create init")
    try:
        create_dummies()
        print("created dummies")
        with open("init.flag", "w") as file:
            file.write("initialized.")
    except mysql.connector.Error as err:
        print(f"{err}")
        messagebox.showerror(title="Error", message=f"{err}")



def show_login_form():

    global login_flag, username_entry, password_entry, login_window
    login_flag = False  # indicates whether the login is successful or not.
    login_window = tkb.Toplevel(root)
    login_window.title("MySQL Login")
    login_window.geometry("500x250") #slighly Edited the screen size
    login_window.maxsize(500, 250)
    login_window.minsize(500, 200)

    def on_close():
        login_window.destroy()  # we destroy the login_window first
        root.destroy()  # Close the root window if login window is closed without logging in

    login_window.protocol("WM_DELETE_WINDOW", on_close)

    crud_title = tkb.Label(login_window, text="Simple CRUD", font=("Helvetica", 28, 'underline'))
    crud_title.grid(row=0, column=2, columnspan=2, pady=(10, 20))

    tkb.Label(login_window, text="MySQL Username:").grid(row=1, column=0, pady=(10, 10), padx=(10, 0))
    username_entry = tkb.Entry(login_window, style="primary")  # Fix typo here
    username_entry.grid(row=1, column=2, columnspan=2)

    tkb.Label(login_window, text="MySQL Password:").grid(row=2, column=0, padx=(10, 0))
    password_entry = tkb.Entry(login_window, show="*", style="primary")  # Fix typo here
    password_entry.grid(row=2, column=2, columnspan=2)

    def login_callback():
        global username, password, login_window
        username = username_entry.get()
        password = password_entry.get()
        login_success = login(username, password, login_window)
        if login_success:
            init_tables()
            if not check_init():
                create_init()
            populate_table()
            clear_fields()

    login_button = tkb.Button(login_window, text="Login", command=login_callback, style="success")
    login_button.grid(row=3, column=3, sticky=tk.W)

    def clear_fields():
        if username_entry.winfo_exists():
            username_entry.delete(0, tk.END)
        if password_entry.winfo_exists():
            password_entry.delete(0, tk.END)


    clear_button = tkb.Button(login_window, text="Clear", command=clear_fields, style="danger")  # Fix typo here
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
                            payroll_no INT PRIMARY KEY AUTO_INCREMENT,
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
                            positions_no INT PRIMARY KEY AUTO_INCREMENT,
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
                            coord_no INT PRIMARY KEY AUTO_INCREMENT,
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
                            dept_fac_no INT PRIMARY KEY AUTO_INCREMENT,
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


""" GLOBAL FUNCTIONS """


def backup_db():
    default_path = os.getcwd()
    try:
        global username, password, db
        sql_path = filedialog.asksaveasfilename(title="Choose Where to Save Database", confirmoverwrite=True,
                                                initialdir=default_path, defaultextension=".sql",
                                                filetypes=[("SQL files", "*.sql")])
        if sql_path:
            # command to back up the db using mysqldump
            command = f"mysqldump --user={username} --password={password} {db} > {sql_path}"

            # we use subprocess to interact with a terminal
            subprocess.run(command, shell=True)

            messagebox.showinfo(title="DB Saved", message=f"Database {db} successfully saved at {sql_path}")
    except Exception as err:
        messagebox.showerror(title="Error", message=f"Error: {err}")


def on_tab_change(event):
    selected_tab = event.widget.select()
    tab_index = event.widget.index(selected_tab)
    print("Current tab: ", tab_index)
    match tab_index:
        case 1:
            populate_table_school()
        case 2:
            populate_table_payroll()
        case 3:
            populate_table_positions()
        case 4:
            populate_table_coord()
        case 5:
            populate_table_dept_fac()


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


# retain


""" FACULTY SECTION """


def insert_data(fac_no, fac_lname, fac_fname, birth_date, hire_date):
    print(fac_no, fac_lname, fac_fname, birth_date, hire_date)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO FACULTY (fac_no, fac_lname, fac_fname, birth_date, hire_date) VALUES (%s, %s, %s, %s, %s)",
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
    except mysql.connector.IntegrityError:
        messagebox.showerror(title="Error:", message="You cannot delete that has records dependent on it...\n")
    finally:
        conn.close()


def delete_record():
    selected_item = treeview.selection()
    if selected_item:
        delete_data(treeview.item(selected_item)['values'][0])
        clear_entries()
        populate_table()
    else:
        messagebox.showerror("Error", "Please select a record to delete.")


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


def search_records(keyword):
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM FACULTY WHERE fac_no LIKE %s OR fac_lname LIKE %s OR fac_fname LIKE %s OR birth_date LIKE %s OR hire_date LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", "end", values=row)
    conn.close()


# retain
def search_button_click():
    keyword = search_entry.get()
    search_records(keyword)


# write to csv function
def faculty_write_to_csv():
    default_path = os.getcwd()
    csv_path = filedialog.asksaveasfilename(initialdir=default_path, defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if csv_path:
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(["Faculty Number", "Last Name",
                                 "First Name", "Birth Date", "Hire Date"])

                global username, password, db
                conn = db_conn(username, password, db)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM FACULTY")

                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)
                conn.close()

            messagebox.showinfo(title="Write Success", message=f"Data successfully written to {csv_path}")
        except Exception as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")


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


def faculty_sort_by(search_column, opt_ord):
    match search_column:
        case "Faculty Number":
            search_column = "fac_no"
        case "Last Name":
            search_column = "fac_lname"
        case "First Name":
            search_column = "fac_fname"
        case "Birth Date":
            search_column = "birth_date"
        case "Hire Date":
            search_column = "hire_date"
        case _:
            # Handle invalid search column
            messagebox.showerror(title="Error", message="Invalid search column")
            return
    print(search_column)

    try:
        global username, password, db
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        query = f"""SELECT * FROM FACULTY ORDER BY {search_column}"""
        if opt_ord:
            query += " DESC"
        print(query)
        cursor.execute(query)
        rows = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in rows:
            print(row)
            treeview.insert("", "end", values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error {err}")


""" SCHOOL SECTION """


def select_item_school(event):
    selected_item = school_treeview.selection()
    if selected_item:
        values = school_treeview.item(selected_item[0], 'values')
        school_no_entry.delete(0, tk.END)
        school_no_entry.insert(0, values[0])
        school_name_entry.delete(0, tk.END)
        school_name_entry.insert(0, values[1])


def insert_data_school(school_no, school_name):
    print(school_no, school_name)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO SCHOOL (school_no, school_name) VALUES (%s, %s)",
            (school_no, school_name))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    finally:
        conn.close()


def update_data_school(school_no, school_name):
    global username, password, db
    print("update_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE SCHOOL SET school_no=%s, school_name=%s WHERE school_no=%s",
                       (school_no, school_name, school_no))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()


def delete_data_school(school_no):
    global username, password, db
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SCHOOL WHERE school_no=%s", (school_no,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror(title="Error:", message="You cannot delete that has records dependent on it...\n")
    finally:
        conn.close()


def delete_record_school():
    selected_item = school_treeview.selection()
    if selected_item:
        delete_data_school(school_treeview.item(selected_item)['values'][0])
        print(school_treeview.item(selected_item)['values'][0])
        clear_entries_school()
        populate_table_school()
    else:
        messagebox.showerror("Error", "Please select a record to delete.")


def clear_entries_school():
    for entry in [school_no_entry, school_name_entry]:
        entry.delete(0, tk.END)


def populate_table_school():
    global username, password, db
    print("populate table called db_conn")
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SCHOOL")
    rows = cursor.fetchall()
    school_treeview.delete(*school_treeview.get_children())
    for row in rows:
        school_treeview.insert("", "end", values=row)
    conn.close()


def add_record_school():
    school_no_value = school_no_entry.get()
    school_name_value = school_name_entry.get()

    if school_no_value and school_name_value:
        try:
            insert_data_school(school_no_value, school_name_value)
            print("school inserted data")
            clear_entries_school()
            print("school cleared entries")
            populate_table_school()
            print("school populated school table")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")


def update_record_school():
    selected_item = school_treeview.selection()
    if selected_item:
        update_data_school(school_treeview.item(selected_item)['values'][0],
                           school_name_entry.get())
        clear_entries_school()
        populate_table_school()
    else:
        messagebox.showerror("Error", "Please select a record to update.")


def search_school_records(keyword):
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM SCHOOL WHERE school_no LIKE %s OR school_name LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    school_treeview.delete(*school_treeview.get_children())
    for row in rows:
        school_treeview.insert("", "end", values=row)
    conn.close()


def search_school_button_click():
    keyword = search_entry_school.get()
    search_school_records(keyword)


# write to csv function
def school_write_to_csv():
    default_path = os.getcwd()
    csv_path = filedialog.asksaveasfilename(initialdir=default_path, defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if csv_path:
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(["School Number", "School Name"])

                global username, password, db
                conn = db_conn(username, password, db)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM SCHOOL")

                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)
                conn.close()

            messagebox.showinfo(title="Write Success", message=f"Data successfully written to {csv_path}")
        except Exception as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")


def school_sort_by(search_column, opt_ord):
    match search_column:
        case "School Number":
            search_column = "school_no"
        case "School Name":
            search_column = "school_name"
        case _:
            # Handle invalid search column
            messagebox.showerror(title="Error", message="Invalid search column")
            return
    print(search_column)

    global username, password, db
    try:
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        query = f""" SELECT * FROM SCHOOL ORDER BY {search_column}"""
        if opt_ord:
            query += " DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        school_treeview.delete(*school_treeview.get_children())
        for row in rows:
            school_treeview.insert("", "end", values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error {err}")


""" PAYROLL SECTION """


def select_item_payroll(event):
    selected_item = payroll_treeview.selection()
    payroll_no_entry.configure(state=NORMAL)
    if selected_item:
        values = payroll_treeview.item(selected_item[0], 'values')
        payroll_no_entry.delete(0, tk.END)
        payroll_no_entry.insert(0, values[0])
        payroll_no_entry.configure(state='readonly')
        payroll_fac_no_entry.delete(0, tk.END)
        payroll_fac_no_entry.insert(0, values[1])
        payroll_pay_amount_entry.delete(0, tk.END)
        payroll_pay_amount_entry.insert(0, values[3])
        payroll_from_date_entry.delete(0, tk.END)
        payroll_from_date_entry.insert(0, values[4])
        payroll_to_date_entry.delete(0, tk.END)
        payroll_to_date_entry.insert(0, values[5])


def insert_data_payroll(payroll_fac_no, payroll_pay_amount, payroll_from_date, payroll_to_date):
    print(payroll_fac_no, payroll_pay_amount, payroll_from_date, payroll_to_date)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO PAYROLL (fac_no, fac_pay, from_date, to_date) VALUES (%s, %s, %s, %s)",
            (payroll_fac_no, payroll_pay_amount, payroll_from_date, payroll_to_date))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error: {err}")

    conn.close()


def update_data_payroll(payroll_no, payroll_fac_no, payroll_pay_amount, payroll_from_date, payroll_to_date):
    global username, password, db
    print("update_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE PAYROLL SET fac_no=%s, fac_pay=%s, from_date=%s, to_date=%s WHERE payroll_no=%s",
                       (payroll_fac_no, payroll_pay_amount, payroll_from_date, payroll_to_date, payroll_no))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()


def delete_data_payroll(payroll_no):
    global username, password, db
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PAYROLL WHERE payroll_no=%s", (payroll_no,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror(title="Error:", message="You cannot delete that has records dependent on it...\n")
    finally:
        conn.close()


def delete_record_payroll():
    selected_item = payroll_treeview.selection()
    if selected_item:
        delete_data_payroll(payroll_treeview.item(selected_item)['values'][0])
        clear_entries_payroll()
        populate_table_payroll()

    else:
        messagebox.showerror("Error", "Please select a record to delete.")


def add_record_payroll():
    payroll_fac_no_value = payroll_fac_no_entry.get()
    payroll_pay_amount_value = payroll_pay_amount_entry.get()
    payroll_from_date_value = payroll_from_date_entry.get()
    payroll_to_date_value = payroll_to_date_entry.get()

    if payroll_fac_no_value and payroll_pay_amount_value and payroll_from_date_value and payroll_to_date_value:
        if payroll_from_date_value > payroll_to_date_value:
            messagebox.showerror(title="Error:", message="From date cannot exceed To Date")
            return
        try:
            insert_data_payroll(payroll_fac_no_value, payroll_pay_amount_value, payroll_from_date_value,
                                payroll_to_date_value)
            print("payroll inserted data")
            clear_entries_payroll()
            print("payroll cleared entries")
            populate_table_payroll()
            print("payroll populated school table")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")


def update_record_payroll():
    selected_item = payroll_treeview.selection()
    payroll_from_date_value = payroll_from_date_entry.get()
    payroll_to_date_value = payroll_to_date_entry.get()
    if selected_item:
        if payroll_from_date_value > payroll_to_date_value:
            messagebox.showerror(title="Error:", message="From date cannot exceed To Date")
            return
        else:
            try:
                update_data_payroll(payroll_treeview.item(selected_item)['values'][0], payroll_fac_no_entry.get(),
                                    payroll_pay_amount_entry.get(), payroll_from_date_value, payroll_to_date_value)
                print(payroll_treeview.item(selected_item)['values'][0])
                clear_entries_payroll()
                populate_table_payroll()
            except mysql.connector.Error as err:
                messagebox.showerror(title="Error", message=f"{err}")

    else:
        messagebox.showerror("Error", "Please select a record to update.")


def clear_entries_payroll():
    for entry in [payroll_no_entry, payroll_fac_no_entry, payroll_pay_amount_entry, payroll_from_date_entry,
                  payroll_to_date_entry]:
        entry.delete(0, tk.END)


def populate_table_payroll():
    global username, password, db
    print("populate table called db_conn")
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    cursor.execute("""
                        SELECT
                        payroll_no,
                        PAYROLL.fac_no,
                        CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname),
                        fac_pay,
                        from_date, 
                        to_date 
                        FROM PAYROLL 
                        INNER JOIN FACULTY ON PAYROLL.fac_no = FACULTY.fac_no""")
    rows = cursor.fetchall()
    payroll_treeview.delete(*payroll_treeview.get_children())
    for row in rows:
        payroll_treeview.insert("", "end", values=row)
    conn.close()


def search_payroll_records(keyword):
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM PAYROLL WHERE payroll_no LIKE %s OR fac_no LIKE %s OR fac_pay LIKE %s OR from_date LIKE %s OR to_date LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    payroll_treeview.delete(*payroll_treeview.get_children())
    for row in rows:
        payroll_treeview.insert("", "end", values=row)
    conn.close()


def search_payroll_button_click():
    keyword = search_entry_payroll.get()
    search_payroll_records(keyword)


# write to csv function
def payroll_write_to_csv():
    default_path = os.getcwd()
    csv_path = filedialog.asksaveasfilename(initialdir=default_path, defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if csv_path:
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(["Payroll Number", "Faculty Number", "Full Name", "Pay Amount", "From Date", "To Date"])

                global username, password, db
                conn = db_conn(username, password, db)
                cursor = conn.cursor()
                cursor.execute("""
                        SELECT
                        payroll_no,
                        PAYROLL.fac_no,
                        CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname),
                        fac_pay,
                        from_date, 
                        to_date 
                        FROM PAYROLL 
                        INNER JOIN FACULTY ON PAYROLL.fac_no = FACULTY.fac_no""")

                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)
                conn.close()

            messagebox.showinfo(title="Write Success", message=f"Data successfully written to {csv_path}")
        except Exception as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")


def payroll_sort_by(search_column, opt_ord):
    match search_column:
        case "Payroll Number":
            search_column = "payroll_no"
        case "Faculty Number":
            search_column = "fac_no"
        case "Pay Amount":
            search_column = "fac_pay"
        case "From Date":
            search_column = "from_date"
        case "To Date":
            search_column = "to_date"
        case _:
            # Handle invalid search column
            messagebox.showerror(title="Error", message="Invalid search column")
            return
    print(search_column)
    global username, password, db
    try:
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        query = f""" SELECT * FROM PAYROLL ORDER BY {search_column}"""
        if opt_ord:
            query += " DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        payroll_treeview.delete(*payroll_treeview.get_children())
        for row in rows:
            payroll_treeview.insert("", "end", values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error {err}")


""" POSITIONS SECTION """


def select_item_positions(event):
    selected_item = positions_treeview.selection()
    positions_no_entry.configure(state=NORMAL)
    if selected_item:
        values = positions_treeview.item(selected_item[0], 'values')
        positions_no_entry.delete(0, tk.END)
        positions_no_entry.insert(0, values[0])
        positions_no_entry.configure(state='readonly')
        positions_fac_no_entry.delete(0, tk.END)
        positions_fac_no_entry.insert(0, values[1])
        positions_position_entry.delete(0, tk.END)
        positions_position_entry.insert(0, values[3])
        positions_from_date_entry.delete(0, tk.END)
        positions_from_date_entry.insert(0, values[4])
        positions_to_date_entry.delete(0, tk.END)
        positions_to_date_entry.insert(0, values[5])


def insert_data_positions(positions_fac_no, positions_position, positions_from_date, positions_to_date):
    print(positions_fac_no, positions_position, positions_from_date, positions_to_date)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO POSITIONS (fac_no, pos, from_date, to_date) VALUES (%s, %s, %s, %s)",
            (positions_fac_no, positions_position, positions_from_date, positions_to_date))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error: {err}")

    conn.close()


def update_data_positions(positions_no, positions_fac_no, positions_position, positions_from_date, positions_to_date):
    global username, password, db
    print("update_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE POSITIONS SET fac_no=%s, pos=%s, from_date=%s, to_date=%s WHERE positions_no=%s",
                       (positions_fac_no, positions_position, positions_from_date, positions_to_date, positions_no))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()


def delete_data_positions(positions_no):
    global username, password, db
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM POSITIONS WHERE positions_no=%s", (positions_no,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror(title="Error:", message="You cannot delete that has records dependent on it...\n")
    finally:
        conn.close()


def clear_entries_positions():
    for entry in [positions_no_entry, payroll_fac_no_entry, payroll_pay_amount_entry, payroll_from_date_entry,
                  payroll_to_date_entry]:
        entry.delete(0, tk.END)


def populate_table_positions():
    global username, password, db
    print("populate table called db_conn")
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT
                    positions_no, 
                    POSITIONS.fac_no, 
                    CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname) AS full_name, 
                    POSITIONS.pos, 
                    POSITIONS.from_date, 
                    POSITIONS.to_date 
                    FROM POSITIONS 
                    INNER JOIN FACULTY ON POSITIONS.fac_no = FACULTY.fac_no""")
    rows = cursor.fetchall()
    positions_treeview.delete(*positions_treeview.get_children())
    for row in rows:
        positions_treeview.insert("", "end", values=row)
    conn.close()


def delete_record_positions():
    selected_item = positions_treeview.selection()
    if selected_item:
        delete_data_positions(positions_treeview.item(selected_item)['values'][0])
        clear_entries_positions()
        populate_table_positions()
    else:
        messagebox.showerror("Error", "Please select a record to delete.")


def add_record_positions():
    positions_fac_no_value = positions_fac_no_entry.get()
    positions_position_value = positions_position_entry.get()
    positions_from_date_value = positions_from_date_entry.get()
    positions_to_date_value = positions_to_date_entry.get()

    if positions_fac_no_value and positions_position_value and positions_from_date_value:
        if positions_to_date_value != "Enter To Date":
            if positions_from_date_value > positions_to_date_value:
                messagebox.showerror(title="Error:", message="From date cannot exceed To Date")
                return
        else:
            positions_to_date_value = None
        try:
            insert_data_positions(positions_fac_no_value, positions_position_value, positions_from_date_value,
                                  positions_to_date_value)
            print("positions inserted data")
            clear_entries_positions()
            print("positions cleared entries")
            populate_table_positions()
            print("positions populated school table")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")


def update_record_positions():
    selected_item = positions_treeview.selection()
    positions_from_date_value = positions_from_date_entry.get()
    positions_to_date_value = positions_to_date_entry.get()
    if selected_item:
        if positions_from_date_value > positions_to_date_value:
            messagebox.showerror(title="Error:", message="From date cannot exceed To Date")
            return
        else:
            try:
                update_data_positions(positions_treeview.item(selected_item)['values'][0], positions_fac_no_entry.get(),
                                      positions_position_entry.get(), positions_from_date_value,
                                      positions_to_date_value)
                clear_entries_positions()
                populate_table_positions()
            except mysql.connector.Error as err:
                messagebox.showerror(title="Error", message=f"{err}")
    else:
        messagebox.showerror("Error", "Please select a record to update.")


def search_positions_records(keyword):
    print("Searched for ", keyword)
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM POSITIONS WHERE positions_no LIKE %s OR fac_no LIKE %s OR pos LIKE %s OR from_date LIKE %s OR to_date LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    positions_treeview.delete(*positions_treeview.get_children())
    for row in rows:
        positions_treeview.insert("", "end", values=row)
    conn.close()


def search_positions_button_click():
    keyword = search_entry_positions.get()
    search_positions_records(keyword)


# write to csv function
def positions_write_to_csv():
    default_path = os.getcwd()
    csv_path = filedialog.asksaveasfilename(initialdir=default_path, defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if csv_path:
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(["Position Number", "Faculty Number", "Full Name", "Position", "From Date", "To Date"])

                global username, password, db
                conn = db_conn(username, password, db)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                    positions_no, 
                    POSITIONS.fac_no, 
                    CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname) AS full_name, 
                    POSITIONS.pos, 
                    POSITIONS.from_date, 
                    POSITIONS.to_date 
                    FROM POSITIONS 
                    INNER JOIN FACULTY ON POSITIONS.fac_no = FACULTY.fac_no""")

                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)
                conn.close()

            messagebox.showinfo(title="Write Success", message=f"Data successfully written to {csv_path}")
        except Exception as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")


def positions_sort_by(search_column, opt_ord):
    match search_column:
        case "Position Number":
            search_column = "positions_no"
        case "Faculty Number":
            search_column = "fac_no"
        case "Position":
            search_column = "pos"
        case "From Date":
            search_column = "from_date"
        case "To Date":
            search_column = "to_date"
        case _:
            # Handle invalid search column
            messagebox.showerror(title="Error", message="Invalid search column")
            return

    print(search_column)
    global username, password, db
    try:
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        query = f""" SELECT * FROM POSITIONS ORDER BY {search_column}"""
        if opt_ord:
            query += " DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        positions_treeview.delete(*positions_treeview.get_children())
        for row in rows:
            positions_treeview.insert("", "end", values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error {err}")


""" COORD SECTION """


def select_item_coord(event):
    selected_item = coord_treeview.selection()
    coord_no_entry.configure(state=NORMAL)
    if selected_item:
        values = coord_treeview.item(selected_item[0], 'values')
        coord_no_entry.delete(0, tk.END)
        coord_no_entry.insert(0, values[0])
        coord_no_entry.configure(state='readonly')
        coord_school_no_entry.delete(0, tk.END)
        coord_school_no_entry.insert(0, values[1])
        coord_fac_no_entry.delete(0, tk.END)
        coord_fac_no_entry.insert(0, values[2])
        coord_from_date_entry.delete(0, tk.END)
        coord_from_date_entry.insert(0, values[5])
        coord_to_date_entry.delete(0, tk.END)
        coord_to_date_entry.insert(0, values[6])


def insert_data_coord(coord_school_no, coord_fac_no, coord_from_date, coord_to_date):
    print(coord_school_no, coord_fac_no, coord_from_date, coord_to_date)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO COORD (school_no, fac_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
            (coord_school_no, coord_fac_no, coord_from_date, coord_to_date))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error: {err}")

    conn.close()


def update_data_coord(coord_no, coord_school_no, coord_fac_no, coord_from_date, coord_to_date):
    global username, password, db
    print("update_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE COORD SET school_no=%s, fac_no=%s, from_date=%s, to_date=%s WHERE coord_no=%s",
                       (coord_school_no, coord_fac_no, coord_from_date, coord_to_date, coord_no))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()


def delete_data_coord(coord_no):
    global username, password, db
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM COORD WHERE coord_no=%s",
                       (coord_no,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror(title="Error:", message="You cannot delete that has records dependent on it...\n")
    finally:
        conn.close()


def delete_record_coord():
    selected_item = coord_treeview.selection()
    if selected_item:
        delete_data_coord(coord_treeview.item(selected_item)['values'][0])
        clear_entries_coord()
        populate_table_coord()
    else:
        messagebox.showerror("Error", "Please select a record to delete.")


def clear_entries_coord():
    for entry in [coord_no_entry, coord_school_no_entry, coord_fac_no_entry, coord_from_date_entry,
                  coord_to_date_entry]:
        entry.delete(0, tk.END)


def populate_table_coord():
    global username, password, db
    print("populate table called db_conn")
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    cursor.execute("""SELECT 
                    COORD.coord_no, 
                    COORD.school_no, 
                    COORD.fac_no, 
                    SCHOOL.school_name, 
                    CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname), 
                    COORD.from_date, COORD.to_date 
                    FROM COORD
                    INNER JOIN FACULTY ON COORD.fac_no = FACULTY.fac_no
                    INNER JOIN SCHOOL ON COORD.school_no = SCHOOL.school_no""")
    rows = cursor.fetchall()
    coord_treeview.delete(*coord_treeview.get_children())
    for row in rows:
        coord_treeview.insert("", "end", values=row)
    conn.close()


def add_record_coord():
    coord_school_no_value = coord_school_no_entry.get()
    coord_fac_no_value = coord_fac_no_entry.get()
    coord_from_date_value = coord_from_date_entry.get()
    coord_to_date_value = coord_to_date_entry.get()

    if coord_school_no_value and coord_fac_no_value and coord_from_date_value:
        if coord_to_date_value != "Enter To Date":
            if coord_from_date_value > coord_to_date_value:
                messagebox.showerror(title="Error", message="From Date cannot exceed To Date")
                return
        else:
            coord_to_date_value = None
        try:
            insert_data_coord(coord_school_no_value, coord_fac_no_value, coord_from_date_value, coord_to_date_value)
            print("coord inserted data")
            clear_entries_coord()
            print("coord cleared entries")
            populate_table_coord()
            print("coord populated school table")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")


def update_record_coord():
    selected_item = coord_treeview.selection()
    coord_from_date_value = coord_from_date_entry.get()
    coord_to_date_value = coord_to_date_entry.get()
    if selected_item:
        if coord_from_date_value > coord_to_date_value:
            messagebox.showerror(title="Error", message="From Date cannot exceed To Date")
            return
        else:
            try:
                update_data_coord(coord_treeview.item(selected_item)['values'][0], coord_school_no_entry.get(),
                                  coord_fac_no_entry.get(), coord_from_date_value, coord_to_date_value)
                clear_entries_coord()
                populate_table_coord()
            except mysql.connector.Error as err:
                messagebox.showerror(title="Error", message=f"{err}")
    else:
        messagebox.showerror("Error", "Please select a record to update.")


def search_coord_records(keyword):
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM COORD WHERE coord_no LIKE %s OR school_no LIKE %s OR fac_no LIKE %s OR from_date LIKE %s OR to_date LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    coord_treeview.delete(*coord_treeview.get_children())
    for row in rows:
        coord_treeview.insert("", "end", values=row)
    conn.close()


def search_coord_button_click():
    keyword = search_entry_coord.get()
    search_coord_records(keyword)


# write to csv function
def coord_write_to_csv():
    default_path = os.getcwd()
    csv_path = filedialog.asksaveasfilename(initialdir=default_path, defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if csv_path:
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(["Coordinator Number", "School Number", "Faculty Number", "School", "Full Name", "From Date", "To Date"])

                global username, password, db
                conn = db_conn(username, password, db)
                cursor = conn.cursor()
                cursor.execute("""SELECT 
                    COORD.coord_no, 
                    COORD.school_no, 
                    COORD.fac_no, 
                    SCHOOL.school_name, 
                    CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname), 
                    COORD.from_date, COORD.to_date 
                    FROM COORD
                    INNER JOIN FACULTY ON COORD.fac_no = FACULTY.fac_no
                    INNER JOIN SCHOOL ON COORD.school_no = SCHOOL.school_no""")

                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)
                conn.close()

            messagebox.showinfo(title="Write Success", message=f"Data successfully written to {csv_path}")
        except Exception as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")


def coord_sort_by(search_column, opt_ord):
    match search_column:
        case "Coordinator Number":
            search_column = "coord_no"
        case "Faculty Number":
            search_column = "fac_no"
        case "School Number":
            search_column = "school_no"
        case "From Date":
            search_column = "from_date"
        case "To Date":
            search_column = "to_date"
        case _:
            # Handle invalid search column
            messagebox.showerror(title="Error", message="Invalid search column")
            return
    print(search_column)
    global username, password, db
    try:
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        query = f""" SELECT * FROM COORD ORDER BY {search_column}"""
        if opt_ord:
            query += " DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        coord_treeview.delete(*coord_treeview.get_children())
        for row in rows:
            coord_treeview.insert("", "end", values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error {err}")


""" DEPT_FAC SECTION """


def select_item_dept_fac(event):
    selected_item = dept_fac_treeview.selection()
    dept_fac_no_entry.configure(state=NORMAL)
    if selected_item:
        values = dept_fac_treeview.item(selected_item[0], 'values')
        dept_fac_no_entry.delete(0, tk.END)
        dept_fac_no_entry.insert(0, values[0])
        dept_fac_no_entry.configure(state='readonly')
        dept_fac_fac_no_entry.delete(0, tk.END)
        dept_fac_fac_no_entry.insert(0, values[1])
        dept_fac_school_no_entry.delete(0, tk.END)
        dept_fac_school_no_entry.insert(0, values[2])
        dept_fac_from_date_entry.delete(0, tk.END)
        dept_fac_from_date_entry.insert(0, values[5])
        dept_fac_to_date_entry.delete(0, tk.END)
        dept_fac_to_date_entry.insert(0, values[6])


def insert_data_dept_fac(dept_fac_fac_no, dept_fac_school_no, dept_fac_from_date, dept_fac_to_date):
    print(dept_fac_fac_no, dept_fac_school_no, dept_fac_from_date, dept_fac_to_date)
    global username, password, db
    print("insert_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO DEPT_FAC (fac_no, school_no, from_date, to_date) VALUES (%s, %s, %s, %s)",
            (dept_fac_fac_no, dept_fac_school_no, dept_fac_from_date, dept_fac_to_date))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    except mysql.connector.Error as err:
        print(f"{err}")
        messagebox.showerror(title="Error", message=f"Error: {err}")

    conn.close()


def update_data_dept_fac(dept_fac_no, dept_fac_fac_no, dept_fac_school_no, dept_fac_from_date, dept_fac_to_date):
    global username, password, db
    print("update_data called db_conn")
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE DEPT_FAC SET fac_no=%s, school_no=%s, from_date=%s, to_date=%s WHERE dept_fac_no=%s",
                       (dept_fac_fac_no, dept_fac_school_no, dept_fac_from_date, dept_fac_to_date, dept_fac_no))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()


def delete_data_dept_fac(dept_fac_no):
    global username, password, db
    conn = db_conn(username, password, db)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DEPT_FAC WHERE dept_fac_no=%s", (dept_fac_no,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror(title="Error:", message="You cannot delete that has records dependent on it...\n")
    finally:
        conn.close()


def delete_record_dept_fac():
    selected_item = dept_fac_treeview.selection()
    if selected_item:
        delete_data_dept_fac(dept_fac_treeview.item(selected_item)['values'][0])
        clear_entries_dept_fac()
        populate_table_dept_fac()
    else:
        messagebox.showerror("Error", "Please select a record to delete.")


def clear_entries_dept_fac():
    for entry in [dept_fac_no_entry, dept_fac_fac_no_entry, dept_fac_school_no_entry, dept_fac_from_date_entry,
                  dept_fac_to_date_entry]:
        entry.delete(0, tk.END)


def populate_table_dept_fac():
    global username, password, db
    print("populate table called db_conn")
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT
                    DEPT_FAC.dept_fac_no,
                    DEPT_FAC.fac_no,
                    DEPT_FAC.school_no,
                    SCHOOL.school_name,
                    CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname) AS full_name,
                    DEPT_FAC.from_date,
                    DEPT_FAC.to_date
                    FROM DEPT_FAC
                    INNER JOIN FACULTY ON DEPT_FAC.fac_no = FACULTY.fac_no
                    INNER JOIN SCHOOL ON DEPT_FAC.school_no = SCHOOL.school_no""")
    rows = cursor.fetchall()
    dept_fac_treeview.delete(*dept_fac_treeview.get_children())
    for row in rows:
        dept_fac_treeview.insert("", "end", values=row)
    conn.close()


def add_record_dept_fac():
    dept_fac_fac_no_value = dept_fac_fac_no_entry.get()
    dept_fac_school_no = dept_fac_school_no_entry.get()
    dept_fac_from_date_value = dept_fac_from_date_entry.get()
    dept_fac_to_date_value = dept_fac_to_date_entry.get()

    if dept_fac_fac_no_value and dept_fac_school_no and dept_fac_from_date_value:
        if dept_fac_to_date_value != "Enter To Date":
            if dept_fac_from_date_value > dept_fac_to_date_value:
                messagebox.showerror(title="Error", message="From Date cannot exceed To Date")
                return
        else:
            dept_fac_to_date_value = None
        try:
            insert_data_dept_fac(dept_fac_fac_no_value, dept_fac_school_no, dept_fac_from_date_value,
                                 dept_fac_to_date_value)
            print("dept_fac inserted data")
            clear_entries_dept_fac()
            print("dept_fac cleared entries")
            populate_table_dept_fac()
            print("dept_fac populated school table")
        except mysql.connector.Error as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")


def update_record_dept_fac():
    selected_item = dept_fac_treeview.selection()
    dept_fac_from_date_value = dept_fac_from_date_entry.get()
    dept_fac_to_date_value = dept_fac_to_date_entry.get()
    if selected_item:
        if dept_fac_from_date_value > dept_fac_to_date_value:
            messagebox.showerror(title="Error", message="From Date cannot exceed To Date")
            return
        else:
            try:
                update_data_dept_fac(dept_fac_treeview.item(selected_item)['values'][0], dept_fac_fac_no_entry.get(),
                                     dept_fac_school_no_entry.get(), dept_fac_from_date_value,
                                     dept_fac_to_date_value)
                clear_entries_dept_fac()
                populate_table_dept_fac()
            except mysql.connector.Error as err:
                messagebox.showerror(title="Error", message=f"{err}")
    else:
        messagebox.showerror("Error", "Please select a record to update.")


def search_dept_fac_records(keyword):
    global username, password, db
    conn = db_conn(username, password, db)
    cursor = conn.cursor()
    query = "SELECT * FROM DEPT_FAC WHERE dept_fac_no LIKE %s OR fac_no LIKE %s OR school_no LIKE %s OR from_date LIKE %s OR to_date LIKE %s"
    cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    dept_fac_treeview.delete(*dept_fac_treeview.get_children())
    for row in rows:
        dept_fac_treeview.insert("", "end", values=row)
    conn.close()


def search_dept_fac_button_click():
    keyword = search_entry_dept_fac.get()
    search_dept_fac_records(keyword)


# write to csv function
def dept_fac_write_to_csv():
    default_path = os.getcwd()
    csv_path = filedialog.asksaveasfilename(initialdir=default_path, defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
    if csv_path:
        try:
            with open(csv_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)

                writer.writerow(
                    ["Department Faculty Number", "Faculty Number", "School Number", "School", "Full Name", "From Date", "To Date"])

                global username, password, db
                conn = db_conn(username, password, db)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT
                    DEPT_FAC.dept_fac_no,
                    DEPT_FAC.fac_no,
                    DEPT_FAC.school_no,
                    SCHOOL.school_name,
                    CONCAT(FACULTY.fac_fname, ' ', FACULTY.fac_lname) AS full_name,
                    DEPT_FAC.from_date,
                    DEPT_FAC.to_date
                    FROM DEPT_FAC
                    INNER JOIN FACULTY ON DEPT_FAC.fac_no = FACULTY.fac_no
                    INNER JOIN SCHOOL ON DEPT_FAC.school_no = SCHOOL.school_no""")

                rows = cursor.fetchall()
                for row in rows:
                    writer.writerow(row)
                conn.close()

            messagebox.showinfo(title="Write Success", message=f"Data successfully written to {csv_path}")
        except Exception as err:
            messagebox.showerror(title="Error", message=f"Error: {err}")


def dept_fac_sort_by(search_column, opt_ord):
    match search_column:
        case "Department Faculty Number":
            search_column = "dept_fac_no"
        case "Faculty Number":
            search_column = "fac_no"
        case "School Number":
            search_column = "school_no"
        case "From Date":
            search_column = "from_date"
        case "To Date":
            search_column = "to_date"
        case _:
            # Handle invalid search column
            messagebox.showerror(title="Error", message="Invalid search column")
            return
    print(search_column)
    global username, password, db
    try:
        conn = db_conn(username, password, db)
        cursor = conn.cursor()

        query = f"""SELECT * FROM DEPT_FAC ORDER BY {search_column}"""
        if opt_ord:
            query += " DESC"
        cursor.execute(query)
        rows = cursor.fetchall()
        dept_fac_treeview.delete(*dept_fac_treeview.get_children())
        for row in rows:
            dept_fac_treeview.insert("", "end", values=row)

        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror(title="Error", message=f"Error {err}")


# Adjusting weights for resizing behavior
root.columnconfigure(1, weight=3)  # Give more weight to the table frame
root.rowconfigure(1, weight=1)

# Faculty Search section
search_entry = tkb.Entry(faculty_options_frame, width=75)
add_placeholder_to(search_entry, "Search for Records")
search_image = Image.open("search_icon.png")
search_image = search_image.resize((12, 12))
search_icon = ImageTk.PhotoImage(search_image)
search_button = tkb.Button(faculty_options_frame, text="Search", image=search_icon, compound=tk.LEFT, command=search_button_click, padding=(1, 1)) #revised format
search_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
search_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.E)

# School Search section
search_entry_school = tkb.Entry(school_options_frame, width=75)
add_placeholder_to(search_entry_school, "Search for Records")
search_image_school = Image.open("search_icon.png")
search_image_school = search_image_school.resize((12, 12))
search_icon_school = ImageTk.PhotoImage(search_image_school)
search_school_button = tkb.Button(school_options_frame, text="Search", image=search_icon, compound=tk.LEFT, command=search_button_click, padding=(1, 1))
search_entry_school.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_school_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.E)

# Payroll Search section
search_entry_payroll = tkb.Entry(payroll_options_frame, width=75)
add_placeholder_to(search_entry_payroll, "Search for Records")
search_image_payroll = Image.open("search_icon.png")
search_image_payroll = search_image_payroll.resize((12, 12))
search_icon_payroll = ImageTk.PhotoImage(search_image_payroll)
search_payroll_button = tkb.Button(payroll_options_frame, text="Search", image=search_icon, compound=tk.LEFT, command=search_button_click, padding=(1, 1))
search_entry_payroll.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_payroll_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.E)

# Positions Search section
search_entry_positions = tkb.Entry(positions_options_frame, width=75)
add_placeholder_to(search_entry_positions, "Search for Records")
search_image_positions = Image.open("search_icon.png")
search_image_positions = search_image_positions.resize((12, 12))
search_icon_positions = ImageTk.PhotoImage(search_image_positions)
search_positions_button = tkb.Button(positions_options_frame, text="Search", image=search_icon, compound=tk.LEFT, command=search_button_click, padding=(1, 1))
search_entry_positions.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_positions_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.E)

# Coord Search section
search_entry_coord = tkb.Entry(coord_options_frame, width=75)
add_placeholder_to(search_entry_coord, "Search for Records")
search_image_coord = Image.open("search_icon.png")
search_image_coord = search_image_coord.resize((12, 12))
search_icon_coord = ImageTk.PhotoImage(search_image_coord)
search_coord_button = tkb.Button(coord_options_frame, text="Search", image=search_icon, compound=tk.LEFT, command=search_button_click, padding=(1, 1))
search_entry_coord.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_coord_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.E)

# Dept_Fac Search section
search_entry_dept_fac = tkb.Entry(dept_fac_options_frame, width=75)
add_placeholder_to(search_entry_dept_fac, "Search for Records")
search_image_dept_fac = Image.open("search_icon.png")
search_image_dept_fac = search_image_dept_fac.resize((12, 12))
search_icon_dept_fac = ImageTk.PhotoImage(search_image_dept_fac)
search_dept_fac_button = tkb.Button(dept_fac_options_frame, text="Search", image=search_icon, compound=tk.LEFT, command=search_button_click, padding=(1, 1))
search_entry_dept_fac.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_dept_fac_button.grid(row=0, column=1, padx=(0, 10), sticky=tk.E)

# Sort Section
# Faculty Sort
faculty_sort_entry = tkb.Combobox(faculty_options_frame, width=75)
faculty_sort_entry['values'] = ('Faculty Number', "Last Name", "First Name", "Birth Date", "Hire Date")
faculty_sort_entry.set("Sort by: ")
faculty_sort_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)

faculty_sort_desc_var = tk.BooleanVar()  # Variable to store the state of the Checkbutton
faculty_sort_desc = tkb.Checkbutton(faculty_options_frame, text="Desc", variable=faculty_sort_desc_var,
                                    bootstyle="info-round-toggle")
faculty_sort_desc.grid(row=1, column=1, padx=(0, 10), sticky=tk.E)

faculty_sort_button = tkb.Button(faculty_options_frame, text="Go",
                                 command=lambda: faculty_sort_by(faculty_sort_entry.get(), faculty_sort_desc_var.get()),
                                 padding=(1, 1))
faculty_sort_button.grid(row=1, column=2, padx=(0, 10), sticky=tk.E)

# School Sort
school_sort_entry = tkb.Combobox(school_options_frame, width=75)
school_sort_entry['values'] = ("School Number", "School Name")
school_sort_entry.set("Sort by: ")
school_sort_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)

school_sort_desc_var = tk.BooleanVar()  # Variable to store the state of the Checkbutton
school_sort_desc = tkb.Checkbutton(school_options_frame, text="Desc", variable=school_sort_desc_var,
                                   bootstyle="info-round-toggle")
school_sort_desc.grid(row=1, column=1, padx=(0, 10), sticky=tk.E)

school_sort_button = tkb.Button(school_options_frame, text="Go", command=lambda: school_sort_by(
    school_sort_entry.get(), school_sort_desc_var.get()), padding=(1, 1))
school_sort_button.grid(row=1, column=2, padx=(0, 10), sticky=tk.E)

# Payroll Sort
payroll_sort_entry = tkb.Combobox(payroll_options_frame, width=75)
payroll_sort_entry['values'] = ("Payroll Number", 'Faculty Number', "Pay Amount", "From Date", "To Date")
payroll_sort_entry.set("Sort by: ")
payroll_sort_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)

payroll_sort_desc_var = tk.BooleanVar()  # Variable to store the state of the Checkbutton
payroll_sort_desc = tkb.Checkbutton(payroll_options_frame, text="Desc", variable=payroll_sort_desc_var,
                                    bootstyle="info-round-toggle")
payroll_sort_desc.grid(row=1, column=1, padx=(0, 10), sticky=tk.E)

payroll_sort_button = tkb.Button(payroll_options_frame, text="Go", command=lambda: payroll_sort_by(
    payroll_sort_entry.get(), payroll_sort_desc_var.get()), padding=(1, 1))
payroll_sort_button.grid(row=1, column=2, padx=(0, 10), sticky=tk.E)

# Positions Sort
positions_sort_entry = tkb.Combobox(positions_options_frame, width=75)
positions_sort_entry['values'] = ("Position Number", 'Faculty Number', "Position", "From Date", "To Date")
positions_sort_entry.set("Sort by: ")
positions_sort_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)

positions_sort_desc_var = tk.BooleanVar()  # Variable to store the state of the Checkbutton
positions_sort_desc = tkb.Checkbutton(positions_options_frame, text="Desc", variable=positions_sort_desc_var,
                                      bootstyle="info-round-toggle")
positions_sort_desc.grid(row=1, column=1, padx=(0, 10), sticky=tk.E)

positions_sort_button = tkb.Button(positions_options_frame, text="Go", command=lambda: positions_sort_by(
    positions_sort_entry.get(), positions_sort_desc_var.get()), padding=(1, 1))
positions_sort_button.grid(row=1, column=2, padx=(0, 10), sticky=tk.E)

# Coord Sort
coord_sort_entry = tkb.Combobox(coord_options_frame, width=75)
coord_sort_entry['values'] = ("Coordinator Number", "School Number", 'Faculty Number', "From Date", "To Date")
coord_sort_entry.set("Sort by: ")
coord_sort_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)

coord_sort_desc_var = tk.BooleanVar()  # Variable to store the state of the Checkbutton
coord_sort_desc = tkb.Checkbutton(coord_options_frame, text="Desc", variable=coord_sort_desc_var,
                                  bootstyle="info-round-toggle")
coord_sort_desc.grid(row=1, column=1, padx=(0, 10), sticky=tk.E)

coord_sort_button = tkb.Button(coord_options_frame, text="Go", command=lambda: coord_sort_by(
    coord_sort_entry.get(), coord_sort_desc_var.get()), padding=(1, 1))
coord_sort_button.grid(row=1, column=2, padx=(0, 10), sticky=tk.E)

# Dept_fac Sort
dept_fac_sort_entry = tkb.Combobox(dept_fac_options_frame, width=75)
dept_fac_sort_entry['values'] = (
    "Department Faculty Number", 'Faculty Number', "Last Name", "First Name", "Birth Date", "Hire Date")
dept_fac_sort_entry.set("Sort by: ")
dept_fac_sort_entry.grid(row=1, column=0, padx=(0, 10), sticky=tk.W)

# Variable to store the state of the Checkbutton
dept_fac_sort_desc_var = tk.BooleanVar()
dept_fac_sort_desc = tkb.Checkbutton(
    dept_fac_options_frame, text="Desc", variable=dept_fac_sort_desc_var, bootstyle="info-round-toggle")
dept_fac_sort_desc.grid(row=1, column=1, padx=(0, 10), sticky=tk.E)

dept_fac_sort_button = tkb.Button(
    dept_fac_options_frame, text="Go",
    command=lambda: dept_fac_sort_by(dept_fac_sort_entry.get(), dept_fac_sort_desc_var.get()), padding=(1, 1))
dept_fac_sort_button.grid(row=1, column=2, padx=(0, 10), sticky=tk.E)

# School Tab Content
school_info_header = tkb.Label(school_frame, text="Simple CRUD", font=("Times New Roman", 25, "bold", "underline"))
school_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

# School CRUD section with entries and labels below them
school_crud_info_label = tkb.LabelFrame(school_frame, text="SCHOOL INFORMATION", borderwidth=2)
school_crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# CRUD section with entries and labels below them
school_crud_section = tkb.Frame(school_crud_info_label, padding=10)
school_crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# CRUD Information Section
crud_info_header = tkb.Label(faculty_frame, text="Simple CRUD", font=("Times New Roman", 25, "bold", "underline"))
crud_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

# CRUD section with entries and labels below them
crud_info_label = tkb.LabelFrame(faculty_frame, text="FACULTY INFORMATION", borderwidth=2, bootstyle="info")
crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# CRUD section with entries and labels below them
crud_section = tkb.Frame(crud_info_label, padding=10)
crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# Payroll Tab Content (replicated from Faculty Tab)
payroll_info_header = tkb.Label(payroll_frame, text="Simple CRUD", font=("Times New Roman", 25, "bold", "underline"))
payroll_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

payroll_crud_info_label = tkb.LabelFrame(payroll_frame, text="PAYROLL INFORMATION", borderwidth=2)
payroll_crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

payroll_crud_section = tkb.Frame(payroll_crud_info_label, padding=10)
payroll_crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# Positions Tab Content (replicated from Faculty Tab)
positions_info_header = tkb.Label(positions_frame, text="Simple CRUD",
                                  font=("Times New Roman", 25, "bold", "underline"))
positions_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

positions_crud_info_label = tkb.LabelFrame(positions_frame, text="POSITIONS INFORMATION", borderwidth=2)
positions_crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

positions_crud_section = tkb.Frame(positions_crud_info_label, padding=10)
positions_crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# Coordinators Tab Content (replicated from Faculty Tab)
coord_info_header = tkb.Label(coord_frame, text="Simple CRUD", font=("Times New Roman", 25, "bold", "underline"))
coord_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

coord_crud_info_label = tkb.LabelFrame(coord_frame, text="COORD INFORMATION", borderwidth=2)
coord_crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

coord_crud_section = tkb.Frame(coord_crud_info_label, padding=10)
coord_crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# Department Faculties Tab Content (replicated from Faculty Tab)
dept_fac_info_header = tkb.Label(dept_fac_frame, text="Simple CRUD", font=("Times New Roman", 25, "bold", "underline"))
dept_fac_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

dept_fac_crud_info_label = tkb.LabelFrame(dept_fac_frame, text="DEPT_FAC INFORMATION", borderwidth=2)
dept_fac_crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

dept_fac_crud_section = tkb.Frame(dept_fac_crud_info_label, padding=10)
dept_fac_crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

# Labels and entries for School
school_labels = ["School Number", "School Name"]
school_entries = []
for i, label_text in enumerate(school_labels):
    label = tkb.Label(school_crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2 * i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(school_crud_section, width=50)
    entry.grid(row=2 * i + 1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    school_entries.append(entry)

school_no_entry, school_name_entry = school_entries
add_placeholder_to(school_no_entry, "Enter School Number")
add_placeholder_to(school_name_entry, "Enter School Name")


# Labels and entries for Faculty
labels = ["Faculty Number", "Last Name", "First Name", "Birth Date", "Hire Date"]
entries = []
for i, label_text in enumerate(labels):
    label = tkb.Label(crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2 * i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(crud_section, width=50)
    entry.grid(row=2 * i + 1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    entries.append(entry)

fac_no_entry, fac_lname_entry, fac_fname_entry, birth_date_entry, hire_date_entry = entries
add_placeholder_to(fac_no_entry, "Enter Faculty Number")
add_placeholder_to(fac_lname_entry, "Enter Last Name")
add_placeholder_to(fac_fname_entry, "Enter First Name")
add_placeholder_to(birth_date_entry, "YYYY-MM-DD")
add_placeholder_to(hire_date_entry, "YYYY-MM-DD")

# Labels and entries for Payroll
payroll_labels = ["Payroll Number", "Faculty Number", "Pay Amount", "From Date", "To Date"]
payroll_entries = []
for i, label_text in enumerate(payroll_labels):
    label = tkb.Label(payroll_crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2 * i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(payroll_crud_section, width=50)
    entry.grid(row=2 * i + 1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    payroll_entries.append(entry)

payroll_no_entry, payroll_fac_no_entry, payroll_pay_amount_entry, payroll_from_date_entry, payroll_to_date_entry = payroll_entries
add_placeholder_to(payroll_fac_no_entry, "Enter Faculty Number")
add_placeholder_to(payroll_pay_amount_entry, "Enter Pay Amount")
add_placeholder_to(payroll_from_date_entry, "YYYY-MM-DD")
add_placeholder_to(payroll_to_date_entry, "YYYY-MM-DD")

# labels and entries for Positions
positions_labels = ["Position Number", "Faculty Number", "Position", "From Date", "To Date"]
positions_entries = []
for i, label_text in enumerate(positions_labels):
    label = tkb.Label(positions_crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2 * i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(positions_crud_section, width=50)
    entry.grid(row=2 * i + 1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    positions_entries.append(entry)

positions_no_entry, positions_fac_no_entry, positions_position_entry, positions_from_date_entry, positions_to_date_entry = positions_entries
add_placeholder_to(positions_fac_no_entry, "Enter Faculty Number")
add_placeholder_to(positions_position_entry, "Enter Position")
add_placeholder_to(positions_from_date_entry, "YYYY-MM-DD")
add_placeholder_to(positions_to_date_entry, "YYYY-MM-DD")

# labels and entries for Coordinators
coord_labels = ["Coordinator Number", "School Number", "Faculty Number", "From Date", "To Date"]
coord_entries = []
for i, label_text in enumerate(coord_labels):
    label = tkb.Label(coord_crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2 * i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(coord_crud_section, width=50)
    entry.grid(row=2 * i + 1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    coord_entries.append(entry)

coord_no_entry, coord_school_no_entry, coord_fac_no_entry, coord_from_date_entry, coord_to_date_entry = coord_entries
add_placeholder_to(coord_school_no_entry, "Enter School Number")
add_placeholder_to(coord_fac_no_entry, "Enter Faculty Number")
add_placeholder_to(coord_from_date_entry, "YYYY-MM-DD")
add_placeholder_to(coord_to_date_entry, "YYYY-MM-DD")

# Labels and entries for Faculty
dept_fac_labels = ["Department Faculty Number", "Faculty Number", "School Number", "From Date", "To Date"]
dept_fac_entries = []
for i, label_text in enumerate(dept_fac_labels):
    label = tkb.Label(dept_fac_crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2 * i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = tkb.Entry(dept_fac_crud_section, width=50)
    entry.grid(row=2 * i + 1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    dept_fac_entries.append(entry)

dept_fac_no_entry, dept_fac_fac_no_entry, dept_fac_school_no_entry, dept_fac_from_date_entry, dept_fac_to_date_entry = dept_fac_entries
add_placeholder_to(dept_fac_fac_no_entry, "Enter Faculty Number")
add_placeholder_to(dept_fac_school_no_entry, "Enter School Number")
add_placeholder_to(dept_fac_from_date_entry, "YYYY-MM-DD")
add_placeholder_to(dept_fac_to_date_entry, "YYYY-MM-DD")

fac_no_entry.configure(bootstyle="warning")
school_no_entry.configure(bootstyle="warning")
payroll_no_entry.configure(bootstyle="warning", state='readonly')
positions_no_entry.configure(bootstyle="warning", state='readonly')
coord_no_entry.configure(bootstyle="warning", state='readonly')
dept_fac_no_entry.configure(bootstyle="warning", state='readonly')

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

write_csv_image = Image.open("write_csv.png")
write_csv_image = write_csv_image.resize((20, 20))
write_csv_icon = ImageTk.PhotoImage(write_csv_image)

save_db_image = Image.open("save_db.png")
save_db_image = save_db_image.resize((20, 20))
save_db_icon = ImageTk.PhotoImage(save_db_image)

# Buttons for CRUD operations
button_icons = [add_icon, update_icon, delete_icon, write_csv_icon, save_db_icon]
button_texts = ["Add", "Update", "Delete", "Write CSV", "Save DB"]

school_button_icons = [add_icon, update_icon, delete_icon, write_csv_icon, save_db_icon]
school_button_texts = ["Add", "Update", "Delete", "Write CSV", "Save DB"]

payroll_button_icons = [add_icon, update_icon, delete_icon, write_csv_icon, save_db_icon]
payroll_button_texts = ["Add", "Update", "Delete", "Write CSV", "Save DB"]

positions_button_icons = [add_icon, update_icon, delete_icon, write_csv_icon, save_db_icon]
positions_button_texts = ["Add", "Update", "Delete", "Write CSV", "Save DB"]

coord_button_icons = [add_icon, update_icon, delete_icon, write_csv_icon, save_db_icon]
coord_button_texts = ["Add", "Update", "Delete", "Write CSV", "Save DB"]

dept_fac_button_icons = [add_icon, update_icon, delete_icon, write_csv_icon, save_db_icon]
dept_fac_button_texts = ["Add", "Update", "Delete", "Write CSV", "Save DB"]

commands = [add_record, update_record, delete_record, faculty_write_to_csv, backup_db]
school_commands = [add_record_school, update_record_school, delete_record_school, school_write_to_csv, backup_db]
payroll_commands = [add_record_payroll, update_record_payroll, delete_record_payroll, payroll_write_to_csv, backup_db]
positions_commands = [add_record_positions, update_record_positions, delete_record_positions, positions_write_to_csv,
                      backup_db]
coord_commands = [add_record_coord, update_record_coord, delete_record_coord, coord_write_to_csv, backup_db]
dept_fac_commands = [add_record_dept_fac, update_record_dept_fac, delete_record_dept_fac, dept_fac_write_to_csv,
                     backup_db]

buttons_frame = tkb.Frame(crud_info_label, padding=10)
buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

school_buttons_frame = tkb.Frame(school_crud_info_label, padding=10)
school_buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

payroll_buttons_frame = tkb.Frame(payroll_crud_info_label, padding=10)
payroll_buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

positions_buttons_frame = tkb.Frame(positions_crud_info_label, padding=10)
positions_buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

coord_buttons_frame = tkb.Frame(coord_crud_info_label, padding=10)
coord_buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

dept_fac_buttons_frame = tkb.Frame(dept_fac_crud_info_label, padding=10)
dept_fac_buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))

for i, (text, icon, cmd) in enumerate(zip(button_texts, button_icons, commands)):
    # Ensure that the image object is retained to prevent garbage collection
    button = tkb.Button(buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.image = icon  # Retain the image object by assigning it to a property of the button
    button.grid(row=0, column=i, padx=5)

for i, (text, icon, cmd) in enumerate(zip(school_button_texts, school_button_icons, school_commands)):
    button = tkb.Button(school_buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.image = icon  # Retain the image object by assigning it to a property of the button
    button.grid(row=0, column=i, padx=5)

for i, (text, icon, cmd) in enumerate(zip(payroll_button_texts, payroll_button_icons, payroll_commands)):
    button = tkb.Button(payroll_buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.image = icon  # Retain the image object by assigning it to a property of the button
    button.grid(row=0, column=i, padx=5)

for i, (text, icon, cmd) in enumerate(zip(positions_button_texts, positions_button_icons, positions_commands)):
    button = tkb.Button(positions_buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.image = icon  # Retain the image object by assigning it to a property of the button
    button.grid(row=0, column=i, padx=5)

for i, (text, icon, cmd) in enumerate(zip(coord_button_texts, coord_button_icons, coord_commands)):
    button = tkb.Button(coord_buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.image = icon  # Retain the image object by assigning it to a property of the button
    button.grid(row=0, column=i, padx=5)

for i, (text, icon, cmd) in enumerate(zip(dept_fac_button_texts, dept_fac_button_icons, dept_fac_commands)):
    button = tkb.Button(dept_fac_buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.image = icon  # Retain the image object by assigning it to a property of the button
    button.grid(row=0, column=i, padx=5)

# Treeview for displaying data
treeview = tkb.Treeview(table_frame, columns=("Faculty Number", "Last Name", "First Name", "Birthday", "Hire Date"),
                        show="headings", bootstyle="info")
for col in treeview["columns"]:
    treeview.heading(col, text=col)
    treeview.column(col, anchor=tk.W)
treeview.column("Faculty Number", width=40)
treeview.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Treeview for displaying data for School
school_treeview = tkb.Treeview(school_table_frame, columns=("School Number", "School Name"), show="headings",
                               bootstyle="info")
for col in school_treeview["columns"]:
    school_treeview.heading(col, text=col)
    school_treeview.column(col, anchor=tk.W)
school_treeview.column("School Number", width=50)
school_treeview.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Treeview for displaying data for Payroll
payroll_treeview = tkb.Treeview(payroll_table_frame,
                                columns=("Payroll Number", "Faculty Number", "Full Name", "Pay Amount", "From Date", "To Date"),
                                show="headings", bootstyle="info")
for col in payroll_treeview["columns"]:
    payroll_treeview.heading(col, text=col)
    payroll_treeview.column(col, anchor=tk.W, stretch=NO)
payroll_treeview.column("Payroll Number", width=40)
payroll_treeview.column("Faculty Number", width=40)
payroll_treeview.grid(row=2, column=0)

positions_treeview = tkb.Treeview(positions_table_frame,
                                  columns=("Position Number", "Faculty Number", "Full Name", "Position", "From Date", "To Date"),
                                  show="headings", bootstyle="info")
for col in positions_treeview["columns"]:
    positions_treeview.heading(col, text=col)
    positions_treeview.column(col, anchor=tk.W)
positions_treeview.column("Position Number", width=40)
positions_treeview.column("Faculty Number", width=40)
positions_treeview.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

coord_treeview = tkb.Treeview(coord_table_frame,
                              columns=("Coordinator Number", "School Number", "Faculty Number", "School", "Full Name", "From Date", "To Date"),
                              show="headings", bootstyle="info")
for col in coord_treeview["columns"]:
    coord_treeview.heading(col, text=col)
    coord_treeview.column(col, anchor=tk.W, width=150)
coord_treeview.column("School Number", width=50)
coord_treeview.column("Coordinator Number", width=40)
coord_treeview.column("Faculty Number", width=40)


coord_treeview.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

dept_fac_treeview = tkb.Treeview(dept_fac_table_frame, columns=(
"Department Faculty Number", "Faculty Number", "School Number", "School", "Full Name", "From Date", "To Date"), show="headings",
                                 bootstyle="info")
for col in dept_fac_treeview["columns"]:
    dept_fac_treeview.heading(col, text=col)
    dept_fac_treeview.column(col, anchor=tk.W, width=150)
dept_fac_treeview.column("Faculty Number", width=40)
dept_fac_treeview.column("Department Faculty Number", width=40)
dept_fac_treeview.column("School Number", width=50)

dept_fac_treeview.grid(row=2, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Bind select event
treeview.bind('<<TreeviewSelect>>', select_item)
school_treeview.bind('<<TreeviewSelect>>', select_item_school)
payroll_treeview.bind('<<TreeviewSelect>>', select_item_payroll)
positions_treeview.bind('<<TreeviewSelect>>', select_item_positions)
coord_treeview.bind('<<TreeviewSelect>>', select_item_coord)
dept_fac_treeview.bind('<<TreeviewSelect>>', select_item_dept_fac)

crud_notebook.bind("<<NotebookTabChanged>>", on_tab_change)

root.mainloop()