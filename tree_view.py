import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

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


def tree(valid_data, filename):
    tree_window = Tk()
    tree_window.title(f"Tree View")
    tree_window.geometry("800x235")

    tree = ttk.Treeview(tree_window)
    tree.column("#0", minwidth=0, width=785)
    tree.heading("#0", text=filename, anchor=tk.W)
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
