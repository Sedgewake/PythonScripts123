import json
import os
import string
import tkinter as tk
from selectors import SelectSelector
from tkinter import ttk
from tkinter import scrolledtext
from datetime import datetime, timedelta
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.style.core import available

matplotlib.use("Agg")

ACCOUNT = "Account"
BALANCE = "Balance: "
INCOME = "Income: "
MAIN = "Main"
HISTORY = "History"
DIAGRAM = "Diagram"
GRAPH = "Graph"
ITEMS = "Items"
ITEM = "Item: "
TYPE = "Type: "
PRICE = "Price: "
COST = "Cost: "
ADD = "Add"
CHECKIN = "Check in"
CHECKOUT = "Check out"
DISMISS = "Dismiss"

def from_cents(amount):
    return float(amount / 100)

def to_cents(amount):
    return int(amount * 100.0)

class Item:
    def __init__(self, name, item_type, price, count = 1):
        self.name = name
        self.item_type = item_type
        self.price = price
        self.count = count

class ItemGUI:
    def __init__(self, parent, app_ref, my_item):
        self.parent = parent
        self.app_ref = app_ref
        self.my_item = my_item
        self.row = tk.Frame(self.parent, bg="#3a3a3a")
        self.row.pack(fill="x", pady=1)
        self.name_label = tk.Label(self.row, text=self.my_item.name, font=("Arial", 14), width=15, fg="white", bg="#3a3a3a")
        self.name_label.pack(side="left", padx=5)
        self.type_label = tk.Label(self.row, text=self.my_item.item_type, font=("Arial", 14), width=15, fg="white", bg="#3a3a3a")
        self.type_label.pack(side="left")
        self.price_input = tk.Entry(self.row, font=("Arial", 14), width=10, fg="white", bg="#3a3a3a")
        self.price_input.pack(side="left")
        self.count_label = tk.Label(self.row, text=str(self.my_item.count), font=("Arial", 14), width=5, fg="white",bg="#3a3a3a")
        self.total_cost_d = tk.Label(self.row, text=f"{from_cents(self.my_item.price * my_item.count):.2f}",font=("Arial", 16), width=15, fg="white", bg="#3a3a3a")
        self.price_input.insert(tk.END, f"{from_cents(self.my_item.price):.2f}")
        self.price_input.bind("<KeyRelease>", self.change_item_price)
        self.total_cost_d.pack(side="left")
        self.minus_btn = tk.Button(self.row, text="-", font=("Arial", 10), width=3, bg="#555555", fg="white",command=lambda: self.decrease_count())
        self.minus_btn.pack(side="left", padx=5)
        self.count_label.pack(side="left")
        plus_btn = tk.Button(self.row, text="+", font=("Arial", 10), width=3, bg="#555555", fg="white", command=lambda: self.increase_count())
        plus_btn.pack(side="left", padx=5)

    def change_item_price(self, event):
        self.my_item.price = to_cents(float(self.price_input.get()))
        self.update_item_display()
        self.app_ref.update_pending()

    def increase_count(self):
        self.my_item.count += 1
        self.update_item_display()
        self.app_ref.update_pending()

    def decrease_count(self):
        self.my_item.count -= 1
        self.update_item_display()
        self.app_ref.update_pending()

    def update_item_display(self):
        if self.my_item.count < 1:
            self.row.destroy()
            self.app_ref.item_list.remove(self.my_item)
            return
        self.total_cost_d.configure(text=f"{from_cents(self.my_item.price * self.my_item.count):.2f}")
        self.count_label.configure(text=f"{self.my_item.count}")

class Operation:
    def __init__(self, kind, amount, balance, timestamp=None, items=None):
        self.kind = kind  # 'income' or 'purchase'
        self.amount = amount
        self.timestamp = timestamp or datetime.now()
        self.items = items or []
        self.balance = balance

    def to_dict(self):
        return {
            "kind": self.kind,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "balance": self.balance,
            "items": [item.__dict__ for item in self.items]
        }

    @staticmethod
    def from_dict(data):
        timestamp = datetime.fromisoformat(data["timestamp"])
        items = [Item(**i) for i in data.get("items", [])]
        return Operation(data["kind"], data["amount"], data["balance"], timestamp, items)

class FinanceCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.resizable(False, False)
        self.root.geometry("1000x800")
        self.root.configure(background="#323232")
        self.balance = 0
        self.pending = 0
        self.list_buttons_frame = None
        self.list_cost_label = None
        self.list_btn_ok = None
        self.list_btn_cancel = None
        self.balance_var = tk.StringVar()
        self.income_amount = None
        self.item_price_input = None
        self.income_type = None
        self.item_selector = None
        self.type_selector = None
        self.list_frame = None
        self.account_frame = None
        self.history_frame = None
        self.available_items = []
        self.available_types = []
        self.item_list = []
        self.operations = []

        self.s1 = ttk.Style()
        self.s1.theme_use("default")
        self.s1.configure("Custom.TCombobox", font=("Arial", 20), padding=1, arrowsize=20)

        self.balance_var.set(f"Balance: {float(self.balance / 100):.2f} ₽")
        app_ref = self

        style = ttk.Style()
        #style.theme_use("clam")
        style.theme_use("default")
        style.configure("TNotebook", background="#323232", borderwidth=0)
        style.configure("TNotebook.Tab", background="#323232", foreground="#e6e6e6", padding=(35, 7), font=('Segoe UI', 10, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#3a3a3a")], foreground=[("selected", "#ffffff")])
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        self.load_data()

        self.setup_tab_main()
        self.setup_tab_items()
        self.setup_tab_history()
        self.setup_tab_pie()
        self.setup_tab_graph()
        root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def setup_tab_main(self):
        tab = tk.Frame(self.notebook, bg="#323232")
        self.account_frame = tk.LabelFrame(tab, fg="white", bg="#323232")
        self.account_frame.pack(fill="x", padx=2, pady=2)
        tk.Label(self.account_frame, textvariable=self.balance_var, font=("Arial", 20), fg="white", bg="#323232").pack(pady=5)
        income_frame = tk.Frame(self.account_frame, bg="#323232")
        income_frame.pack(pady=5)
        tk.Label(income_frame, text=INCOME, font=("Arial", 20), fg="white", bg="#323232").pack(side="left")
        self.income_amount = tk.Entry(income_frame, font=("Arial", 20), width=15)
        self.income_amount.pack(side="left", padx=5)
        self.income_type = ttk.Combobox(income_frame, values=["Salary", "Gift", "Other", "Set"], style="Custom.TCombobox", font=("Arial", 20), height=20, width=10)
        self.income_type.set("Salary")
        self.income_type.pack(side="left", padx=5)
        tk.Button(income_frame, text=CHECKIN, font=("Arial", 14), command=self.add_income).pack(side="left", padx=5)
        select_frame = tk.Frame(tab, bg="#323232")
        select_frame.pack(pady=5)
        tk.Label(select_frame, text=ITEM, font=("Arial", 20), fg="white", bg="#323232").pack(side="left")
        self.item_selector = ttk.Combobox(select_frame, values=[item.name for item in self.available_items], style="Custom.TCombobox", font=("Arial", 20), height=20, width=15)
        self.item_selector.set("")
        self.item_selector.pack(side="left")
        self.item_selector.bind("<<ComboboxSelected>>", self.item_change)
        tk.Label(select_frame, text=TYPE, font=("Arial", 20), fg="white", bg="#323232").pack(side="left")
        self.type_selector = ttk.Combobox(select_frame, values=[item for item in self.available_types], style="Custom.TCombobox", font=("Arial", 20), height=20, width=12)
        self.type_selector.set("")
        self.type_selector.pack(side="left")
        tk.Label(select_frame, text=PRICE, font=("Arial", 20), fg="white", bg="#323232").pack(side="left")
        self.item_price_input = tk.Entry(select_frame, font=("Arial", 20), width=10)
        self.item_price_input.pack(side="left", padx=5)
        tk.Button(select_frame, text=ADD, font=("Arial", 14), command=self.add_item).pack(side="left", padx=5)

        self.list_frame = tk.Frame(tab, bg="#323232")
        self.list_frame.pack(pady=5)

        self.list_buttons_frame = tk.Frame(tab, bg="#323232")
        self.list_buttons_frame.pack(pady=5)
        self.list_cost_label = tk.Label(self.list_buttons_frame, text=COST + f"{float(self.pending / 100):.2f} ₽", font=("Arial", 20), fg="white", bg="#323232")
        self.list_cost_label.pack(side="left")
        self.list_btn_ok = tk.Button(self.list_buttons_frame, text=CHECKOUT, font=("Arial", 14), command=self.check_out)
        self.list_btn_ok.pack(side="left", padx=5)
        self.list_btn_cancel = tk.Button(self.list_buttons_frame, text=DISMISS, font=("Arial", 14), command=self.dismiss_list)
        self.list_btn_cancel.pack(side="left", padx=5)
        self.notebook.add(tab, text="Main")
        self.update_pending()
        self.refresh_items()

    def setup_tab_items(self):
        tab = tk.Frame(self.notebook, bg="#323232")
        self.notebook.add(tab, text=ITEMS)


    def setup_tab_history(self):
        tab = tk.Frame(self.notebook, bg="#323232")
        canvas = tk.Canvas(tab, bg="#323232", highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.history_frame = tk.Frame(canvas, bg="#323232")
        self.history_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        history_window = canvas.create_window((0, 0), window=self.history_frame, anchor="nw")

        def resize_frame(event):
            canvas.itemconfig(history_window, width=event.width)

        canvas.bind("<Configure>", resize_frame)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.refresh_history()
        self.notebook.add(tab, text="History")

    def refresh_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        for op in reversed(self.operations):
            base = f"[{op.timestamp.strftime('%Y-%m-%d %H:%M')}] {op.kind}: {op.amount:.2f} ₽   Balance: {op.balance:.2f} ₽"
            op_frame = tk.Frame(self.history_frame, bg="#3a3a3a")
            op_frame.pack(fill="x", padx=10, pady=3)
            tk.Label(op_frame, text=base, fg="white", bg="#3a3a3a").pack(side="left")
            if op.items:
                def toggle(frame=op_frame, items=op.items):
                    if hasattr(frame, 'expanded') and frame.expanded:
                        for w in frame.extra:
                            w.destroy()
                        frame.expanded = False
                    else:
                        frame.extra = [tk.Label(frame, text=f"  - {i.name} ({i.count}) ({from_cents(i.price * i.count):.2f})", fg="white", bg="#444") for i in items]
                        for w in frame.extra:
                            w.pack(anchor="w")
                        frame.expanded = True
                tk.Button(op_frame, text="Expand", command=toggle, fg="white", bg="#323232").pack(side="right")

    def setup_tab_pie(self):
        tab = tk.Frame(self.notebook, bg="#323232")

        self.notebook.add(tab, text="Chart")

    def setup_tab_graph(self):
        tab = tk.Frame(self.notebook, bg="#323232")

        self.notebook.add(tab, text="Graph")

    def on_closing(self):
        self.save_data()
        main_window.destroy()

    def save_data(self):
        with open("fc_data.json", "w") as f:
            json.dump({
                "balance": self.balance,
                "item_list": [item.__dict__ for item in self.item_list],
                "item_types": [item for item in self.available_types],
                "items": [item.__dict__ for item in self.available_items],
                "history": [op.to_dict() for op in self.operations]

            }, f, indent=2)

    def load_data(self):
        if os.path.exists("fc_data.json"):
            with open("fc_data.json", "r") as f:
                data = json.load(f)
                self.balance = data.get("balance", 0)
                self.item_list = [Item(**item) for item in data.get("item_list", [])]
                self.available_types = data.get("item_types", [])
                self.operations = [Operation.from_dict(op) for op in data.get("history", [])]
                self.available_items = [Item(**item) for item in data.get("items", [])]


    def add_income(self):
        try:
            amount = int(float(self.income_amount.get()) * 100.0)
        except ValueError:
            return
        if self.income_type.get() == "Set":
            b1 = self.balance
            self.balance = amount
            self.operations.append(Operation("Set balance", from_cents(self.balance - b1), from_cents(self.balance)))
        else:
            self.balance += amount
            if amount > 0:
                self.operations.append(Operation("Income ("+self.income_type.get()+")", from_cents(amount), from_cents(self.balance)))
            else:
                self.operations.append(Operation("Expense (" + self.income_type.get() + ")", from_cents(amount), from_cents(self.balance)))
        self.income_amount.delete(0, tk.END)
        self.update_main_tab()
        self.refresh_history()

    def update_main_tab(self):
        if self.pending > 0:
            self.balance_var.set(f"Balance: {float(self.balance / 100):.2f} ({float((self.balance - self.pending) / 100):.2f}) ₽")
            self.list_cost_label.pack(side="left")
            self.list_cost_label.configure(text=f"Cost: {float(self.pending / 100):.2f} ₽")
            self.list_btn_ok.pack(side="left", padx=5)
            self.list_btn_cancel.pack(side="left", padx=5)
        else:
            self.balance_var.set(f"Balance: {float(self.balance / 100):.2f} ₽")
            self.list_cost_label.pack_forget()
            self.list_btn_ok.pack_forget()
            self.list_btn_cancel.pack_forget()

    def add_item(self):
        i1 = Item(self.item_selector.get(), self.type_selector.get(), to_cents(float(self.item_price_input.get())))
        ItemGUI(self.list_frame, self, i1)
        self.item_list.append(i1)
        self.update_pending()
        match = False
        for t in self.available_types:
            if i1.item_type == t:
                match = True
                break
        if not match:
            self.available_types.append(i1.item_type)
            self.type_selector.config(values=[item for item in self.available_types])
        for item in self.available_items:
            if item.name == i1.name:
                item.item_type = i1.item_type
                item.price = i1.price
                return
        self.available_items.append(i1)
        self.item_selector.config(values=[item.name for item in self.available_items])

    def check_out(self):
        self.balance -= self.pending
        self.operations.append(Operation("Purchase", from_cents(self.pending), from_cents(self.balance), None, self.item_list.copy()))
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.item_list.clear()
        self.update_pending()
        self.refresh_history()

    def dismiss_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.item_list.clear()
        self.update_pending()

    def update_pending(self):
        self.pending = 0
        for item in self.item_list:
            self.pending += item.price * item.count
        self.update_main_tab()
        if len(self.item_list) > 17:
            self.root.resizable(False, True)

    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        tab_index = event.widget.index(selected_tab)
        tab_name = self.notebook.tab(selected_tab, "text")

        if tab_name == "History":
            print("History tab selected")
            self.refresh_history()
        elif tab_name == "Main":
            print("Main tab selected")
        elif tab_name == "Items":
            print("Items tab selected")
            self.refresh_items()
        elif tab_name == "Chart":
            print("Chart tab selected")
            # self.update_chart()  ← if you add such a method
        elif tab_name == "Graph":
            print("Graph tab selected")
            # self.update_graph()  ← if you add such a method

    def item_change(self, event):
        if len(self.available_items) < 1:
            return
        input_v = self.item_selector.get()
        for item in self.available_items:
            if item.name == input_v:
                self.type_selector.set(item.item_type)
                self.item_price_input.delete(0, tk.END)
                self.item_price_input.insert(tk.END, f"{float(item.price / 100):.2f}")
                return

    def refresh_items(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        for i, item in enumerate(self.item_list):
            ItemGUI(self.list_frame, self, item)


if __name__ == "__main__":
    main_window = tk.Tk()
    app = FinanceCalcApp(main_window)
    main_window.mainloop()