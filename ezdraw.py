import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Debug, easy_print, popup, popup_get_file, popup_get_text
import PIL.Image
import io
import base64

sg.theme('dark amber')
#ystem of 24x24 on this one - weird i know
# CONSTANTS

HEIGHT = 24
WIDTH = 24

pointlist = []


# WRAPPER FUNCTIONS
def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def show_grid():
    """
    Turns grid on
    """
    # draws grid
    for x in range(0, WIDTH, 1):
        grid1 = graph.DrawLine((x, 0), (x, HEIGHT), color="grey")
        #adds
        TK.addtag_withtag('grid', grid1)
    for y in range(0, HEIGHT, 1):
        grid2 = graph.DrawLine((0, y), (WIDTH, y), color="grey")
        TK.addtag_withtag('grid', grid2)
    # draws in numbers
    for a in range(0, WIDTH, 2):
        grid3 = graph.DrawText(a, (a, 0.4), font="Arial 9 normal", angle=90)
        TK.addtag_withtag('grid', grid3)
    for b in range(0, HEIGHT, 2):
        grid4 = graph.DrawText(
            b,
            (0.4, b),
            font="Arial 9 normal",
        )
        TK.addtag_withtag('grid', grid4)

def hide_grid():
    graph.delete_figure('grid')

def wipe():
    graph.erase()

def arrow(dir, x, y):
    """
    Draws an arrow with head at (x,y)

       Parameters:
           dir (str): one of 'n','s','e' or 'w'
           x(float): number between 0,24
           y(float): number between 0,24

       Returns:
           None
    """
    if dir.lower() not in ["n", "s", "e", "w"]:
        return
    if dir == "n":
        graph.DrawPolygon(
            [(x, y), (x - 0.25, y + 0.5), (x + 0.25, y + 0.5)],
            fill_color="black",
            line_color="black",
        )
        graph.DrawLine((x, y + 0.5), (x, y + 1.5), width=1.5)
    elif dir == "s":
        graph.DrawPolygon(
            [(x, y), (x - 0.25, y - 0.5), (x + 0.25, y - 0.5)],
            fill_color="black",
            line_color="black",
        )
        graph.DrawLine((x, y - 0.5), (x, y - 1.5), width=1.5)
    elif dir == "e":
        graph.DrawPolygon(
            [(x, y), (x - 0.5, y - 0.25), (x - 0.5, y + 0.25)],
            fill_color="black",
            line_color="black",
        )
        graph.DrawLine((x - 0.5, y), (x - 1.5, y), width=1.5)
    else:
        graph.DrawPolygon(
            [(x, y), (x + 0.5, y + 0.25), (x + 0.5, y - 0.25)],
            fill_color="black",
            line_color="black",
        )
        graph.DrawLine((x + 0.5, y), (x + 1.5, y), width=1.5)

def h_arrow(x1,x2,y,meas,measdir='l'):
    '''
    Draws a set of horizontal arrows with measurement

        Parameters:
            x1(int or float): 1st horizontal coordinate
            x2(int or float): 2nd horizontal coordinate
            y(int or float): vertical coordinate
            meas(str): measurement to display
            measdir(str): where the measurement will be displayed relative to arrows('l' or 'r')

        Returns:
            None
    '''

    if x1 > x2:
        arrow('w',x1,y)
        arrow('e',x2,y)
        if measdir.lower() == 'l':
            hlabel(meas,x2-2.8,y,11)
        elif measdir.lower() =='r':
            hlabel(meas,x1+2.8,y,11)
    else:
        arrow('e',x1,y)
        arrow('w',x2,y)
        if measdir.lower() == 'l':
            hlabel(meas,x1-2.8,y,11)
        elif measdir.lower() == 'r':
            hlabel(meas,x2+2.8,y,11)

def v_arrow(x,y1,y2,meas,measdir='u'):
    '''
    Draws a set of vertical arrows with measurement

        Parameters:
        x(int or float): horizontal coordinate
        y1(int or float): 1st vertical coordinate
        y2(int or float): 2nd vertical coordinate
        meas(str): measurement to output
        measdir(str): where the measurement will be relative to arrows('u' or 'd')

        Returns:
            None
    '''
    if y1 > y2:
        arrow('n',x,y1)
        arrow('s',x,y2)
        if measdir.lower() == 'u':
            vlabel(meas,x,y2-2.8,11)
        elif measdir.lower() =='d':
            vlabel(meas,x,y1+2.8,11)
    else:
        arrow('s',x,y1)
        arrow('n',x,y2)
        if measdir.lower() == 'u':
            vlabel(meas,x,y1-2.8,11)
        elif measdir.lower() == 'd':
            vlabel(meas,x,y2+2.8,11)

def pole(x, y):
    graph.draw_circle((x, y), 0.4, fill_color="white")


