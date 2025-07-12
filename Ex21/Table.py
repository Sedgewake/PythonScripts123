import tkinter as tk
from tkinter import filedialog, messagebox
import csv

class TableEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("5x10 Table Editor")

        self.rows = 10
        self.columns = 5
        self.entries = []

        self.create_table()
        self.create_buttons()

    def create_table(self):
        for row in range(self.rows):
            row_entries = []
            for col in range(self.columns):
                entry = tk.Entry(self.root, width=15)
                entry.grid(row=row, column=col, padx=1, pady=1)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def create_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=self.rows, column=0, columnspan=self.columns, pady=10)

        load_btn = tk.Button(btn_frame, text="Load", command=self.load_table)
        load_btn.pack(side=tk.LEFT, padx=5)

        save_btn = tk.Button(btn_frame, text="Save", command=self.save_table)
        save_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_table)
        clear_btn.pack(side=tk.LEFT, padx=5)

    def load_table(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                with open(filepath, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    for r, row in enumerate(reader):
                        if r >= self.rows:
                            break
                        for c, cell in enumerate(row):
                            if c < self.columns:
                                self.entries[r][c].delete(0, tk.END)
                                self.entries[r][c].insert(0, cell)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def save_table(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for row in self.entries:
                        writer.writerow([entry.get() for entry in row])
                messagebox.showinfo("Saved", "Table saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def clear_table(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TableEditorApp(root)
    root.mainloop()
