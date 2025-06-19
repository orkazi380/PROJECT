import tkinter as tk
from tkinter import messagebox, ttk
import csv
import datetime
import os

DAIRY_FILE = "dairy_entries.csv"
DISPATCH_FILE = "dispatch_entries.csv"
FILE_MOVEMENT_FILE = "file_movement.csv"

def get_date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ensure_files():
    for file_name, headers in [
        (DAIRY_FILE, ["ID", "Date", "From", "Subject", "Received By", "Remarks"]),
        (DISPATCH_FILE, ["ID", "Date", "To", "Subject", "Dispatched By", "Mode", "Remarks"]),
        (FILE_MOVEMENT_FILE, ["File ID", "From Section", "To Section", "Moved By", "Date", "Remarks"])
    ]:
        if not os.path.exists(file_name):
            with open(file_name, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)

def save_entry(file_name, fields):
    with open(file_name, 'a', newline='') as f:
        csv.writer(f).writerow(fields)
    messagebox.showinfo("Success", "Entry added successfully!")

def create_form(root, labels, file_name, extra_date=True):
    form = tk.Toplevel(root)
    form.title("Add Entry")

    entries = []
    for label_text in labels:
        row = tk.Frame(form)
        row.pack(padx=10, pady=5, fill="x")
        tk.Label(row, text=label_text, width=20, anchor='w').pack(side="left")
        entry = tk.Entry(row)
        entry.pack(side="right", expand=True, fill="x")
        entries.append(entry)

    def submit():
        values = [e.get() for e in entries]
        if extra_date:
            values.insert(1, get_date())
        if all(values):
            save_entry(file_name, values)
            form.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")

    tk.Button(form, text="Submit", command=submit).pack(pady=10)

def view_records(file_name):
    viewer = tk.Toplevel()
    viewer.title("View Records")

    tree = ttk.Treeview(viewer)
    tree.pack(expand=True, fill='both')

    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            tree["columns"] = headers
            for h in headers:
                tree.heading(h, text=h)
                tree.column(h, width=100)
            for row in reader:
                tree.insert("", "end", values=row)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")

def main_gui():
    ensure_files()
    root = tk.Tk()
    root.title("Mail & File Management System")
    root.geometry("500x400")

    tk.Label(root, text="Official Mail & File Management System", font=("Helvetica", 16)).pack(pady=20)

    actions = [
        ("Add Dairy Entry", lambda: create_form(root,
            ["ID", "From", "Subject", "Received By", "Remarks"], DAIRY_FILE)),
        ("Add Dispatch Entry", lambda: create_form(root,
            ["ID", "To", "Subject", "Dispatched By", "Mode", "Remarks"], DISPATCH_FILE)),
        ("Track File Movement", lambda: create_form(root,
            ["File ID", "From Section", "To Section", "Moved By", "Remarks"], FILE_MOVEMENT_FILE)),
        ("View Dairy Records", lambda: view_records(DAIRY_FILE)),
        ("View Dispatch Records", lambda: view_records(DISPATCH_FILE)),
        ("View File Movement Records", lambda: view_records(FILE_MOVEMENT_FILE)),
    ]

    for text, cmd in actions:
        tk.Button(root, text=text, width=40, command=cmd).pack(pady=5)

    tk.Button(root, text="Exit", width=40, command=root.destroy).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_gui()