import os
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename

from table_view import table
from get_data import get_data
from tree_view import tree

def open_file():
    filepath = askopenfilename(
        filetypes=[("JSON", "*.json"), ("YAML", "*.yaml"), ("All", "*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Parser of - {filepath}")
    ent_filename.delete(0, 'end')
    ent_filename.insert(tk.END, filepath)

def run_treeview():
    valid_data = get_data(ent_filename.get())

    if not valid_data:
        lbl_errorfield.config(text="Your file is not correct")
    else:
        lbl_errorfield.config(text="Choose file and click view button")
        tree(valid_data, ent_filename.get())

def run_tableview():
    valid_data = get_data(ent_filename.get())

    if not valid_data:
        lbl_errorfield.config(text="Your file is not correct")
    else:
        lbl_errorfield.config(text="Choose file and click view button")
        table(valid_data, ent_filename.get())

if __name__ == '__main__':
    "Список тип\функция окон визуализации, можно расширять"
    views = [("Tree View", run_treeview), ("Table View", run_tableview)]

    "Создание всех элементов основного окна и привязка методом .grid к фреймам"
    window = tk.Tk()
    window.title("Parser")
    window.rowconfigure(0, minsize=600, weight=1)
    window.columnconfigure(1, minsize=600, weight=1)

    left_frame = tk.Frame(window, relief=tk.RAISED, bd=5)
    btn_open = tk.Button(left_frame, text="Choose file", command=open_file)
    text = StringVar()
    ent_filename = tk.Entry(left_frame, textvariable=text, width=50)
    ent_filename.insert(tk.END, os.path.abspath('.'))
    txt_edit = tk.Text(window)
    lbl_errorfield = tk.Label(left_frame, text="Choose file and click view button")

    row = 2
    for txt, cmd in views:
        tk.Button(left_frame, text=txt, padx=15, pady=10, command=cmd) \
            .grid(row=row, sticky="nsew")
        row += 1

    left_frame.grid(row=0, column=0, sticky="nsew")
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    ent_filename.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    lbl_errorfield.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
    txt_edit.grid(row=0, column=1, sticky="nsew")

    window.mainloop()
