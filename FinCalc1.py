# --- Import required libraries ---
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import json
import os

# --- Sample data ---
class Operation:
    def __init__(self, kind, amount, timestamp=None, items=None):
        self.kind = kind  # 'income' or 'purchase'
        self.amount = amount
        self.timestamp = timestamp or datetime.now()
        self.items = items or []

    def to_dict(self):
        return {
            "kind": self.kind,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "items": [item.__dict__ for item in self.items]
        }

    @staticmethod
    def from_dict(data):
        timestamp = datetime.fromisoformat(data["timestamp"])
        items = [Item(**i) for i in data.get("items", [])]
        return Operation(data["kind"], data["amount"], timestamp, items)

class Item:
    def __init__(self, name, typ, price):
        self.name = name
        self.typ = typ
        self.price = price

# --- Main Application Class ---
class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Tracker")
        self.root.geometry("1000x700")

        self.balance = 0.0
        self.available_items = []
        self.pending_items = []
        self.history = []

        self.load_items()
        self.load_state()

        self.setup_tabs()

    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_balance = tk.Frame(self.notebook, bg="#323232")
        self.tab_history = tk.Frame(self.notebook, bg="#323232")
        self.tab_pie = tk.Frame(self.notebook, bg="#323232")
        self.tab_graph = tk.Frame(self.notebook, bg="#323232")

        self.notebook.add(self.tab_balance, text="Balance")
        self.notebook.add(self.tab_history, text="History")
        self.notebook.add(self.tab_pie, text="Stats Pie")
        self.notebook.add(self.tab_graph, text="Income vs Expense")

        self.setup_tab_balance()
        self.setup_tab_history()
        self.setup_tab_pie()
        self.setup_tab_graph()

    # --- JSON Persistence ---
    def save_items(self):
        with open("items.json", "w") as f:
            json.dump([item.__dict__ for item in self.available_items], f, indent=2)

    def load_items(self):
        if os.path.exists("items.json"):
            with open("items.json", "r") as f:
                data = json.load(f)
                self.available_items = [Item(**item) for item in data]
        else:
            self.available_items = [Item("Apple", "Food", 1.0), Item("Notebook", "Stationery", 3.5)]

    def save_state(self):
        with open("state.json", "w") as f:
            json.dump({
                "balance": self.balance,
                "pending_items": [item.__dict__ for item in self.pending_items],
                "history": [op.to_dict() for op in self.history]
            }, f, indent=2)

    def load_state(self):
        if os.path.exists("state.json"):
            with open("state.json", "r") as f:
                data = json.load(f)
                self.balance = data.get("balance", 0.0)
                self.pending_items = [Item(**item) for item in data.get("pending_items", [])]
                self.history = [Operation.from_dict(op) for op in data.get("history", [])]

    # --- Tab 1: Balance ---
    def setup_tab_balance(self):
        frame = self.tab_balance

        self.balance_var = tk.StringVar()
        self.update_balance_label()
        tk.Label(frame, textvariable=self.balance_var, font=("Arial", 20), fg="white", bg="#323232").pack(pady=10)

        # Income entry
        income_frame = tk.Frame(frame, bg="#323232")
        income_frame.pack(pady=10)

        tk.Label(income_frame, text="Income:", fg="white", bg="#323232").pack(side="left")
        self.income_amount = tk.Entry(income_frame, width=10)
        self.income_amount.pack(side="left", padx=5)

        self.income_type = ttk.Combobox(income_frame, values=["Salary", "Gift", "Other"], width=15)
        self.income_type.set("Salary")
        self.income_type.pack(side="left", padx=5)

        tk.Button(income_frame, text="Check In", command=self.add_income).pack(side="left", padx=5)

        # Pending purchases
        tk.Label(frame, text="Pending Items:", fg="white", bg="#323232").pack(pady=(20, 0))
        self.pending_frame = tk.Frame(frame, bg="#323232")
        self.pending_frame.pack()

        # Item selection
        select_frame = tk.Frame(frame, bg="#323232")
        select_frame.pack(pady=10)

        self.item_selector = ttk.Combobox(select_frame, values=[item.name for item in self.available_items])
        if self.available_items:
            self.item_selector.set(self.available_items[0].name)
        self.item_selector.pack(side="left")

        tk.Button(select_frame, text="Add Item", command=self.add_pending_item).pack(side="left", padx=5)
        tk.Button(select_frame, text="Check Out", command=self.checkout_items).pack(side="left", padx=5)
        tk.Button(select_frame, text="Add New Item", command=self.add_new_item_popup).pack(side="left", padx=5)

        self.refresh_pending_items()

    def update_balance_label(self):
        self.balance_var.set(f"Current Balance: ${self.balance:.2f}")

    def add_income(self):
        try:
            amount = float(self.income_amount.get())
            kind = self.income_type.get()
            self.balance += amount
            self.history.append(Operation('income', amount))
            self.update_balance_label()
            self.income_amount.delete(0, tk.END)
            self.save_state()
        except:
            messagebox.showerror("Invalid Input", "Please enter a valid amount")

    def add_pending_item(self):
        name = self.item_selector.get()
        item = next((i for i in self.available_items if i.name == name), None)
        if item:
            self.pending_items.append(item)
            self.refresh_pending_items()
            self.save_state()

    def refresh_pending_items(self):
        for widget in self.pending_frame.winfo_children():
            widget.destroy()
        for item in self.pending_items:
            tk.Label(self.pending_frame, text=f"{item.name} - ${item.price:.2f}", fg="white", bg="#323232").pack()

    def checkout_items(self):
        total = sum(item.price for item in self.pending_items)
        if total > self.balance:
            messagebox.showerror("Insufficient Funds", "You don't have enough balance to checkout.")
            return
        self.balance -= total
        self.history.append(Operation('purchase', total, items=list(self.pending_items)))
        self.pending_items.clear()
        self.update_balance_label()
        self.refresh_pending_items()
        self.save_state()

    def add_new_item_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Add New Item")
        win.configure(bg="#3a3a3a")
        tk.Label(win, text="Name:", fg="white", bg="#3a3a3a").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()
        tk.Label(win, text="Type:", fg="white", bg="#3a3a3a").pack()
        type_entry = tk.Entry(win)
        type_entry.pack()
        tk.Label(win, text="Price:", fg="white", bg="#3a3a3a").pack()
        price_entry = tk.Entry(win)
        price_entry.pack()

        def add():
            try:
                name = name_entry.get().strip()
                typ = type_entry.get().strip()
                price = float(price_entry.get())
                if name and typ:
                    new_item = Item(name, typ, price)
                    self.available_items.append(new_item)
                    self.item_selector["values"] = [item.name for item in self.available_items]
                    self.save_items()
                    win.destroy()
            except:
                messagebox.showerror("Error", "Invalid data")

        tk.Button(win, text="Add", command=add).pack(pady=10)

