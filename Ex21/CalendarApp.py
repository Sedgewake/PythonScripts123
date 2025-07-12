import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime, timedelta
import calendar
import random

COLORS = [
    "#e6194b", "#3cb44b", "#ffe119", "#0082c8", "#f58231", "#911eb4", "#46f0f0",
    "#f032e6", "#d2f53c", "#fabebe", "#008080", "#e6beff", "#aa6e28", "#fffac8",
    "#800000", "#aaffc3", "#808000", "#ffd8b1", "#000080", "#808080", "#ffffff",
    "#000000", "#ffd700", "#cd5c5c", "#4b0082", "#7fffd4", "#ff69b4", "#1e90ff",
    "#ff4500", "#90ee90"
]

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar App")
        self.root.geometry("870x700")
        self.root.configure(bg="#323232")
        self.current_date = datetime.today()
        self.setup_ui()

    def setup_ui(self):
        self.header = tk.Frame(self.root, bg="#323232")
        self.header.pack(fill=tk.X)

        self.prev_btn = tk.Button(self.header, text="<", command=self.prev_month, bg="#444", fg="white")
        self.prev_btn.pack(side=tk.LEFT, padx=10)

        self.month_label = tk.Label(self.header, text="", font=("Arial", 25), bg="#323232", fg="white")
        self.month_label.pack(side=tk.TOP, padx=20)

        self.next_btn = tk.Button(self.header, text=">", command=self.next_month, bg="#444", fg="white")
        self.next_btn.pack(side=tk.RIGHT)

        self.calendar_frame = tk.Frame(self.root, bg="#323232")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH)

        self.draw_calendar()

    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        year = self.current_date.year
        month = self.current_date.month
        self.month_label.config(text=self.current_date.strftime("%B %Y"))

        cal = calendar.Calendar()
        days = list(cal.itermonthdays2(year, month))

        row = 1
        for i, (day, weekday) in enumerate(days):
            if day == 0:
                continue
            date = datetime(year, month, day)
            btn = tk.Label(
                self.calendar_frame,
                text=str(day),
                font=("Arial", 30),  # 👈 change number here for size
                width=5,
                height=2,
                bg="#666" if weekday >= 5 else "#323232",
                fg="white",
                borderwidth=1,
                relief="solid"
            )
            if date.date() == datetime.today().date():
                btn.config(bg="#484882")
            btn.grid(row=row, column=weekday, padx=2, pady=2, sticky="nsew")
            btn.bind("<Double-Button-1>", lambda e, d=date: self.open_day_view(d))
            if weekday == 6:
                row += 1

    def prev_month(self):
        self.current_date -= timedelta(days=self.current_date.day)
        self.draw_calendar()

    def next_month(self):
        next_month = self.current_date.replace(day=28) + timedelta(days=4)
        self.current_date = next_month.replace(day=1)
        self.draw_calendar()

    def open_day_view(self, date):
        DayViewWindow(date)

