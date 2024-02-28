import tkinter as tk
import math

def start_rotation(event):
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def rotate(event):
    global start_x, start_y, item_id
    current_x = event.x
    current_y = event.y
    dx = current_x - start_x
    dy = current_y - start_y

    # Calculate rotation angle
    angle = math.degrees(math.atan2(dy, dx))

    # Rotate the canvas item
    canvas.coords(item_id, *original_coords)
    canvas.rotate(item_id, angle, (start_x, start_y))

def stop_rotation(event):
    pass

class MyCanvas(tk.Canvas):
    def rotate(self, item, angle, origin):
        coords = self.coords(item)
        origin_x, origin_y = origin
        angle_rad = math.radians(angle)
        rotated_coords = []
        for i in range(0, len(coords), 2):
            x = coords[i]
            y = coords[i+1]
            rel_x = x - origin_x
            rel_y = y - origin_y
            new_x = rel_x * math.cos(angle_rad) - rel_y * math.sin(angle_rad) + origin_x
            new_y = rel_x * math.sin(angle_rad) + rel_y * math.cos(angle_rad) + origin_y
            rotated_coords.extend([new_x, new_y])
        self.coords(item, *rotated_coords)

root = tk.Tk()
canvas = MyCanvas(root, width=400, height=400, bg="white")
canvas.pack()

# Draw a rectangle on the canvas
item_id = canvas.create_rectangle(100, 100, 200, 200, fill="blue")

original_coords = canvas.coords(item_id)

canvas.bind("<ButtonPress-1>", start_rotation)
canvas.bind("<B1-Motion>", rotate)
canvas.bind("<ButtonRelease-1>", stop_rotation)

root.mainloop()
