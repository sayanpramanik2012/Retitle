import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import sys
from io import StringIO

def setup_removal_tab(notebook, console_text):
    tab_removal = ttk.Frame(notebook)
    notebook.add(tab_removal, text="Remover")

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
                                                          checkbox_prefix_var, checkbox_postfix_var, console_text))
    button_rename.grid(row=4, column=0, columnspan=2, pady=10)

def get_directory_path(entry_widget):
    directory_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, directory_path)

def start_rename(directory_entry, prefix_entry, postfix_entry, prefix_checkbox_var, postfix_checkbox_var, console_text):
    directory_path = directory_entry.get()
    if not directory_path or not os.path.isdir(directory_path):
        append_to_console(console_text, "Invalid directory path!")
        return
    remove_prefix = prefix_checkbox_var.get()
    remove_postfix = postfix_checkbox_var.get()

    # Redirect sys.stdout to the console_text widget
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Call the rename_files function
        files = os.listdir(directory_path)

        # Iterate through each file in the directory
        for filename in files:
            # Split the filename and extension
            name, extension = os.path.splitext(filename)

            # Check if the filename starts with the specified prefix
            if remove_prefix and name.startswith(prefix_entry.get()):
                name = name[len(prefix_entry.get()):]

            # Check if the filename ends with the specified postfix
            if remove_postfix and name.endswith(postfix_entry.get()):
                name = name[:-len(postfix_entry.get())]

            # Construct the full paths for the old and new filenames
            old_path = os.path.join(directory_path, filename)
            new_path = os.path.join(directory_path, f"{name}{extension}")

            # Rename the file
            os.rename(old_path, new_path)

            # Print a message indicating the renaming process
            print(f'Renamed: {filename} to {name}{extension}')

        # Get the captured output and insert it into the console_text widget
        console_output = sys.stdout.getvalue()
        console_text.config(state=tk.NORMAL)  # Enable the widget to insert text
        console_text.insert(tk.END, console_output)

        # Scroll to the end of the console
        console_text.see(tk.END)
    finally:
        # Restore sys.stdout
        sys.stdout = old_stdout
        console_text.config(state=tk.DISABLED)
