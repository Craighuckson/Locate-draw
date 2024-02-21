import tkinter as tk


class DraggableObjects:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Draw two objects
        self.rect = self.canvas.create_rectangle(50, 50, 100, 100, fill='blue')
        self.oval = self.canvas.create_oval(200, 200, 250, 250, fill='red')

        # Bind the mouse events to the handlers
        self.canvas.bind("<Button-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)

        # Initialize instance variables
        self.last_x = 0
        self.last_y = 0
        self.dragged_item = None

    def on_drag_start(self, event):
        # Store the ID of the object being dragged and its location
        self.dragged_item = self.canvas.find_closest(event.x, event.y)[0]
        self.last_x = event.x
        self.last_y = event.y

    def on_drag_motion(self, event):
        # Compute how much the mouse has moved
        dx = event.x - self.last_x
        dy = event.y - self.last_y
        # Move the object the same distance as the mouse
        self.canvas.move(self.dragged_item, dx, dy)
        # Store the current mouse position for the next motion event
        self.last_x = event.x
        self.last_y = event.y


root = tk.Tk()
app = DraggableObjects(root)
root.mainloop()
