import os
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter.filedialog import askopenfilename

def open_file():
    """Открываем файл для редактирования"""
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

def insert_all(tree, id_p, node):
    i = 0
    for item in node:
        if isinstance(item, dict) and isinstance(node, list):
            "List_of_dicts"
            id = tree.insert(id_p, 'end', text=str(i) + ': {' + str(len(item.values())) + '}')
            insert_all(tree, id, item)
        elif not isinstance(item, (dict, list)) and isinstance(node, list):
            "List"
            if isinstance(item, str):
                tree.insert(id_p, 'end', text=f'{str(i)}: "{item}"')
            else:
                tree.insert(id_p, 'end', text=f'{str(i)}: {item}')
        elif isinstance(item, str) and isinstance(node[item], list):
            "Dict_of_lists"
            id = tree.insert(id_p, 'end', text=item + ': [' + str(len(node[item])) + ']')
            insert_all(tree, id, node[item])
        elif isinstance(item, str) and isinstance(node, dict) \
                and isinstance(node.get(item), dict):
            "Dict_of_named_dicts"
            id = tree.insert(id_p, 'end', text=item + ': {' + str(len(node.get(item))) + '}')
            insert_all(tree, id, node.get(item))
        elif isinstance(item, str) and not isinstance(node.get(item), (dict, list)) \
                and isinstance(node, dict):
            "Scalar"
            if isinstance(node.get(item), str):
                tmp = f'{item}: "{node.get(item)}"'
            else:
                tmp = f'{item}: {node.get(item)}'
            tree.insert(id_p, 'end', text=tmp)
        else:
            "Empty_value"
            if isinstance(item, str):
                tree.insert(id_p, 'end', text=f'{str(i)}: "{item}"')
            else:
                tree.insert(id_p, 'end', text=f'{str(i)}: {item}')
        i += 1
    pass


def run_treeview():
    lbl_errorfield.config(text="Tree View")
    with open(ent_filename.get(), "r") as input_file:
        valid_data = json.load(input_file)

    tree_window = Tk()
    tree_window.title("Tree View")
    tree_window.geometry("800x235")

    tree = ttk.Treeview(tree_window)
    tree.column("#0", minwidth=0, width=785)
    tree.heading("#0", text=ent_filename.get(), anchor=tk.W)
    ysb = ttk.Scrollbar(tree_window, orient=tk.VERTICAL,
                        command=tree.yview)
    xsb = ttk.Scrollbar(tree_window, orient=tk.HORIZONTAL,
                        command=tree.xview)
    tree.configure(yscroll=ysb.set, xscroll=xsb.set)

    tree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
    ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
    xsb.grid(row=1, column=0, sticky=tk.E + tk.W)
    tree.rowconfigure(0, weight=1)
    tree.columnconfigure(0, weight=1)

    if isinstance(valid_data, list):
        id = tree.insert('', 'end', text='[' + str(len(valid_data)) + ']')
    else:
        id = tree.insert('', 'end', text='{' + str(len(valid_data)) + '}')
    insert_all(tree, id, valid_data)

    tree_window.mainloop()
    pass

def run_tableview():
    lbl_errorfield.config(text="Table View")
    pass

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
    ent_filename = tk.Entry(left_frame, textvariable=text, width=62)
    ent_filename.insert(tk.END, os.path.abspath('.'))
    txt_edit = tk.Text(window)
    lbl_errorfield = tk.Label(left_frame, text="If some errors\n .config() this lbl")

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
