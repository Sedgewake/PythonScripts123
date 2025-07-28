import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

matplotlib.use("Agg")

class Item:
    def __init__(self, name, item_type, price):
        self.name = name
        self.item_type = item_type
        self.price = price

class FinanceCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Calculator")
        self.root.resizable(False, False)
        self.root.geometry("900x600")
        self.root.configure(background="#323232")
        self.balance = 1230
        self.balance_var = tk.StringVar()
        self.income_amount = None
        self.income_type = None
        self.item_selector = None
        self.available_items = []
        self.available_items.append(Item("Apple", "Food", 3000))
        self.available_items.append(Item("ESP32", "Tech", 52000))

        self.balance_var.set(f"Balance: {float(self.balance / 100):.2f} ₽")

        style = ttk.Style()
        #style.theme_use("clam")
        style.theme_use("default")
        style.configure("TNotebook", background="#323232", borderwidth=0)
        style.configure("TNotebook.Tab", background="#323232", foreground="#e6e6e6", padding=(12, 8), font=('Segoe UI', 10, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", "#3a3a3a")], foreground=[("selected", "#ffffff")])
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

        self.setup_tab_main()
        self.setup_tab_history()
        self.setup_tab_pie()
        self.setup_tab_graph()

    def setup_tab_main(self):
        tab = tk.Frame(self.notebook, bg="#323232")
        tk.Label(tab, textvariable=self.balance_var, font=("Arial", 20), fg="white", bg="#323232").pack(pady=5)
        income_frame = tk.Frame(tab, bg="#323232")
        income_frame.pack(pady=5)
        tk.Label(income_frame, text="Income:", font=("Arial", 20), fg="white", bg="#323232").pack(side="left")
        self.income_amount = tk.Entry(income_frame, font=("Arial", 20), width=15)
        self.income_amount.pack(side="left", padx=5)
        self.income_type = ttk.Combobox(income_frame, values=["Salary", "Gift", "Other"], font=("Arial", 20), height=20, width=10)
        self.income_type.set("Salary")
        self.income_type.pack(side="left", padx=5)
        tk.Button(income_frame, text="Check In", font=("Arial", 14), command=self.add_income).pack(side="left", padx=5)
        select_frame = tk.Frame(tab, bg="#ff3232")
        select_frame.pack(pady=5)
        self.item_selector = ttk.Combobox(select_frame, values=[item.name for item in self.available_items], font=("Arial", 20), height=20, width=10)
        self.item_selector.set("")
        self.item_selector.pack(side="left")
        #tk.Label(select_frame, textvariable=self.balance_var, font=("Arial", 20), fg="white", bg="#323232").pack(pady=5)

        self.notebook.add(tab, text="Main")

    def setup_tab_history(self):
        tab = tk.Frame(self.notebook, bg="#323232")

        self.notebook.add(tab, text="History")

    def setup_tab_pie(self):
        tab = tk.Frame(self.notebook, bg="#323232")

        self.notebook.add(tab, text="Chart")

    def setup_tab_graph(self):
        tab = tk.Frame(self.notebook, bg="#323232")

        self.notebook.add(tab, text="Graph")

    def add_income(self):
        print("Adding Income")
        try:
            amount = int(float(self.income_amount.get()) * 100.0)
        except ValueError:
            return
        self.balance += amount
        self.income_amount.delete(0, tk.END)
        self.balance_var.set(f"Balance: {float(self.balance / 100):.2f} ₽")





if __name__ == "__main__":
    main_window = tk.Tk()
    app = FinanceCalcApp(main_window)
    main_window.mainloop()
