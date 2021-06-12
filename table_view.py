import tkinter as tk
import tkinter.ttk as ttk

class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"]=headings
        table["displaycolumns"]=headings
    
        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER, minwidth=0, width=(785//len(headings)))
        
        for row in rows:
            table.insert('', tk.END, values=tuple(row))
        
        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

def get_head(valid_data, dict_of_dict):
    head = ["", ]
    if dict_of_dict:
        for dct in valid_data.values():
            for key in dct:
                if key not in head:
                    head.append(key)
    else:
        for dct in valid_data:
            for key in dct:
                if key not in head:
                    head.append(key)
    return tuple(head)

def get_rows(valid_data, headings, dict_of_dict):
    rows = []

    if dict_of_dict:
        first_col = list(valid_data.keys())
        i = 0
        for dct in valid_data.values():
            row = []
            row.append(first_col[i])
            i += 1
            j = 0
            for key, value in dct.items():
                j += 1
                while key != headings[j]:
                    row.append("")
                    j += 1
                if isinstance(value, str):
                    row.append('"' + value + '"')
                else:
                    row.append(value)
            rows.append(tuple(row))
    else:
        i = 0
        for dct in valid_data:
            row = [i, ]
            i += 1
            j = 0
            for key, value in dct.items():
                j += 1
                while key != headings[j]:
                    row.append("")
                    j += 1
                if isinstance(value, str):
                    row.append('"' + value + '"')
                else:
                    row.append(value)
            rows.append(tuple(row))
    return tuple(rows)

def table(valid_data, filename):
    headings = ()
    rows = []

    dict_of_dict = False
    try:
        for key, value in valid_data.items():
            if isinstance(value, dict):
                dict_of_dict = True
    except AttributeError:
        pass

    if dict_of_dict:
        headings = get_head(valid_data, dict_of_dict)
        rows = get_rows(valid_data, headings, dict_of_dict)
    elif isinstance(valid_data, list) and valid_data \
            and isinstance(valid_data[0], dict):
        headings = get_head(valid_data, dict_of_dict)
        rows = get_rows(valid_data, headings, dict_of_dict)
    elif isinstance(valid_data, list):
        headings = ("", "value")
        i = 0
        for item in valid_data:
            if isinstance(item, str):
                rows.append((i, '"' + item + '"'))
            else:
                rows.append((i, item))
            i += 1
        rows = tuple(rows)
    elif isinstance(valid_data, dict):
        headings = ("", "value")
        for key, value in valid_data.items():
            if isinstance(value, str):
                rows.append((key, '"' + value + '"'))
            else:
                rows.append((key, value))
        rows = tuple(rows)

    root = tk.Tk()
    root.title(f"Table View of {filename}")
    root.geometry("800x235")

    table = Table(root, headings, rows)
    table.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
