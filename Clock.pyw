import tkinter as tk
import time

# Segment layout for each digit (A-G)
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
    '9': [1,1,1,1,0,1,1],
    ':': [0,0,0,0,0,0,0],  # Colon handled separately
    ' ': [0,0,0,0,0,0,0]
}

# Polygon coordinates for each segment (A–G)
SEGMENT_COORDS = {
    'A': [(10, 5), (90, 5), (75, 20), (25, 20)],
    'B': [(75, 20), (90, 5), (90, 85), (75, 75)],
    'C': [(75, 95), (90, 85), (90, 165), (75, 150)],
    'D': [(10, 165), (90, 165), (75, 150), (25, 150)],
    'E': [(10, 85), (25, 95), (25, 150), (10, 165)],
    'F': [(10, 5), (25, 20), (25, 75), (10, 85)],
    'G': [(10, 85), (25, 75), (75, 75), (90, 85), (75, 95), (25, 95)],
}

class SevenSegmentDigit:
    def __init__(self, canvas, x_offset, y_offset):
        self.canvas = canvas
        self.segments = {}
        self.x_offset = x_offset
        self.y_offset = y_offset
        for name, coords in SEGMENT_COORDS.items():
            shifted = [(x + x_offset, y + y_offset) for x, y in coords]
            self.segments[name] = canvas.create_polygon(
                shifted, fill='grey20', outline='#323232', width=1
            )

    def display(self, char):
        if char not in SEGMENTS:
            char = ' '
        states = SEGMENTS[char]
        for name, state in zip("ABCDEFG", states):
            color = 'lightblue' if state else '#2e2e2e'
            self.canvas.itemconfig(self.segments[name], fill=color)

class Colon:
    def __init__(self, canvas, x_offset, y_offset):
        self.canvas = canvas
        r = 2
        self.top = canvas.create_oval(x_offset+r, y_offset+50+r, x_offset+20-r, y_offset+50+20-r, fill='blue', outline='')
        self.bottom = canvas.create_oval(x_offset+r, y_offset+110+r, x_offset+20-r, y_offset+110+20-r, fill='blue', outline='')

    def blink(self, visible):
        color = 'lightblue' if True else '#2e2e2e'
        self.canvas.itemconfig(self.top, fill=color)
        self.canvas.itemconfig(self.bottom, fill=color)

class SevenSegmentClockApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=200, bg='#323232', highlightthickness=0)
        self.canvas.pack()

        self.digits = []
        x = 10
        for i in range(8):
            if i in [2, 5]:  # Colons
                self.digits.append(Colon(self.canvas, x, 0))
                x += 30
            else:
                self.digits.append(SevenSegmentDigit(self.canvas, x, 10))
                x += 100

        self.blink_state = True
        self.update_clock()

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        for i, char in enumerate(now):
            if char == ':':
                self.digits[i].blink(self.blink_state)
            else:
                self.digits[i].display(char)

        self.blink_state = not self.blink_state
        self.root.after(500, self.update_clock)

# Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    root.title("7-Segment Clock")
    app = SevenSegmentClockApp(root)
    root.mainloop()
