import tkinter as tk
from tkinter import messagebox
import pyperclip  # Make sure to install: pip install pyperclip

# Initial default coordinates
SEGMENT_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
DEFAULT_COORDS = {
    'A': [(20, 10), (80, 10), (70, 20), (30, 20)],
    'B': [(80, 10), (90, 20), (90, 80), (80, 70)],
    'C': [(80, 90), (90,100), (90,160), (80,150)],
    'D': [(20,160), (80,160), (70,150), (30,150)],
    'E': [(10, 90), (20,100), (20,160), (10,150)],
    'F': [(10, 10), (20, 20), (20, 80), (10, 70)],
    'G': [(20, 80), (30, 70), (70, 70), (80, 80), (70, 90), (30, 90)]
}

DIGIT_MAP = {
    '0': [1,1,1,1,1,1,0],
    '1': [0,1,1,0,0,0,0],
    '2': [1,1,0,1,1,0,1],
    '3': [1,1,1,1,0,0,1],
    '4': [0,1,1,0,0,1,1],
    '5': [1,0,1,1,0,1,1],
    '6': [1,0,1,1,1,1,1],
    '7': [1,1,1,0,0,0,0],
    '8': [1,1,1,1,1,1,1],
    '9': [1,1,1,1,0,1,1]
}

class SegmentEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("7-Segment Editor")
        self.canvas = tk.Canvas(root, width=200, height=200, bg="#323232")
        self.canvas.grid(row=0, column=0, rowspan=20)

        self.coord_entries = {}
        self.segments = {}
        self.segment_coords = {k: list(v) for k, v in DEFAULT_COORDS.items()}

        # Create entry fields for each segment's coordinates
        for i, name in enumerate(SEGMENT_NAMES):
            tk.Label(root, text=f"{name}:").grid(row=i, column=1, sticky="e")
            entry = tk.Entry(root, width=35)
            entry.insert(0, str(self.segment_coords[name]))
            entry.grid(row=i, column=2, padx=5, pady=2)
            self.coord_entries[name] = entry

        # Input digit
        tk.Label(root, text="Digit (0-9):").grid(row=8, column=1, sticky="e")
        self.digit_entry = tk.Entry(root, width=5)
        self.digit_entry.grid(row=8, column=2, sticky="w")
        self.digit_entry.insert(0, "8")

        # Buttons
        tk.Button(root, text="Update Display", command=self.update_display).grid(row=9, column=2, sticky="w")
        tk.Button(root, text="Copy Coords to Clipboard", command=self.copy_to_clipboard).grid(row=10, column=2, sticky="w")

        self.draw_segments()
        self.update_display()

    def draw_segments(self):
        for name in SEGMENT_NAMES:
            coords = self.segment_coords[name]
            self.segments[name] = self.canvas.create_polygon(coords, fill="blue", outline="black")

    def update_display(self):
        # Parse coordinates from entries
        for name in SEGMENT_NAMES:
            try:
                text = self.coord_entries[name].get()
                coords = eval(text)
                if not all(isinstance(x, (list, tuple)) and len(x) == 2 for x in coords):
                    raise ValueError
                self.segment_coords[name] = coords
                self.canvas.coords(self.segments[name], *sum(coords, ()))
            except Exception:
                messagebox.showerror("Invalid Input", f"Invalid coordinates for segment {name}")
                return

        digit = self.digit_entry.get().strip()
        if digit not in DIGIT_MAP:
            messagebox.showerror("Invalid Digit", "Please enter a digit from 0 to 9.")
            return

        # Update colors
        on_segments = DIGIT_MAP[digit]
        for name, is_on in zip(SEGMENT_NAMES, on_segments):
            self.canvas.itemconfig(self.segments[name], fill="blue" if is_on else "#1e1e1e")

    def copy_to_clipboard(self):
        formatted = "SEGMENT_COORDS = {\n"
        for name in SEGMENT_NAMES:
            coords = self.segment_coords[name]
            formatted += f"    '{name}': {coords},\n"
        formatted += "}"
        pyperclip.copy(formatted)
        messagebox.showinfo("Copied", "Segment coordinates copied to clipboard.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SegmentEditorApp(root)
    root.mainloop()
