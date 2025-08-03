import tkinter as tk
from tkinter import ttk


class ExcelLikeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel-like Table - Dark Mode with Cell Borders")
        self.root.geometry("700x400")
        self.setup_style()
        self.create_table()

    def setup_style(self):
        style = ttk.Style(self.root)
        self.root.configure(bg="#2b2b2b")
        style.theme_use("default")

        # Treeview style
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="#ffffff",
                        fieldbackground="#2b2b2b",
                        rowheight=26,
                        font=('Segoe UI', 10),
                        bordercolor="#5a5a5a",
                        borderwidth=1)

        # Heading style
        style.configure("Treeview.Heading",
                        background="#3c3f41",
                        foreground="#ffffff",
                        font=('Segoe UI', 10, 'bold'),
                        borderwidth=1)

        # Selected row styling
        style.map("Treeview",
                  background=[('selected', '#4a708b')],
                  foreground=[('selected', '#ffffff')])

    def create_table(self):
        columns = ("A", "B", "C", "D")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Insert data with striped rows to simulate borders
        for i in range(30):
            bg = "#333333" if i % 2 == 0 else "#3a3a3a"
            self.tree.insert("", "end", values=(f"Item {i}", f"Data {i}", f"Val {i}", f"More {i}"),
                             tags=(f'row{i}',))
            self.tree.tag_configure(f'row{i}', background=bg)

        self.tree.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        col_index = int(column[1:]) - 1

        if not row_id:
            return

        x, y, width, height = self.tree.bbox(row_id, column)
        value = self.tree.item(row_id)['values'][col_index]

        self.entry = tk.Entry(self.tree, font=('Segoe UI', 10), bg="#444", fg="#fff", bd=1, relief="solid")
        self.entry.place(x=x, y=y, width=width, height=height)
        self.entry.insert(0, value)
        self.entry.focus()

        def save_edit(event):
            new_val = self.entry.get()
            values = list(self.tree.item(row_id)['values'])
            values[col_index] = new_val
            self.tree.item(row_id, values=values)
            self.entry.destroy()

        self.entry.bind("<Return>", save_edit)
        self.entry.bind("<FocusOut>", lambda e: self.entry.destroy())


if __name__ == "__main__":
    root = tk.Tk()
    app = ExcelLikeApp(root)
    root.mainloop()
