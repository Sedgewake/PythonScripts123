
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

        self.graph_lines = {}  # To keep track of which lines are visible
        self.color_palette = [
            "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4",
            "#46f0f0", "#f032e6", "#bcf60c", "#fabebe", "#008080", "#e6beff",
            "#9a6324", "#fffac8", "#800000", "#aaffc3", "#808000", "#ffd8b1",
            "#000075", "#808080", "#ffffff", "#000000", "#c0c0c0", "#ff69b4",
            "#cd853f", "#7fffd4", "#ff4500", "#dda0dd", "#90ee90", "#add8e6"
        ]

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

    # [Rest of the setup_tab_balance, income functions, history and pie setup unchanged]
    # Only draw_graph and setup_tab_graph will be modified from previous version

    def setup_tab_graph(self):
        self.graph_container = tk.Frame(self.tab_graph, bg="#323232")
        self.graph_container.pack(fill="both", expand=True)

        self.toolbar = tk.Frame(self.graph_container, bg="#2a2a2a", width=200)
        self.toolbar.pack(side="left", fill="y")

        self.graph_frame = tk.Frame(self.graph_container, bg="#323232")
        self.graph_frame.pack(side="left", fill="both", expand=True)

        self.timeframe2 = ttk.Combobox(self.toolbar, values=["Week", "Month", "Year"])
        self.timeframe2.set("Month")
        self.timeframe2.pack(pady=5)

        tk.Button(self.toolbar, text="Update Graph", command=self.draw_graph).pack(pady=5)
        self.line_check_vars = {}
        self.line_colors = {}

    def draw_graph(self):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        for widget in self.toolbar.winfo_children():
            if isinstance(widget, tk.Checkbutton):
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
        income_types = set(op.kind if op.kind == "income" else item.typ for op in self.history for item in op.items if op.kind == "purchase")
        purchase_types = set(item.typ for op in self.history if op.kind == "purchase" for item in op.items)
        income_entries = set(op.kind for op in self.history if op.kind == "income")

        categories = list(purchase_types | income_entries) + ["Total income", "Total expense"]

        for cat in categories:
            var = tk.BooleanVar(value=(cat in ["Total income", "Total expense"]))
            cb = tk.Checkbutton(self.toolbar, text=cat, variable=var, bg="#2a2a2a", fg="white", selectcolor="#444444",
                                command=self.draw_graph)
            cb.pack(anchor="w")
            self.line_check_vars[cat] = var
            if cat not in self.line_colors:
                self.line_colors[cat] = random.choice(self.color_palette)

        fig, ax = plt.subplots(figsize=(7, 5))

        for cat, var in self.line_check_vars.items():
            if not var.get():
                continue
            ydata = []
            for day in dates:
                if cat == "Total income":
                    val = sum(op.amount for op in self.history if op.kind == "income" and op.timestamp.date() == day.date())
                elif cat == "Total expense":
                    val = sum(op.amount for op in self.history if op.kind == "purchase" and op.timestamp.date() == day.date())
                elif cat in purchase_types:
                    val = sum(item.price for op in self.history if op.kind == "purchase" and op.timestamp.date() == day.date()
                              for item in op.items if item.typ == cat)
                elif cat in income_entries:
                    val = sum(op.amount for op in self.history if op.kind == "income" and op.timestamp.date() == day.date())
                else:
                    val = 0
                ydata.append(val)
            ax.plot(dates, ydata, label=cat, color=self.line_colors.get(cat, 'gray'))

        ax.legend()
        fig.autofmt_xdate()
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
