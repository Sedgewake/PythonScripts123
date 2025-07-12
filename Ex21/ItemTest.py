import tkinter as tk

class Item:
    def __init__(self, name, item_type, price, count=1):
        self.name = name
        self.type = item_type
        self.price = price
        self.count = count

class ItemListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Item List with Count Buttons")
        self.root.configure(bg="#323232")
        self.items = []

        self.item_frame = tk.Frame(root, bg="#323232")
        self.item_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Sample items
        self.add_item(Item("Apple", "Fruit", 0.5, 2))
        self.add_item(Item("Hammer", "Tool", 15.0, 1))
        self.add_item(Item("Notebook", "Stationery", 2.5, 3))

    def add_item(self, item):
        self.items.append(item)
        self.refresh_items()

    def refresh_items(self):
        for widget in self.item_frame.winfo_children():
            widget.destroy()

        for i, item in enumerate(self.items):
            self.create_item_row(i, item)

    def create_item_row(self, index, item):
        row = tk.Frame(self.item_frame, bg="#3a3a3a")
        row.pack(fill="x", pady=3)

        name_label = tk.Label(row, text=item.name, width=15, fg="white", bg="#3a3a3a")
        name_label.pack(side="left", padx=5)

        type_label = tk.Label(row, text=item.type, width=15, fg="white", bg="#3a3a3a")
        type_label.pack(side="left")

        price_label = tk.Label(row, text=f"${item.price:.2f}", width=10, fg="white", bg="#3a3a3a")
        price_label.pack(side="left")

        minus_btn = tk.Button(row, text="-", width=3, bg="#555555", fg="white",
                              command=lambda: self.decrease_count(index))
        minus_btn.pack(side="left", padx=5)

        count_label = tk.Label(row, text=str(item.count), width=5, fg="white", bg="#3a3a3a")
        count_label.pack(side="left")

        plus_btn = tk.Button(row, text="+", width=3, bg="#555555", fg="white",
                             command=lambda: self.increase_count(index))
        plus_btn.pack(side="left", padx=5)

    def increase_count(self, index):
        self.items[index].count += 1
        self.refresh_items()

    def decrease_count(self, index):
        if self.items[index].count > 1:
            self.items[index].count -= 1
        else:
            del self.items[index]
        self.refresh_items()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ItemListApp(root)
    root.mainloop()
