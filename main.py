import tkinter as tk
from tkinter import ttk
from tabs.remover import setup_removal_tab
from tabs.adder import setup_adder_tab 

root = tk.Tk()
root.title("Retitle")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10)

# Console area with Scrollbar
console_text = tk.Text(root, height=10, width=60, state=tk.DISABLED, wrap=tk.WORD)
console_text.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

scrollbar = tk.Scrollbar(root, command=console_text.yview)
scrollbar.grid(row=1, column=2, sticky="ns")

console_text.config(yscrollcommand=scrollbar.set)

setup_removal_tab(notebook, console_text)  # Pass the console_text to setup_removal_tab
setup_adder_tab(notebook, console_text)

root.mainloop()