# --- Remaining tabs are unchanged ---

    # --- Tab 2: History ---
    def setup_tab_history(self):
        self.history_frame = tk.Frame(self.tab_history, bg="#323232")
        self.history_frame.pack(fill="both", expand=True)
        self.refresh_history()

    def refresh_history(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        for op in reversed(self.history):
            base = f"[{op.timestamp.strftime('%Y-%m-%d %H:%M')}] {'INCOME' if op.kind == 'income' else 'PURCHASE'}: ${op.amount:.2f}"
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
                        frame.extra = [tk.Label(frame, text=f"  - {i.name} (${i.price:.2f})", fg="white", bg="#444") for i in items]
                        for w in frame.extra:
                            w.pack(anchor="w")
                        frame.expanded = True

                tk.Button(op_frame, text="Expand", command=toggle).pack(side="right")

    # --- Tab 3: Pie Stats ---
    def setup_tab_pie(self):
        self.pie_frame = tk.Frame(self.tab_pie, bg="#323232")
        self.pie_frame.pack(fill="both", expand=True)

        self.timeframe = ttk.Combobox(self.tab_pie, values=["Day", "Week", "Month", "Year"])
        self.timeframe.set("Week")
        self.timeframe.pack()
        tk.Button(self.tab_pie, text="Update Chart", command=self.draw_pie).pack()

    def draw_pie(self):
        for widget in self.pie_frame.winfo_children():
            widget.destroy()

        tf = self.timeframe.get()
        now = datetime.now()
        if tf == "Day":
            cutoff = now - timedelta(days=1)
        elif tf == "Week":
            cutoff = now - timedelta(weeks=1)
        elif tf == "Month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = now - timedelta(days=365)

        filtered = [op for op in self.history if op.kind == 'purchase' and op.timestamp >= cutoff]
        type_totals = {}
        for op in filtered:
            for item in op.items:
                type_totals[item.typ] = type_totals.get(item.typ, 0) + item.price

        if not type_totals:
            tk.Label(self.pie_frame, text="No data", fg="white", bg="#323232").pack()
            return

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(type_totals.values(), labels=type_totals.keys(), autopct='%1.1f%%')
        canvas = FigureCanvasTkAgg(fig, master=self.pie_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # --- Tab 4: Line Graph ---
    def setup_tab_graph(self):
        self.graph_frame = tk.Frame(self.tab_graph, bg="#323232")
        self.graph_frame.pack(fill="both", expand=True)

        self.timeframe2 = ttk.Combobox(self.tab_graph, values=["Week", "Month", "Year"])
        self.timeframe2.set("Month")
        self.timeframe2.pack()
        tk.Button(self.tab_graph, text="Update Graph", command=self.draw_graph).pack()

    def draw_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        tf = self.timeframe2.get()
        now = datetime.now()
        if tf == "Week":
            cutoff = now - timedelta(weeks=1)
        elif tf == "Month":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = now - timedelta(days=365)

        dates = [cutoff + timedelta(days=i) for i in range((now - cutoff).days + 1)]
        income_data = []
        expense_data = []

        for day in dates:
            day_total_income = sum(op.amount for op in self.history if op.kind == 'income' and op.timestamp.date() == day.date())
            day_total_expense = sum(op.amount for op in self.history if op.kind == 'purchase' and op.timestamp.date() == day.date())
            income_data.append(day_total_income)
            expense_data.append(day_total_expense)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, income_data, label="Income", color="green")
        ax.plot(dates, expense_data, label="Expense", color="red")
        ax.legend()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# --- Run the app ---
if __name__ == '__main__':
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
