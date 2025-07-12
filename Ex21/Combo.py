import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_value = combo.get()
    print("Selected or entered:", selected_value)

root = tk.Tk()
root.title("Editable ComboBox")
root.geometry("300x100")

values = ["Groceries", "Rent", "Utilities", "Transport"]

combo = ttk.Combobox(root, values=values)
combo.set("Select or type...")  # Optional placeholder
combo.bind("<<ComboboxSelected>>", on_select)
combo.pack(padx=10, pady=20, fill="x")

root.mainloop()
