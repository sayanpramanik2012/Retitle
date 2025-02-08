import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import sys
from io import StringIO

def setup_adder_tab(notebook, console_text):
    tab_adder = ttk.Frame(notebook)
    notebook.add(tab_adder, text="Adder")

    label_directory = tk.Label(tab_adder, text="Directory:")
    label_directory.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

    entry_directory = tk.Entry(tab_adder, width=50)
    entry_directory.grid(row=0, column=1, padx=10, pady=5)

    button_browse = tk.Button(tab_adder, text="Browse", command=lambda: get_directory_path(entry_directory))
    button_browse.grid(row=0, column=2, padx=5, pady=5)

    filter_var = tk.StringVar()
    filter_var.set("all")

    label_filter = tk.Label(tab_adder, text="Filter:")
    label_filter.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    filter_combobox = ttk.Combobox(tab_adder, values=["all", "starting", "ending", "both"], textvariable=filter_var)
    filter_combobox.grid(row=1, column=1, padx=10, pady=5)

    label_prefix = tk.Label(tab_adder, text="Prefix to Add:")
    label_prefix.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

    entry_prefix = tk.Entry(tab_adder, width=50)
    entry_prefix.grid(row=2, column=1, padx=10, pady=5)

    label_postfix = tk.Label(tab_adder, text="Postfix to Add:")
    label_postfix.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

    entry_postfix = tk.Entry(tab_adder, width=50)
    entry_postfix.grid(row=3, column=1, padx=10, pady=5)

    checkbox_prefix_var = tk.BooleanVar()
    checkbox_prefix = tk.Checkbutton(tab_adder, text="Add Prefix", variable=checkbox_prefix_var)
    checkbox_prefix.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

    checkbox_postfix_var = tk.BooleanVar()
    checkbox_postfix = tk.Checkbutton(tab_adder, text="Add Postfix", variable=checkbox_postfix_var)
    checkbox_postfix.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

    button_add = tk.Button(tab_adder, text="Add to Files",
                           command=lambda: start_add(entry_directory, filter_var.get(), entry_prefix, entry_postfix,
                                                    checkbox_prefix_var, checkbox_postfix_var, console_text))
    button_add.grid(row=5, column=0, columnspan=2, pady=10)

def get_directory_path(entry_widget):
    directory_path = filedialog.askdirectory()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, directory_path)

def start_add(directory_entry, filter_option, prefix_entry, postfix_entry, prefix_checkbox_var, postfix_checkbox_var, console_text):
    directory_path = directory_entry.get()
    if not directory_path or not os.path.isdir(directory_path):
        append_to_console(console_text, "Invalid directory path!")
        return
    add_prefix = prefix_checkbox_var.get()
    add_postfix = postfix_checkbox_var.get()

    # Redirect sys.stdout to the console_text widget
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Call the add_files function based on the selected filter option
        if filter_option == "all":
            add_all(directory_path, add_prefix, add_postfix, prefix_entry, postfix_entry)
        elif filter_option == "starting":
            user_input = get_user_input("Enter the starting characters:")
            add_starting_with(directory_path, add_prefix, add_postfix, user_input, prefix_entry, postfix_entry)
        elif filter_option == "ending":
            user_input = get_user_input("Enter the ending characters:")
            add_ending_with(directory_path, add_prefix, add_postfix, user_input, prefix_entry, postfix_entry)
        elif filter_option == "both":
            start_input = get_user_input("Enter the starting characters:")
            end_input = get_user_input("Enter the ending characters:")
            add_starting_and_ending(directory_path, add_prefix, add_postfix, start_input, end_input, prefix_entry, postfix_entry)

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

def add_all(directory_path, add_prefix, add_postfix, prefix_entry, postfix_entry):
    files = os.listdir(directory_path)

    for filename in files:
        # Split the filename and extension
        name, extension = os.path.splitext(filename)

        # Add prefix if selected
        if add_prefix:
            name = f"{prefix_entry.get()}{name}"

        # Add postfix if selected
        if add_postfix:
            name = f"{name}{postfix_entry.get()}"

        # Construct the full paths for the old and new filenames
        old_path = os.path.join(directory_path, filename)
        new_path = os.path.join(directory_path, f"{name}{extension}")

        # Rename the file
        os.rename(old_path, new_path)

        # Print a message indicating the renaming process
        print(f'Added to {filename}: {name}{extension}')

def add_starting_with(directory_path, add_prefix, add_postfix, user_input, prefix_entry, postfix_entry):
    files = os.listdir(directory_path)

    for filename in files:
        # Split the filename and extension
        name, extension = os.path.splitext(filename)

        # Check if the filename starts with the specified characters
        if name.startswith(user_input):
            # Add prefix if selected
            if add_prefix:
                name = f"{prefix_entry.get()}{name}"

            # Add postfix if selected
            if add_postfix:
                name = f"{name}{postfix_entry.get()}"

            # Construct the full paths for the old and new filenames
            old_path = os.path.join(directory_path, filename)
            new_path = os.path.join(directory_path, f"{name}{extension}")

            # Rename the file
            os.rename(old_path, new_path)

            # Print a message indicating the renaming process
            print(f'Added to {filename}: {name}{extension}')

def add_ending_with(directory_path, add_prefix, add_postfix, user_input, prefix_entry, postfix_entry):
    files = os.listdir(directory_path)

    for filename in files:
        # Split the filename and extension
        name, extension = os.path.splitext(filename)

        # Check if the filename ends with the specified characters
        if name.endswith(user_input):
            # Add prefix if selected
            if add_prefix:
                name = f"{prefix_entry.get()}{name}"

            # Add postfix if selected
            if add_postfix:
                name = f"{name}{postfix_entry.get()}"

            # Construct the full paths for the old and new filenames
            old_path = os.path.join(directory_path, filename)
            new_path = os.path.join(directory_path, f"{name}{extension}")

            # Rename the file
            os.rename(old_path, new_path)

            # Print a message indicating the renaming process
            print(f'Added to {filename}: {name}{extension}')

def add_starting_and_ending(directory_path, add_prefix, add_postfix, start_input, end_input, prefix_entry, postfix_entry):
    files = os.listdir(directory_path)

    for filename in files:
        # Split the filename and extension
        name, extension = os.path.splitext(filename)

        # Check if the filename starts and ends with the specified characters
        if name.startswith(start_input) and name.endswith(end_input):
            # Add prefix if selected
            if add_prefix:
                name = f"{prefix_entry.get()}{name}"

            # Add postfix if selected
            if add_postfix:
                name = f"{name}{postfix_entry.get()}"

            # Construct the full paths for the old and new filenames
            old_path = os.path.join(directory_path, filename)
            new_path = os.path.join(directory_path, f"{name}{extension}")

            # Rename the file
            os.rename(old_path, new_path)

            # Print a message indicating the renaming process
            print(f'Added to {filename}: {name}{extension}')

def get_user_input(prompt):
    user_input = tk.simpledialog.askstring("User Input", prompt)
    return user_input

# Other functions (add_all, setup_adder_tab, start_add) remain unchanged
