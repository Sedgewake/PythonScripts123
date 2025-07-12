import tkinter as tk

# Segment configurations for digits 0–9 (A-G)
SEGMENTS = {
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

# Segment coordinates: each is a polygon
SEGMENT_COORDS = {
    'A': [(20, 10), (80, 10), (70, 20), (30, 20)],
    'B': [(80, 10), (90, 20), (90, 80), (80, 70)],
    'C': [(80, 90), (90, 100), (90, 160), (80, 150)],
    'D': [(20, 160), (80, 160), (70, 150), (30, 150)],
    'E': [(10, 90), (20, 100), (20, 160), (10, 150)],
    'F': [(10, 10), (20, 20), (20, 80), (10, 70)],
    'G': [(20, 80), (30, 70), (70, 70), (80, 80), (70, 90), (30, 90)]
}

class SevenSegmentDisplay:
    def __init__(self, canvas, x_offset=0, y_offset=0):
        self.canvas = canvas
        self.segments = {}
        for name, coords in SEGMENT_COORDS.items():
            shifted_coords = [(x + x_offset, y + y_offset) for x, y in coords]
            poly = canvas.create_polygon(shifted_coords, fill="grey", outline="black")
            self.segments[name] = poly

    def display(self, digit):
        states = SEGMENTS.get(str(digit), [0]*7)
        for seg_name, state in zip("ABCDEFG", states):
            self.canvas.itemconfig(self.segments[seg_name], fill="red" if state else "grey")

# Create main window
root = tk.Tk()
root.title("7 Segment Display")

canvas = tk.Canvas(root, width=200, height=200, bg="white")
canvas.pack()

display = SevenSegmentDisplay(canvas)

# Change the digit here
display.display(5)

root.mainloop()
