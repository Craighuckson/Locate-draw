from PIL import Image, ImageDraw, ImageFont
import math

def draw_dashed_line(draw, x1, y1, x2, y2, dash_length=8, space_length=4):
    dx = x2 - x1
    dy = y2 - y1
    length = math.sqrt(dx*dx + dy*dy)
    sin_theta = dy / length
    cos_theta = dx / length
    is_dash = False
    l = int(dash_length) + int(space_length)
    for i in range(0, int(length), l):
        x = x1 + i * cos_theta
        y = y1 + i * sin_theta
        if is_dash:
            draw.line((x, y, x + dash_length * cos_theta, y + dash_length * sin_theta), fill='black', width=3)
        is_dash = not is_dash

# create a new image
img = Image.new('RGB', (400, 400), color='white')

#use anti-aliasing
img = img.resize((img.width, img.height), Image.ANTIALIAS)

# create a draw object
draw = ImageDraw.Draw(img)

# draw a dashed line
x1, y1 = 300, 0
x2, y2 = 200,400
draw_dashed_line(draw, x1, y1, x2, y2)

def house(draw, x, y, number):
    rect_x1, rect_y1 = x, y
    rect_x2, rect_y2 = x + 80, y + 80
    draw.rectangle((rect_x1, rect_y1, rect_x2, rect_y2), fill='white', outline='black', width=1)

    # draw the number in the middle of the rectangle
    number = 42 # example number
    font = ImageFont.truetype('arial.ttf', 14)
    text_width, text_height = draw.textsize(str(number), font=font)
    text_x = x + (80 - text_width) // 2
    text_y = y + (80 - text_height) // 2
    draw.text((text_x, text_y), str(number), font=font, fill='black')

def vertical_text(draw,x, y, text, font_size=10):
    """
    Draws vertical text on an image using the specified font size.

    Args:
    - draw: ImageDraw object to draw on.
    - x: x-coordinate of the starting point of the text.
    - y: y-coordinate of the starting point of the text.
    - text: The text to be drawn.
    - font_size: The size of the font to be used. Default is 10.

    Returns:
    - None
    """
    f = ImageFont.truetype('arial.ttf', font_size)
    vf = ImageFont.TransposedFont(f, orientation=2)
    draw.text((x, y), text, font=vf, fill='black')


house(draw, 100, 100, 42)
vertical_text(draw, 50, 50, "HELLO SHIT", 18)

# show the image wit
img.show()