import tkinter as tk
from tkinter import simpledialog, Toplevel, Text, Scrollbar, messagebox, colorchooser
import json
import os

SAVE_FILE = "nodes.json"

class Node:
    def __init__(self, canvas, x, y, text="New Node", note="", color="lightblue"):
        self.canvas = canvas
        self.text = text
        self.note = note
        self.color = color
        self.x = x
        self.y = y
        self.height = 40
        self.tooltip = None
        self.deleted = False

        self.width = self.calculate_width(text)
        self.rect = canvas.create_rectangle(x, y, x + self.width, y + self.height, fill=self.color, tags="node")
        self.label = canvas.create_text(x + self.width // 2, y + self.height // 2, text=text, tags="node")
        self.note_button = canvas.create_text(x + self.width - 10, y + 10, text="📝", tags="node", font=("Arial", 10))
        self.color_button = canvas.create_text(x + 10, y + 10, text="🎨", tags="node", font=("Arial", 10))

        self._bind_events()

    def calculate_width(self, text):
        return max(100, 10 + len(text) * 8)

    def _bind_events(self):
        for item in (self.rect, self.label, self.note_button, self.color_button):
            self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_press)
            self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
            self.canvas.tag_bind(item, "<Button-3>", self.confirm_delete)
            self.canvas.tag_bind(item, "<Double-1>", self.edit_text)
            self.canvas.tag_bind(item, "<Enter>", self.show_tooltip)
            self.canvas.tag_bind(item, "<Leave>", self.hide_tooltip)

        self.canvas.tag_bind(self.note_button, "<Button-1>", self.open_note_editor)
        self.canvas.tag_bind(self.color_button, "<Button-1>", self.pick_color)

    def on_press(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        for item in (self.rect, self.label, self.note_button, self.color_button):
            self.canvas.move(item, dx, dy)
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def confirm_delete(self, event):
        confirm = messagebox.askokcancel("Delete Node", "Are you sure you want to delete this node?")
        if confirm:
            self.delete()

    def delete(self):
        for item in (self.rect, self.label, self.note_button, self.color_button):
            self.canvas.delete(item)
        self.deleted = True

    def edit_text(self, event):
        new_text = simpledialog.askstring("Edit Node", "Enter new text:", initialvalue=self.text)
        if new_text:
            self.text = new_text
            self.canvas.itemconfig(self.label, text=new_text)
            new_width = self.calculate_width(new_text)
            coords = self.canvas.coords(self.rect)
            self.canvas.coords(self.rect, coords[0], coords[1], coords[0] + new_width, coords[3])
            self.width = new_width
            self.canvas.coords(self.label, coords[0] + new_width // 2, coords[1] + self.height // 2)
            self.canvas.coords(self.note_button, coords[0] + new_width - 10, coords[1] + 10)

    def open_note_editor(self, event=None):
        editor = Toplevel(self.canvas)
        editor.title("Edit Note")

        if event:
            editor.geometry(f"300x200+{event.x_root}+{event.y_root}")
        else:
            editor.geometry("300x200")

        editor.transient(self.canvas.winfo_toplevel())
        editor.configure(bg="#323232")

        text_area = Text(editor, wrap="word", bg="#323232", fg="white", insertbackground="white")
        text_area.insert("1.0", self.note)
        text_area.pack(expand=True, fill="both")

        scrollbar = Scrollbar(text_area)
        scrollbar.pack(side="right", fill="y")
        text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_area.yview)

        def save_and_close():
            self.note = text_area.get("1.0", "end-1c")
            editor.destroy()

        editor.protocol("WM_DELETE_WINDOW", save_and_close)

    def pick_color(self, event=None):
        color = colorchooser.askcolor(title="Choose Node Color", initialcolor=self.color)[1]
        if color:
            self.color = color
            self.canvas.itemconfig(self.rect, fill=self.color)

    def show_tooltip(self, event):
        if self.note.strip():
            self.tooltip = Toplevel(self.canvas)
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            preview = self.note.split("\n")[0][:50] + ("..." if len(self.note) > 50 else "")
            label = tk.Label(self.tooltip, text=preview, bg="lightblue", relief="solid", borderwidth=1)
            label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def to_dict(self):
        coords = self.canvas.coords(self.rect)
        return {
            "x": coords[0],
            "y": coords[1],
            "text": self.text,
            "note": self.note,
            "color": self.color
        }

class NodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Node Editor")
        self.nodes = []

        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.toolbar, text="Add Node", command=self.add_node).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.toolbar, text="Save", command=self.save_nodes).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.toolbar, text="Load", command=self.load_nodes).pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(root, bg="#323232", width=1750, height=850, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        self.draw_background()
        self.load_nodes()

    def add_node(self, x=120, y=120, text="New Node", note="", color="lightblue"):
        node = Node(self.canvas, x, y, text=text, note=note, color=color)
        self.nodes.append(node)

    def save_nodes(self):
        data = [node.to_dict() for node in self.nodes if not node.deleted]
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", f"{len(data)} node(s) saved to {SAVE_FILE}")

    def load_nodes(self):
        if not os.path.exists(SAVE_FILE):
            return
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Failed to load nodes. Invalid JSON.")
                return
        self.clear_all_nodes()
        for node_data in data:
            self.add_node(**node_data)

    def clear_all_nodes(self):
        for node in self.nodes:
            node.delete()
        self.nodes.clear()

    def draw_background(self):
        self.canvas.delete("bg")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx = w // 2
        cy = h

        arcs = [
            (250, "#62cc6a"),
            (450, "#ede774"),
            (650, "#d04a4a")
        ]
        for r, color in arcs:
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                                   start=0, extent=180,
                                   outline=color, width=2, style=tk.ARC, tags="bg")

    def on_resize(self, event):
        self.draw_background()

if __name__ == "__main__":
    root = tk.Tk()
    app = NodeEditorApp(root)
    root.mainloop()