def transformer(x, y):
    graph.draw_rectangle((x - 0.5, y - 0.5), (x + 0.5, y + 0.5), line_color="black")
    graph.draw_polygon(
        [(x, y - 0.5), (x - 0.5, y + 0.5), (x + 0.5, y + 0.5)], fill_color="black"
    )


def vault(util, x, y):
    if util.lower() == "b":
        vlbl = "FTG"
    else:
        vlbl = "HW"
    v1 = graph.draw_rectangle(
        (x - 0.7, y - 0.4), (x + 0.7, y + 0.4), line_color="black", fill_color=None
    )
    v2 = graph.draw_text(vlbl, (x, y), font="Arial 3 normal")
    # prfloat(v2)
    graph.bring_figure_to_front("v2")


def hlabel(msg, x, y, size):
    sg.Graph.draw_text(graph, msg, (x, y), font="Arial " + str(size) + " normal")


def vlabel(msg, x, y, size):
    sg.Graph.draw_text(
        graph, msg, (x, y), font="Arial " + str(size) + " normal", angle=90
    )


def ped(x,y):
    sg.Graph.draw_rectangle(
        graph,(x-0.4,y-0.4), (x+0.4,y+0.4), line_color='black', line_width=1
    )
    sg.Graph.draw_line(graph,(x-0.4,y-0.4), (x+0.4,y+0.4))
    sg.Graph.draw_line(graph,(x-0.4,y+0.4),(x+0.4,y-0.4))

def ped_1arm(x,y,direction='',distance=''):
    '''
    Creates a ped with stub (with or without measurement)

        Parameters:
            x : x coord
            y: y coord
            direction(str): N, S, E or W
            distance: how many squares from ped

        Returns:
            None
    '''
    ped(x,y)
    if direction.lower() == 'n':
        cable(x,y-0.4,x,y-distance)
    elif direction.lower() =='s':
        cable(x,y+0.4,x,y+distance)
    elif direction.lower() == 'w':
        cable(x-0.4,y,x-distance,y)       
    elif direction.lower() == 'e':
        cable(x+0.4,y,x+distance,y)
    else:
        pass

def ped_multiarm(x,y,direction,meas1,meas2,distance,third_arm=False):
    '''
    minimum distance = 3 (for measurements)
    '''
    ped_offset = 0.4
    arm_offset = 1
    arm_offset2 = 2
    if distance < 3:
        return
    ped(x,y)

    if direction.lower() == 'n':
        #left arm
        cable(x,y-ped_offset,x-arm_offset,y-arm_offset)
        cable(x-arm_offset,y-arm_offset,x-arm_offset,y-distance)
        #right arm
        cable(x,y-ped_offset,x+arm_offset,y-arm_offset)
        cable(x+arm_offset,y-arm_offset,x+arm_offset,y-distance)
        #if third arm
        if third_arm:
            cable(x,y-ped_offset,x,y-distance)
        #left arm measurement
        h_arrow(x,x-arm_offset,y-arm_offset,meas1,'l')
        #right arm measurement
        h_arrow(x,x+arm_offset,y-arm_offset2,meas2,'r')
   
    elif direction.lower() == 's':
        pass # dont need yet

    elif direction.lower() == 'w':
        #upper arm
        cable(x-ped_offset,y,x-arm_offset,y-arm_offset)
        cable(x-arm_offset,y-arm_offset,x-distance,y-arm_offset)
        #lower arm
        cable(x-ped_offset,y,x-arm_offset,y+arm_offset)
        h_cable(x-distance,x-arm_offset,y+arm_offset)
        #if third arm
        if third_arm:
            h_cable(x-distance,x-ped_offset,y)
        #upper measurement
        v_arrow(x-arm_offset,y-arm_offset,y,meas1,'u')
        #lower measurement
        v_arrow(x-arm_offset2,y,y+arm_offset,meas2,'d')   

def road(*args):
    return graph.draw_line((args[0], args[1]), (args[2], args[3]), width=3)

def h_road(x1,x2,y):
    road(x1,y,x2,y)

def v_road(x,y1,y2):
    road(x,y1,x,y2)

def cable(x1, y1, x2, y2):
    cable = graph.DrawLine((x1, y1), (x2, y2), width="2")
    graph.TKCanvas.itemconfig(cable, dash=(10, 5))

def h_cable(x1,x2,y,label=''):
    cable(x1,y,x2,y)
    if label:
        #check for cable length to determine spacing
        if (abs(x1 - x2) < 4) or (abs(x2 - x1) < 4):
            gap = 2
        else:
            gap = 6
        for x in range(round(x1),round(x2),gap):
            #white box
            #check for text size
            if len(label) <= 2:
                s = 0.25
            else:
                s = 0.6
            sg.Graph.draw_rectangle(graph,(x-s,y-s),(x+s,y+s), fill_color = 'white', line_color = 'white')
            #text
            hlabel(label,x,y,7)

