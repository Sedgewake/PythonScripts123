import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class Item:
    def __init__(self, name, item_type, price, count):
        self.name = name
        self.item_type = item_type
        self.price = price
        self.count = count

class ItemTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Table with Right-Click Menu")
        self.root.geometry("700x400")

        self.items = [
            Item("Apple", "Fruit", 1.2, 100),
            Item("Screwdriver", "Tool", 4.5, 25),
            Item("Notebook", "Stationery", 2.8, 50),
        ]

        self.create_treeview()
        self.create_popup_menu()
        self.populate_table()

    def create_treeview(self):
        self.tree = ttk.Treeview(self.root, columns=("Name", "Type", "Price", "Count"), show="headings")
        for col in ("Name", "Type", "Price", "Count"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Button-3>", self.show_popup)

    def create_popup_menu(self):
        self.popup = tk.Menu(self.root, tearoff=0)
        self.popup.add_command(label="Edit Item", command=self.edit_selected_item)
        self.popup.add_command(label="Delete Item", command=self.delete_selected_item)

    def show_popup(self, event):
        selected = self.tree.identify_row(event.y)
        if selected:
            self.tree.selection_set(selected)
            self.popup.post(event.x_root, event.y_root)

    def populate_table(self):
        for i, item in enumerate(self.items):
            self.tree.insert("", "end", iid=str(i), values=(item.name, item.item_type, item.price, item.count))

    def edit_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = int(selected[0])
        item = self.items[item_id]

        # Popup dialog to edit
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit Item")
        edit_win.geometry("300x200")
        edit_win.transient(self.root)

        # Entry fields
        tk.Label(edit_win, text="Name").pack()
        name_entry = tk.Entry(edit_win)
        name_entry.pack()
        name_entry.insert(0, item.name)

        tk.Label(edit_win, text="Type").pack()
        type_entry = tk.Entry(edit_win)
        type_entry.pack()
        type_entry.insert(0, item.item_type)

        tk.Label(edit_win, text="Price").pack()
        price_entry = tk.Entry(edit_win)
        price_entry.pack()
        price_entry.insert(0, str(item.price))

        tk.Label(edit_win, text="Count").pack()
        count_entry = tk.Entry(edit_win)
        count_entry.pack()
        count_entry.insert(0, str(item.count))

        def save_changes():
            try:
                item.name = name_entry.get()
                item.item_type = type_entry.get()
                item.price = float(price_entry.get())
                item.count = int(count_entry.get())
                self.tree.item(selected, values=(item.name, item.item_type, item.price, item.count))
                edit_win.destroy()
            except ValueError:
                messagebox.showerror("Invalid input", "Price must be float and Count must be integer")

        tk.Button(edit_win, text="Save", command=save_changes).pack(pady=10)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            return

        item_id = int(selected[0])
        confirm = messagebox.askyesno("Delete", f"Delete item '{self.items[item_id].name}'?")
        if confirm:
            self.tree.delete(selected)
            del self.items[item_id]

            # Rebuild tree to update iids
            self.tree.delete(*self.tree.get_children())
            self.populate_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = ItemTableApp(root)
    root.mainloop()
