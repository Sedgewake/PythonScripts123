import tkinter as tk
from tkinter import ttk

class DarkTabbedEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Tabbed Text Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="#323232")  # RGB (50,50,50)

        # Style configuration
        style = ttk.Style()
        style.theme_use("default")

        # Notebook tab styling (dark background, light text, taller tabs)
        style.configure("TNotebook",
                        background="#323232",
                        borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#323232",
                        foreground="#e6e6e6",
                        padding=(12, 12),
                        font=('Segoe UI', 10, 'bold'))
        style.map("TNotebook.Tab",
                  background=[("selected", "#3a3a3a")],
                  foreground=[("selected", "#ffffff")])

        # Notebook widget
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

        # New Tab button
        add_tab_btn = tk.Button(root, text="+ New Tab", command=self.add_new_tab,
                                bg="#3a3a3a", fg="#e6e6e6", activebackground="#505050", activeforeground="#ffffff")
        add_tab_btn.pack(fill="x")

        # Add first tab
        self.add_new_tab()

    def add_new_tab(self):
        # Create frame for the tab
        tab_frame = ttk.Frame(self.notebook)
        tab_frame.pack(fill="both", expand=True)

        # Create a Text widget inside the tab
        text_editor = tk.Text(tab_frame,
                              bg="#2b2b2b", fg="#e6e6e6",
                              insertbackground="#ffffff",  # cursor color
                              selectbackground="#555555",
                              wrap="word")
        text_editor.pack(fill="both", expand=True)

        # Give it a name
        tab_index = len(self.notebook.tabs()) + 1
        self.notebook.add(tab_frame, text=f"Tab {tab_index}")
        self.notebook.select(tab_frame)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DarkTabbedEditor(root)
    root.mainloop()