def v_cable(x,y1,y2,label=''):
    cable(x,y1,x,y2)
    if label:
        if (abs(y1 - y2) < 4) or (abs(y2 - y1) < 4):
            gap = 2
        else:
            gap = 6
        for y in range(round(y1),round(y2),gap):
            #white box
            if len(label) <= 2:
                s = 0.25
            else:
                s = 0.6
            sg.Graph.draw_rectangle(graph,(x-s,y-s),(x+s,y+s), fill_color = 'white', line_color = 'white')
            vlabel(label,x,y,7)   


def line(x1,y1,x2,y2):
    sg.Graph.draw_line(graph,(x1,y1), (x2,y2))

def h_line(x1,x2,y):
    line(x1,y,x2,y)

def v_line(x,y1,y2):
    line(x,y1,x,y2)


def digbox(x1, y1, x2, y2):
    db = graph.draw_rectangle((x1, y1), (x2, y2), fill_color="#D3D3D3", line_color="black")
    graph.TKCanvas.itemconfig(db, stipple="gray50")
    graph.send_figure_to_back(db)


def located_area(x, y):
    sg.Graph.draw_text(graph, "LOCATED AREA", (x, y), font="Arial 12 bold")


def house(x, y, size, num):
    if size == "m":
        graph.draw_rectangle((x, y), (x + 4, y + 4))

#barebones

notify = sg.Text()
notify2 = sg.Text()

col = [[
        sg.Graph(
            canvas_size=(856, 1056),
            graph_bottom_left=(0, HEIGHT),
            graph_top_right=(WIDTH, 0),
            background_color="white",
            key="graph",
            enable_events=True,
            drag_submits=True,
            expand_x=True,
            expand_y=True
        ),
    ],]
layout = [
    [
        notify,notify2
    ],
    [sg.Column(col,scrollable=True,vertical_scroll_only=True,expand_y=True,expand_x=True)
    ]
]

window = sg.Window(
    "EZ Draw",
    layout,
    finalize=True,
    font="Arial",
    resizable=True,
    return_keyboard_events=True,
    use_default_focus=False
)
graph = window["graph"]
TK = graph.TKCanvas
# DRAW HERE


mode = {0:'select', 1:'get points', 2:'draw'}
current_mode = 'regular'
x = y = a = b = None
isGrid = False
graph.bind('<Motion>','motion')
#small loop
while True:
    event, values = window.read()
    #notify2.update(event)
    if event == sg.WIN_CLOSED:
        break
    if event.endswith('motion'):
        winx, winy = window.mouse_location()
        notify2.update(f'{winx},{winy}')
    if event == 'Escape:27':
                notify.update('Cancelled')
                current_mode = ''
    if event == 'i':
        img = popup_get_file('Select image')
        sg.Graph.draw_image(graph,location=(0,0),data=convert_to_bytes(img))
    if event == 'c':
        current_mode = 'cable'
        notify.update('Please click first point of line:')
    if event == 'g':
        if isGrid == False:
            isGrid = not isGrid
            show_grid()
        else:
            isGrid = not isGrid
            #hide_grid
            hide_grid()
    if event == 'u':
        ids = list(graph.TKCanvas.find_all())
        if len(ids) < 1:
            pass
        else:
            graph.delete_figure(ids[-1])
    if event == 'w':
        wipe()
    if event == 't':
        current_mode = 'text'
        entered_text = popup_get_text('Enter text')
        notify.update('Please click to enter text')
    if event == 'T':
        current_mode = 'vtext'
        entered_text = popup_get_text('Enter text')
        notify.update('Please click to enter text')
    if event.endswith('+UP'):
        if current_mode == 'cable':
            x, y = values['graph']
            point1 = (x, y)
            dot1 = sg.Graph.draw_point(graph,(x, y), size=0.5, color='red')
            notify.update(f'mode:{current_mode}, event = {event} points = {point1}')
            current_mode='clickedonce'
        elif current_mode == 'clickedonce':
            a, b = values['graph']
            point2 = (a, b)
            dot2 = sg.Graph.draw_point(graph,(a,b), size=0.5, color='blue')
            cable(x, y, a, b)
            x=y=a=b=None
            current_mode=''
            graph.delete_figure(dot1)
            graph.delete_figure(dot2)
        elif current_mode == 'text':
            x, y = values['graph']
            hlabel(entered_text, x, y, 11)
            x=y=entered_text =None
        elif current_mode == 'vtext':
            x, y = values['graph']
            vlabel(entered_text,x,y,11)
            x = y = entered_text = None

window.close()
