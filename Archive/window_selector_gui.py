
import tkinter as tk

class WindowSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.coords = None

    def start_selection(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.root.configure(bg='blue')
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="blue")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.root.mainloop()
        return self.coords

    def on_mouse_down(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_mouse_up(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        self.coords = (
            int(min(self.start_x, end_x)),
            int(min(self.start_y, end_y)),
            int(max(self.start_x, end_x)),
            int(max(self.start_y, end_y))
        )
        self.root.destroy()
