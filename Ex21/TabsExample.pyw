import tkinter as tk
from tkinter import ttk

class TabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Browser-like Tabs with Tkinter")

        # Create the Notebook (tab container)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Add the first tab
        self.add_new_tab()

        # Add button to add more tabs
        add_tab_btn = tk.Button(root, text="+ New Tab", command=self.add_new_tab)
        add_tab_btn.pack(side="bottom", fill='x')

    def add_new_tab(self):
        # Create a frame for the new tab
        new_tab = ttk.Frame(self.notebook)

        # Example content in tab
        label = tk.Label(new_tab, text="This is a new tab")
        label.pack(padx=10, pady=10)

        # Add tab to notebook
        tab_index = len(self.notebook.tabs()) + 1
        self.notebook.add(new_tab, text=f"Tab {tab_index}")

        # Optionally select the new tab
        self.notebook.select(new_tab)

# Run the application
root = tk.Tk()
app = TabApp(root)
root.mainloop()
