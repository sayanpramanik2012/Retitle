# main.py
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tabs.file_renamer import rename_files

def get_directory_path(entry_widget):
    directory_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, directory_path)

def start_rename(directory_entry, prefix_entry, postfix_entry, prefix_checkbox_var, postfix_checkbox_var):
    directory_path = directory_entry.get()
    remove_prefix = prefix_checkbox_var.get()
    remove_postfix = postfix_checkbox_var.get()

    rename_files(directory_path, remove_prefix, remove_postfix, prefix_entry, postfix_entry)


# Create the main window
root = tk.Tk()
root.title("File Renamer")

# Create and place tabs
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10)

# Tab 1: Removal
tab_removal = ttk.Frame(notebook)
notebook.add(tab_removal, text="Removal")

# Widgets for tab 1
label_directory = tk.Label(tab_removal, text="Directory:")
label_directory.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

entry_directory = tk.Entry(tab_removal, width=50)
entry_directory.grid(row=0, column=1, padx=10, pady=5)

button_browse = tk.Button(tab_removal, text="Browse", command=lambda: get_directory_path(entry_directory))
button_browse.grid(row=0, column=2, padx=5, pady=5)

label_prefix = tk.Label(tab_removal, text="Prefix to Remove:")
label_prefix.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

entry_prefix = tk.Entry(tab_removal, width=50)
entry_prefix.grid(row=1, column=1, padx=10, pady=5)

label_postfix = tk.Label(tab_removal, text="Postfix to Remove:")
label_postfix.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

entry_postfix = tk.Entry(tab_removal, width=50)
entry_postfix.grid(row=2, column=1, padx=10, pady=5)

checkbox_prefix_var = tk.BooleanVar()
checkbox_prefix = tk.Checkbutton(tab_removal, text="Remove Prefix", variable=checkbox_prefix_var)
checkbox_prefix.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

checkbox_postfix_var = tk.BooleanVar()
checkbox_postfix = tk.Checkbutton(tab_removal, text="Remove Postfix", variable=checkbox_postfix_var)
checkbox_postfix.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

button_rename = tk.Button(tab_removal, text="Rename Files",
                          command=lambda: start_rename(entry_directory, entry_prefix, entry_postfix,
                                                      checkbox_prefix_var, checkbox_postfix_var))

button_rename.grid(row=4, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
