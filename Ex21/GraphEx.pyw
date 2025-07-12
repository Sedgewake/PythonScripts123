#pip install matplotlib

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import matplotlib
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

matplotlib.use("Agg")  # Use non-interactive backend

class DarkTabbedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tabbed App with Editor, Pie Chart, and Graph")
        self.root.geometry("900x600")
        self.root.configure(bg="#323232")

        style = ttk.Style()
        style.theme_use("default")
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

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=2, pady=2)

        self.add_text_editor_tab()
        self.add_pie_chart_tab()
        self.add_graph_tab()

    def add_text_editor_tab(self):
        tab = ttk.Frame(self.notebook)
        text_editor = scrolledtext.ScrolledText(tab,
                                                bg="#2b2b2b",
                                                fg="#e6e6e6",
                                                insertbackground="#ffffff",
                                                selectbackground="#555555",
                                                wrap="word")
        text_editor.pack(fill="both", expand=True)
        self.notebook.add(tab, text="Editor")

    def add_pie_chart_tab(self):
        tab = ttk.Frame(self.notebook)
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        ax.set_facecolor("#323232")
        fig.patch.set_facecolor("#323232")

        labels = ['A', 'B', 'C', 'D']
        sizes = [random.randint(10, 40) for _ in labels]
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']

        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', textprops={'color': 'white'})
        ax.set_title("Random Pie Chart", color='white')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.notebook.add(tab, text="Pie Chart")

    def add_graph_tab(self):
        tab = ttk.Frame(self.notebook)
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.set_facecolor("#323232")
        fig.patch.set_facecolor("#323232")

        x = list(range(10))
        y1 = [random.randint(0, 10) for _ in x]
        y2 = [random.randint(0, 10) for _ in x]

        ax.plot(x, y1, label="Data 1", color="#ff6666")
        ax.plot(x, y2, label="Data 2", color="#66ffcc")

        ax.legend()
        ax.set_title("Random Line Graph", color='white')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.notebook.add(tab, text="Graph")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DarkTabbedApp(root)
    root.mainloop()