class DayViewWindow:
    def __init__(self, date):
        self.window = tk.Toplevel()
        self.window.title(f"Day View - {date.strftime('%Y-%m-%d')}")
        self.window.geometry("1200x400")
        self.window.configure(bg="#323232")
        self.date = date
        self.start_hour = 0
        self.nodes = []
        self.color_pool = COLORS[:]
        self.canvas_width = 960

        control_frame = tk.Frame(self.window, bg="#323232")
        control_frame.pack(fill=tk.X)

        self.start_entry = tk.Entry(control_frame)
        self.start_entry.pack(side=tk.LEFT, padx=10)
        self.start_entry.insert(0, "0")

        set_btn = tk.Button(control_frame, text="Set Start Hour", command=self.set_start_hour, bg="#444", fg="white")
        set_btn.pack(side=tk.LEFT)

        now_btn = tk.Button(control_frame, text="Set to Now", command=self.set_now, bg="#444", fg="white")
        now_btn.pack(side=tk.LEFT)

        add_btn = tk.Button(control_frame, text="Add Task", command=lambda: self.create_node(100), bg="#444", fg="white")
        add_btn.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self.window, bg="#1e1e1e", height=300, width=self.canvas_width)
        self.canvas.pack(fill=tk.X)

        self.window.after(1000, self.update_time_line)
        self.draw_time_ruler()

    def set_start_hour(self):
        try:
            self.start_hour = float(self.start_entry.get()) % 24
            self.draw_time_ruler()
            self.redraw_nodes()
        except ValueError:
            pass

    def set_now(self):
        now = datetime.now()
        self.start_hour = (now.hour + now.minute / 60.0) % 24
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, str(self.start_hour))
        self.draw_time_ruler()
        self.redraw_nodes()

    def draw_time_ruler(self):
        self.canvas.delete("ruler")
        for h in range(25):
            hour = (self.start_hour + h) % 24
            x = self.hour_to_x(hour)
            self.canvas.create_line(x, 0, x, 300, fill="#aaa", tags="ruler")
            self.canvas.create_text(x + 2, 10, anchor="nw", text=f"{int(hour):02d}", fill="white", tags="ruler")
            hx = self.hour_to_x((hour + 0.5) % 24)
            self.canvas.create_line(hx, 0, hx, 40, fill="#777", tags="ruler")

    def hour_to_x(self, hour):
        delta = (hour - self.start_hour) % 24
        return delta * 50

    def x_to_hour(self, x):
        return (self.start_hour + x / 50.0) % 24

    def update_time_line(self):
        self.canvas.delete("current_time")
        now = datetime.now()
        hour = (now.hour + now.minute / 60.0) % 24
        x = self.hour_to_x(hour)
        self.canvas.create_line(x, 0, x, 300, fill="cyan", width=2, tags="current_time")
        self.window.after(1000, self.update_time_line)

    def create_node(self, x=100):
        hour = self.x_to_hour(x)
        width = 120
        color = self.color_pool.pop(random.randint(0, len(self.color_pool) - 1)) if self.color_pool else random.choice(COLORS)
        node = self.canvas.create_rectangle(x, 60, x + width, 120, fill=color, outline="white", tags="node")
        start_time = self.canvas.create_text(x + 2, 62, anchor="nw", text=f"{hour:.2f}", fill="white", tags="node")
        end_time = self.canvas.create_text(x + width - 2, 62, anchor="ne", text=f"{(hour + width / 40.0) % 24:.2f}", fill="white", tags="node")
        text = self.canvas.create_text(x + width / 2, 80, text="Task", fill="white", tags="node")
        self.nodes.append((node, start_time, end_time, text))
        self.make_interactive(node, start_time, end_time, text)

    def make_interactive(self, rect, start_text, end_text, mid_text):
        drag_data = {"x": 0, "action": None}

        def on_press(event):
            x1, _, x2, _ = self.canvas.coords(rect)
            drag_data["x"] = event.x
            if abs(event.x - x1) <= 20:
                drag_data["action"] = "resize_left"
            elif abs(event.x - x2) <= 20:
                drag_data["action"] = "resize_right"
            else:
                drag_data["action"] = "move"

        def on_drag(event):
            dx = event.x - drag_data["x"]
            x1, y1, x2, y2 = self.canvas.coords(rect)

            if drag_data["action"] == "move":
                new_x1 = x1 + dx
                new_x2 = x2 + dx
                if new_x1 < x2 - 40:
                    self.canvas.coords(rect, new_x1, y1, new_x2, y2)
                    self.canvas.move(end_text, dx, 0)
                    self.canvas.move(start_text, dx, 0)
                    self.canvas.coords(mid_text, (new_x1 + new_x2) / 2, (y1 + y2) / 2)
                drag_data["x"] = event.x

                #self.canvas.move(rect, dx, 0)
                #self.canvas.move(start_text, dx, 0)
                #self.canvas.move(end_text, dx, 0)
                #self.canvas.move(mid_text, dx, 0)
            elif drag_data["action"] == "resize_left":
                new_x1 = x1 + dx
                if new_x1 < x2 - 40:
                    self.canvas.coords(rect, new_x1, y1, x2, y2)
                    self.canvas.move(start_text, dx, 0)
                    self.canvas.coords(mid_text, (new_x1 + x2) / 2, (y1 + y2) / 2)
                drag_data["x"] = event.x
            elif drag_data["action"] == "resize_right":
                new_x2 = x2 + dx
                if new_x2 > x1 + 40:
                    self.canvas.coords(rect, x1, y1, new_x2, y2)
                    self.canvas.move(end_text, dx, 0)
                    self.canvas.coords(mid_text, (x1 + new_x2) / 2, (y1 + y2) / 2)
                drag_data["x"] = event.x

            x1, _, x2, _ = self.canvas.coords(rect)
            self.canvas.itemconfigure(start_text, text=f"{self.x_to_hour(x1):.2f}")
            self.canvas.itemconfigure(end_text, text=f"{self.x_to_hour(x2):.2f}")

        def on_right_click(event):
            if messagebox.askokcancel("Delete", "Delete this task?"):
                self.canvas.delete(rect)
                self.canvas.delete(start_text)
                self.canvas.delete(end_text)
                self.canvas.delete(mid_text)

        def on_double_click(event):
            new_text = simpledialog.askstring("Edit Task", "Enter new text:")
            if new_text:
                self.canvas.itemconfigure(mid_text, text=new_text)

        self.canvas.tag_bind(rect, "<ButtonPress-1>", on_press)
        self.canvas.tag_bind(rect, "<B1-Motion>", on_drag)
        self.canvas.tag_bind(rect, "<Button-3>", on_right_click)
        self.canvas.tag_bind(rect, "<Double-Button-1>", on_double_click)

        self.canvas.tag_bind(mid_text, "<Double-Button-1>", on_double_click)

    def redraw_nodes(self):
        for node in self.nodes:
            rect, start_text, end_text, mid_text = node
            x1, y1, x2, y2 = self.canvas.coords(rect)
            self.canvas.coords(rect, self.hour_to_x(self.x_to_hour(x1)), y1, self.hour_to_x(self.x_to_hour(x2)), y2)
            self.canvas.coords(start_text, self.hour_to_x(self.x_to_hour(x1)) + 2, y1 + 2)
            self.canvas.coords(end_text, self.hour_to_x(self.x_to_hour(x2)) - 2, y1 + 2)
            self.canvas.coords(mid_text, (self.hour_to_x(self.x_to_hour(x1)) + self.hour_to_x(self.x_to_hour(x2))) / 2, (y1 + y2) / 2)

root = tk.Tk()
app = CalendarApp(root)
root.mainloop()
