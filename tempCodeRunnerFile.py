import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
from sqlite3 import Error
from sqlite3.dbapi2 import Connection
from PIL import Image, ImageTk

current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

def connect_db():
    conn = sqlite3.connect("users.db")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        surname TEXT,
                        email TEXT,
                        address TEXT,
                        contact_no TEXT
                    )""")
    conn.commit()
    conn.close()

def insert_data(id, surname, email, address, contact_no):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, surname, email, address, contact_no) VALUES (?, ?, ?, ?, ?)",
                       (id, surname, email, address, contact_no))
        conn.commit()
        messagebox.showinfo("Success", "Record added successfully!")
    finally:
        conn.close()

def update_data(id, surname, email, address, contact_no):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET surname=?, email=?, address=?, contact_no=? WHERE id=?",
                       (surname, email, address, contact_no, id))
        conn.commit()
        messagebox.showinfo("Success", "Record updated successfully!")
    finally:
        conn.close()

def delete_data(id):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (id,))
        conn.commit()
        messagebox.showinfo("Success", "Record deleted successfully!")
    finally:
        conn.close()

def clear_entries():
    for entry in [id_entry, surname_entry, email_entry, address_entry, contact_no_entry]:
        entry.delete(0, tk.END)

def populate_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", "end", values=row)
    conn.close()

def add_record():
    id_value = id_entry.get()
    surname_value = surname_entry.get()
    email_value = email_entry.get()
    address_value = address_entry.get()
    contact_no_value = contact_no_entry.get()
    
    if id_value and surname_value and email_value and address_value and contact_no_value:
        try:
            insert_data(id_value, surname_value, email_value, address_value, contact_no_value)
            clear_entries()
            populate_table()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Duplicate record. ID already exists.")
    else:
        messagebox.showerror("Error", "All fields must be filled out.")

def update_record():
    selected_item = treeview.selection()
    if selected_item:
        update_data(treeview.item(selected_item)['values'][0],
                    surname_entry.get(), email_entry.get(), address_entry.get(), contact_no_entry.get())
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
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE surname LIKE ? OR email LIKE ? OR address LIKE ? OR contact_no LIKE ?"
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
        values = treeview.item(selected_item, 'values')
        id_entry.delete(0, tk.END)
        id_entry.insert(0, values[0])
        surname_entry.delete(0, tk.END)
        surname_entry.insert(0, values[1])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[2])
        address_entry.delete(0, tk.END)
        address_entry.insert(0, values[3])
        contact_no_entry.delete(0, tk.END)
        contact_no_entry.insert(0, values[4])

def add_placeholder_to(entry: tk.Entry, placeholder: str, color='grey'):
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)

    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

root = tk.Tk()
root.title("CRUD Application")
root.geometry("1600x600")  # Adjust the initial size of the window

style = ttk.Style(root)
style.theme_use('clam')  # Using a more modern theme

# Frames for organization
crud_frame = ttk.Frame(root, padding="90 0 0 10")
crud_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

table_frame = ttk.Frame(root, padding="0 70 10 10")
table_frame.grid(row=1, column=1, sticky=(tk.N, tk.W, tk.E, tk.S))

# Adjusting weights for resizing behavior
root.columnconfigure(1, weight=3)  # Give more weight to the table frame
root.rowconfigure(1, weight=1)

# Search section
search_entry = ttk.Entry(table_frame, width=35)
add_placeholder_to(search_entry, "Search for Records")
search_image = Image.open("search_icon.png")  # Provide the correct path to your image file
search_image = search_image.resize((12, 12))
search_icon = ImageTk.PhotoImage(search_image)
search_button = ttk.Button(table_frame, image=search_icon, compound=tk.LEFT, command=search_button_click,padding=(1,1))
search_entry.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)
search_button.grid(row=0, column=0, padx=(0, 10), sticky=tk.E)

# CRUD Information Section
crud_info_header = ttk.Label(crud_frame, text="CRUD Application", font=("Times New Roman", 25, "bold"))
crud_info_header.grid(row=0, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E))

# CRUD section with entries and labels below them
crud_info_label = ttk.LabelFrame(crud_frame, text="INFORMATION", borderwidth=2)
crud_info_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# CRUD section with entries and labels below them
crud_section = ttk.Frame(crud_info_label, padding=10)
crud_section.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.W, tk.E, tk.S))

labels = ["ID", "Surname", "Email", "Address", "Contact No"]
entries = []
for i, label_text in enumerate(labels):
    label = ttk.Label(crud_section, text=f"{label_text}:", font=('Helvetica', 10))
    label.grid(row=2*i, column=0, padx=5, pady=2, sticky=(tk.W))
    entry = ttk.Entry(crud_section, width=50)
    entry.grid(row=2*i+1, column=0, padx=5, pady=2, sticky=(tk.W, tk.E))
    entries.append(entry)
    
id_entry, surname_entry, email_entry, address_entry, contact_no_entry = entries
add_placeholder_to(id_entry, "Enter ID number")
add_placeholder_to(surname_entry, "Enter surname")
add_placeholder_to(email_entry, "Enter email address")
add_placeholder_to(address_entry, "Enter address")
add_placeholder_to(contact_no_entry, "Enter contact number")

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
buttons_frame = ttk.Frame(crud_info_label, padding=10)
buttons_frame.grid(row=12, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
for i, (text, icon, cmd) in enumerate(zip(button_texts, button_icons, commands)):
    button = ttk.Button(buttons_frame, text=text, image=icon, compound=tk.LEFT, command=cmd)
    button.grid(row=0, column=i, padx=5)

# Treeview for displaying data
treeview = ttk.Treeview(table_frame, columns=("ID", "Surname", "Email", "Address", "Contact No"), show="headings")
for col in treeview["columns"]:
    treeview.heading(col, text=col)
    treeview.column(col, anchor=tk.W)
treeview.column("ID", width=40)
treeview.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Bind select event
treeview.bind('<<TreeviewSelect>>', select_item)

# Initialize database and populate table
create_table()
populate_table()

root.mainloop()
