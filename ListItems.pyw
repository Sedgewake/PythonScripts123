import tkinter as tk
from tkinter import messagebox

class Item:
    def __init__(self, name, item_type, price, count=1):
        self.name = name
        self.type = item_type
        self.price = price
        self.count = count

class ItemListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Tracker")
        self.root.geometry("600x500")
        self.root.configure(bg="#323232")
        self.items = []

        # Scrollable frame
        self.canvas = tk.Canvas(root, bg="#323232", highlightthickness=0)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#323232")
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Add Item Button
        self.add_button = tk.Button(root, text="+ Add Item", command=self.open_add_item_window,
                                    bg="#3a3a3a", fg="white", activebackground="#505050")
        self.add_button.pack(fill="x", pady=(0, 5))

        # Total Price Display
        self.total_label = tk.Label(root, text="Total: $0.00", bg="#323232", fg="#e6e6e6", font=("Segoe UI", 12, "bold"))
        self.total_label.pack(fill="x", pady=(0, 5))

        # Sample data
        self.add_item(Item("Apple", "Fruit", 0.5, 2))
        self.add_item(Item("Hammer", "Tool", 15.0, 1))
        self.add_item(Item("Notebook", "Stationery", 2.5, 3))

    def add_item(self, item):
        self.items.append(item)
        self.refresh_items()

    def refresh_items(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(self.items):
            self.create_item_row(i, item)

        self.update_total()

    def create_item_row(self, index, item):
        row = tk.Frame(self.scrollable_frame, bg="#3a3a3a")
        row.pack(fill="x", pady=2, padx=5)

        tk.Label(row, text=item.name, width=15, fg="white", bg="#3a3a3a").pack(side="left", padx=5)
        tk.Label(row, text=item.type, width=15, fg="white", bg="#3a3a3a").pack(side="left")
        tk.Label(row, text=f"${item.price:.2f}", width=10, fg="white", bg="#3a3a3a").pack(side="left")

        tk.Button(row, text="-", width=3, bg="#555555", fg="white",
                  command=lambda: self.decrease_count(index)).pack(side="left", padx=5)

        tk.Label(row, text=str(item.count), width=5, fg="white", bg="#3a3a3a").pack(side="left")

        tk.Button(row, text="+", width=3, bg="#555555", fg="white",
                  command=lambda: self.increase_count(index)).pack(side="left", padx=5)

    def increase_count(self, index):
        self.items[index].count += 1
        self.refresh_items()

    def decrease_count(self, index):
        if self.items[index].count > 1:
            self.items[index].count -= 1
        else:
            del self.items[index]
        self.refresh_items()

    def update_total(self):
        total = sum(item.count * item.price for item in self.items)
        self.total_label.config(text=f"Total: ${total:.2f}")

    def open_add_item_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add New Item")
        window.configure(bg="#3a3a3a")
        window.geometry("300x200")
        window.grab_set()  # modal behavior

        def create_labeled_entry(label_text):
            frame = tk.Frame(window, bg="#3a3a3a")
            frame.pack(fill="x", pady=5, padx=10)
            tk.Label(frame, text=label_text, fg="white", bg="#3a3a3a", width=10).pack(side="left")
            entry = tk.Entry(frame, bg="#222222", fg="white", insertbackground="white")
            entry.pack(side="left", fill="x", expand=True)
            return entry

        name_entry = create_labeled_entry("Name")
        type_entry = create_labeled_entry("Type")
        price_entry = create_labeled_entry("Price")

        def add():
            name = name_entry.get().strip()
            typ = type_entry.get().strip()
            try:
                price = float(price_entry.get())
                if not name or not typ:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Please enter valid data.")
                return
            self.add_item(Item(name, typ, price, 1))
            window.destroy()

        tk.Button(window, text="Add", command=add,
                  bg="#505050", fg="white", activebackground="#666666").pack(pady=10)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ItemListApp(root)
    root.mainloop()
