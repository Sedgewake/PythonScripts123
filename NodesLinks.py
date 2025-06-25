import tkinter as tk
from tkinter import simpledialog, Toplevel, Text, Scrollbar, messagebox
import json
import os

SAVE_FILE = "nodes.json"

class Node:
    def __init__(self, app, canvas, x, y, text="New Node", note=""):
        self.app = app
        self.canvas = canvas
        self.text = text
        self.note = note
        self.x = x
        self.y = y
        self.width = 100
        self.height = 40
        self.tooltip = None
        self.deleted = False

        self.rect = canvas.create_rectangle(x, y, x + self.width, y + self.height, fill="lightblue", tags="node")
        self.label = canvas.create_text(x + self.width // 2, y + self.height // 2, text=text, tags="node")
        self.note_button = canvas.create_text(x + self.width - 10, y + 10, text="📝", tags="node", font=("Arial", 10))
        self.link_button = canvas.create_oval(x + self.width - 10, y + self.height - 10,
                                              x + self.width - 2, y + self.height - 2,
                                              fill="black", tags="node")

        self._bind_events()

    def _bind_events(self):
        for item in (self.rect, self.label, self.note_button):
            self.canvas.tag_bind(item, "<ButtonPress-1>", self.on_press)
            self.canvas.tag_bind(item, "<B1-Motion>", self.on_drag)
            self.canvas.tag_bind(item, "<Button-3>", self.confirm_delete)
            self.canvas.tag_bind(item, "<Double-1>", self.edit_text)
            self.canvas.tag_bind(item, "<Enter>", self.show_tooltip)
            self.canvas.tag_bind(item, "<Leave>", self.hide_tooltip)

        self.canvas.tag_bind(self.note_button, "<Button-1>", self.open_note_editor)

        self.canvas.tag_bind(self.link_button, "<ButtonPress-1>", self.start_link)
        self.canvas.tag_bind(self.link_button, "<Enter>", self.show_tooltip)
        self.canvas.tag_bind(self.link_button, "<Leave>", self.hide_tooltip)

    def center(self):
        coords = self.canvas.coords(self.rect)
        return (coords[0] + self.width // 2, coords[1] + self.height // 2)

    def start_link(self, event):
        self.app.start_link_from(self, event)

    def on_press(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        for item in (self.rect, self.label, self.note_button, self.link_button):
            self.canvas.move(item, dx, dy)
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.app.draw_links()

    def confirm_delete(self, event):
        confirm = messagebox.askokcancel("Delete Node", "Are you sure you want to delete this node?")
        if confirm:
            self.delete()
            self.app.draw_links()

    def delete(self):
        for item in (self.rect, self.label, self.note_button, self.link_button):
            self.canvas.delete(item)
        self.deleted = True

    def edit_text(self, event):
        new_text = simpledialog.askstring("Edit Node", "Enter new text:", initialvalue=self.text)
        if new_text:
            self.text = new_text
            self.canvas.itemconfig(self.label, text=new_text)

    def open_note_editor(self, event=None):
        editor = Toplevel(self.canvas)
        editor.title("Edit Note")
        editor.geometry("300x200")
        editor.transient(self.canvas.winfo_toplevel())

        text_area = Text(editor, wrap="word")
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

    def show_tooltip(self, event):
        if self.note.strip():
            self.tooltip = Toplevel(self.canvas)
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            preview = self.note.split("\n")[0][:50] + ("..." if len(self.note) > 50 else "")
            label = tk.Label(self.tooltip, text=preview, bg="yellow", relief="solid", borderwidth=1)
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
            "note": self.note
        }

class NodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Node Editor")
        self.nodes = []
        self.links = []
        self.temp_link_line = None
        self.link_start_node = None

        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.toolbar, text="Add Node", command=self.add_node).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.toolbar, text="Save", command=self.save_nodes).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.toolbar, text="Load", command=self.load_nodes).pack(side=tk.LEFT, padx=5, pady=5)

        self.canvas = tk.Canvas(root, bg="#323232", width=1750, height=850, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<ButtonRelease-1>", self.complete_link)
        self.canvas.bind("<Motion>", self.track_temp_link)

        self.draw_background()
        self.load_nodes()

    def add_node(self, x=120, y=120, text="New Node", note=""):
        node = Node(self, self.canvas, x, y, text=text, note=note)
        self.nodes.append(node)

    def start_link_from(self, node, event):
        self.link_start_node = node
        x, y = node.center()
        self.temp_link_line = self.canvas.create_line(x, y, x, y, fill="white", dash=(4, 2), width=2)

    def track_temp_link(self, event):
        if self.temp_link_line:
            x0, y0 = self.link_start_node.center()
            self.canvas.coords(self.temp_link_line, x0, y0, event.x, event.y)

    def complete_link(self, event):
        if not self.temp_link_line:
            return
        end_node = self.find_node_at(event.x, event.y)
        if end_node and end_node != self.link_start_node:
            self.links.append((self.link_start_node, end_node))
        self.canvas.delete(self.temp_link_line)
        self.temp_link_line = None
        self.link_start_node = None
        self.draw_links()

    def find_node_at(self, x, y):
        for node in self.nodes:
            if node.deleted:
                continue
            coords = self.canvas.coords(node.rect)
            if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                return node
        return None

    def draw_links(self):
        self.canvas.delete("link")
        for from_node, to_node in self.links:
            if from_node.deleted or to_node.deleted:
                continue
            x0, y0 = from_node.center()
            x1, y1 = to_node.center()
            self.canvas.create_line(x0, y0, x1, y1, fill="white", width=2, tags="link")

    def save_nodes(self):
        data = {
            "nodes": [node.to_dict() for node in self.nodes if not node.deleted],
            "links": [
                {"from": self.nodes.index(from_node), "to": self.nodes.index(to_node)}
                for from_node, to_node in self.links
                if not from_node.deleted and not to_node.deleted
            ]
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Saved", f"{len(data['nodes'])} node(s) saved to {SAVE_FILE}")

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
        if isinstance(data, list):  # old format
            for node_data in data:
                self.add_node(**node_data)
            self.links = []
        else:
            for node_data in data["nodes"]:
                self.add_node(**node_data)
            self.links = []
            for link in data.get("links", []):
                try:
                    from_node = self.nodes[link["from"]]
                    to_node = self.nodes[link["to"]]
                    self.links.append((from_node, to_node))
                except IndexError:
                    pass
            self.draw_links()

    def clear_all_nodes(self):
        for node in self.nodes:
            node.delete()
        self.nodes.clear()
        self.links.clear()
        self.canvas.delete("link")

    def draw_background(self):
        self.canvas.delete("bg")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx = w // 2
        cy = h

        arc_radii = [250, 450, 650]
        for r in arc_radii:
            self.canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                                   start=0, extent=180,
                                   outline="#888", width=2, style=tk.ARC, tags="bg")

    def on_resize(self, event):
        self.draw_background()

if __name__ == "__main__":
    root = tk.Tk()
    app = NodeEditorApp(root)
    root.mainloop()
