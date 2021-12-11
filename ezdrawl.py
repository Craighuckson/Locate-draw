import base64
import logging
import io
from tkinter.constants import TRUE
from PIL import ImageGrab

import PIL.Image
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import (Window, easy_print, main, popup_error, popup_get_file,
                                     popup_get_text)

sg.theme('dark amber')
#ystem of 24x24 on this one - weird i know
logging.basicConfig(filename='ezdraw.log',level=logging.WARNING, format='%(asctime)s')
# CONSTANTS

HEIGHT = 30
WIDTH = 30

ECURB = [WIDTH/3,2,WIDTH/3,HEIGHT-2]
WCURB = [(WIDTH*2)/3,2,(WIDTH*3)/2,HEIGHT-2]
NCURB = [2,(HEIGHT*2)/3, WIDTH-2,(HEIGHT*2)/3]
SCURB = [2,HEIGHT/3,WIDTH-2,HEIGHT/3]

NSTREET = [WIDTH/2,(NCURB[1] + HEIGHT)/2]
SSTREET = [WIDTH/2, (SCURB[1])/2]
WSTREET = [(WCURB[0] + WIDTH)/2, HEIGHT/2]
ESTREET = [ECURB[0]/2, HEIGHT/2]


pointlist = []


# WRAPPER FUNCTIONS

def save_element_as_file(element, filename):
    """
    Saves any element as an image file.  Element needs to have an underlyiong Widget available (almost if not all of them do)
    :param element: The element to save
    :param filename: The filename to save to. The extension of the filename determines the format (jpg, png, gif, ?)
    """
    widget = element.Widget
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox=box)
    grab.save(filename)
    ImageGrab.grab()

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

def convert_measurement():
    newmeas = ''
    meas = popup_get_text('Enter measurement(int)')
    try:
        if len(meas) == 1:
            newmeas = '0.' + meas + 'm'
            return newmeas
        elif len(meas) ==2:
            newmeas = meas[0] + '.' + meas[1] + 'm'
            return newmeas
        elif len(meas) ==3:
            newmeas = meas[0] + meas[1] + '.' + meas[2] + 'm'
            return newmeas
    except TypeError:
        logging.exception('empty measurement')
        return
def logerror():
    logging.exception('Caught an error')

def show_grid():
    """
    Turns grid on
    """
    # draws grid
    # for x in range(0, WIDTH, 1):
    #     grid1 = graph.DrawLine((x, 0), (x, HEIGHT), color="grey")
    #     #adds
    #     TK.addtag_withtag('grid', grid1)
    # for y in range(0, HEIGHT, 1):
    #     grid2 = graph.DrawLine((0, y), (WIDTH, y), color="grey")
    #     TK.addtag_withtag('grid', grid2)
    # # draws in numbers
   
    #     TK.addtag_withtag('grid', grid4)
    #     TK.itemconfig('grid',state='disabled')
    try:
        for x in range(0,WIDTH):
            for y in range(0,HEIGHT):
                gpt = sg.Graph.draw_point(graph,(x,y),color='grey',size=0.1)
                TK.addtag_withtag('grid',gpt)
        for a in range(0, WIDTH, 2):
            grid3 = graph.DrawText(a, (a, 0.4), font="Arial 9 normal", angle=90)
            TK.addtag_withtag('grid', grid3)
        for b in range(0, HEIGHT, 2):
            grid4 = graph.DrawText(
                b,
                (0.4, b),
                font="Arial 9 normal",
            )
            TK.addtag_withtag('grid',grid4)
            graph.send_figure_to_back('grid')
            TK.itemconfig('grid',state='disabled')
    except:
        logging.exception('Caught an error')

def hide_grid():
    TK.itemconfig('grid',state='hidden')
    #graph.delete_figure('grid')

def group(group_name,figure):
    TK.addtag_withtag(group_name,figure)

def wipe():
    graph.erase()

def rarrow(x1,y1,x2,y2):
    sg.Graph.draw_line()

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
    try:
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
    except:
        logging.exception('caught an error')

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
    try:
        if x1 > x2:
            arrow('w',x1,y)
            arrow('e',x2,y)
            if measdir.lower() == 'l':
                hlabelm(meas,x2-2.8,y,11)
            elif measdir.lower() =='r':
                hlabelm(meas,x1+2.8,y,11)

        else:
            arrow('e',x1,y)
            arrow('w',x2,y)
            if measdir.lower() == 'l':
                hlabelm(meas,x1-2.8,y,11)
            elif measdir.lower() == 'r':
                hlabelm(meas,x2+2.8,y,11)
    except:
        logerror()

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
    try:
        if y1 > y2:
            arrow('n',x,y1)
            arrow('s',x,y2)
            if measdir.lower() == 'u':
                vlabelm(meas,x,y2-2.8,11)
            elif measdir.lower() =='d':
                vlabelm(meas,x,y1+2.8,11)
        else:
            arrow('s',x,y1)
            arrow('n',x,y2)
            if measdir.lower() == 'u':
                vlabelm(meas,x,y1-2.8,11)
            elif measdir.lower() == 'd':
                vlabelm(meas,x,y2+2.8,11)
    except:
        logerror()

def pole(x, y):
    try:
        p=graph.draw_circle((x, y), 0.4, fill_color="white")
        TK.addtag_withtag('pole',p)
    except:
        logerror()


def transformer(x, y):
    try:
        txr = graph.draw_rectangle((x - 0.5, y - 0.5), (x + 0.5, y + 0.5), line_color="black")
        txtri = graph.draw_polygon(
            [(x, y - 0.5), (x - 0.5, y + 0.5), (x + 0.5, y + 0.5)], fill_color="black"
        )
        TK.addtag_withtag('transformer',txr)
        TK.addtag_withtag('transformer',txtri)
    except:
        logerror()


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
    try:
        sg.Graph.draw_text(graph, msg.upper(), (x, y), font="Arial " + str(size) + " normal")
    except:
        logerror()

def hlabelm(msg, x, y, size):
    try:
        sg.Graph.draw_text(graph, msg.lower(), (x, y), font="Arial " + str(size) + " normal")
    except:
        logerror()

def vlabel(msg, x, y, size):
    try:
        sg.Graph.draw_text(
            graph, msg.upper(), (x, y), font="Arial " + str(size) + " normal", angle=90
        )
    except:
        logerror()

def vlabelm(msg, x, y, size):
    try:
        sg.Graph.draw_text(
            graph, msg.lower(), (x, y), font="Arial " + str(size) + " normal", angle=90
        )
    except:
        logerror()

def ped(x,y):
    try:
        pedsq = sg.Graph.draw_rectangle(
            graph,(x-0.4,y-0.4), (x+0.4,y+0.4), line_color='black',fill_color='white',line_width=1
        )
        group('ped',pedsq)
        pedline1 = sg.Graph.draw_line(graph,(x-0.4,y-0.4), (x+0.4,y+0.4))
        group('ped',pedline1)
        pedline2 = sg.Graph.draw_line(graph,(x-0.4,y+0.4),(x+0.4,y-0.4))
        group('ped',pedline2)
        TK.itemconfig('ped',activefill='red')
        
    except:
        logerror()

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

def road(x1,y1,x2,y2):
    try:
        r=graph.DrawLine((x1,y1),(x2,y2),width='3')
        graph.TKCanvas.itemconfig(r,activefill='red')
        TK.addtag_withtag('road',r)
    except:
        logerror()

def h_road(x1,x2,y):
    road(x1,y,x2,y)

def v_road(x,y1,y2):
    road(x,y1,x,y2)

def offset_line(x1,y1,x2,y2):
    try:
        offset = graph.draw_line((x1,y1), (x2,y2), width='1')
        graph.TKCanvas.itemconfig(offset, dash = (2, 7))
        TK.itemconfig(offset,activefill='red')
        TK.addtag_withtag('oline',offset)
    except:
        logerror()

def cable(x1, y1, x2, y2,label=''):
    try:
        cable = graph.DrawLine((x1, y1), (x2, y2), width="2")
        graph.TKCanvas.itemconfig(cable, dash=(10, 5))
        TK.addtag_withtag('cable',cable)
        if label:
            #check for horizontal or vertical lines
            if x1==x2:
                #vertical cable
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
                    tbox = sg.Graph.draw_rectangle(graph,(x1-s,y-s),(x1+s,y+s), fill_color = 'white', line_color = 'white')
                    TK.addtag_withtag('cable','tbox')
                    tlab = sg.Graph.draw_text(graph,label.upper(),(x1,y),font='Arial 7 normal')
                    TK.addtag_withtag('cable',tlab)

            elif y1==y2:
                #horizontal cable
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
                    tbox = sg.Graph.draw_rectangle(graph,(x-s,y1-s),(x+s,y1+s), fill_color = 'white', line_color = 'white')
                    TK.addtag_withtag('cable',tbox)
                    #text
                    tlab = sg.Graph.draw_text(graph,label.upper(),(x,y1),font='Arial 7 normal')
                    TK.addtag_withtag('cable',tlab)
    except:
        logerror()



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
    try:
        l = sg.Graph.draw_line(graph,(x1,y1), (x2,y2))
        #TK.itemconfig(l,arrow='last',activefill='red')
    except:
        logerror()

def h_line(x1,x2,y):
    line(x1,y,x2,y)

def v_line(x,y1,y2):
    line(x,y1,x,y2)


def digbox(x1, y1, x2, y2):
    try:
        db = graph.draw_rectangle((x1, y1), (x2, y2), fill_color="#D3D3D3", line_color="black")
        graph.TKCanvas.itemconfig(db, stipple="gray50")
        graph.send_figure_to_back(db)
        TK.addtag_withtag('digbox',db)
    except:
        logerror()

def located_area(x, y):
    try:
        sg.Graph.draw_text(graph, "LOCATED AREA", (x, y), font="Arial 12 bold")
    except:
        logerror()

def house(x, y, size, num):
    if size == "m":
        graph.draw_rectangle((x, y), (x + 6, y + 6),line_color='black')
    elif size == 'l':
        bldng = sg.Graph.draw_rectangle(graph,(x,y),(x+8,y+8),line_color='black',fill_color='white')
        hnumber = hlabel(num,x+4,y+4,16)
        nbl = hlabel('NBL',x+4,y-1,10)
        sbl = hlabel('SBL',x+4,y+9,10)
        wbl = vlabel('WBL',x-1,y+4,10)
        ebl = vlabel('EBL',x+9,y+4,10)
        for x in bldng,hnumber,nbl,sbl,wbl,ebl:
            group('house_l','x')

def get_point1():
    x, y = values['graph']
    return x, y

def get_point2():
    a, b = values['graph']
    return a,b

def draw_point1(x,y,color='red'):
    try:
        point1 = sg.Graph.draw_point(graph,(x, y), size=0.5, color= color)
        return point1
    except:
        logerror()

def draw_point2(x,y,color='blue'):
    try:
        point2 = sg.Graph.draw_point(graph,(x,y),size=0.5,color=color)
        return point2
    except:
        logerror()

def cleanup_2point():
            x=y=a=b=None
            current_mode=''
            graph.delete_figure(point1)
            graph.delete_figure(point2)


#callback routines

def short_gas():
    try:
        dir = popup_get_text('N, S, E, W?')
        hnum = popup_get_text('House number?')
        street = popup_get_text('Street name?')
        if dir.lower() == 'n':
            h_road(2,WIDTH-2,23)
            hlabel('NCL',27,24,12)
            digbox(7,1,23,27)
            house(11,4,'l',hnum)
            hlabel(street,15,27,20)
        elif dir.lower() == 's':
            h_road(2,WIDTH-2, 7)
            hlabel('SCL',27,8,12)
            digbox(7,3,23,29)
            house(11,18,'l',hnum)
            hlabel(street,15,3,20)
            hlabel('LOCATED AREA',15,14,12)
        elif dir.lower() == 'e':
            v_road(7,2,HEIGHT-2)
            vlabel('ECL',8,3,12)
            digbox(3,7,29,23)
            house(18,11,'l',hnum)
            vlabel(street,3,15,20)
        elif dir.lower() == 'w':
            v_road(23,2,HEIGHT-2)
            vlabel('WCL',22,3,12)
            digbox(1,7,27,23)
            house(4,11,'l',hnum)
            vlabel(street,27,15,20)
        else:
            easy_print(logging.exception('err'))
            pass

    except:
        easy_print(logging.exception('err'))
        pass

#barebones

notify = sg.Text()
notify2 = sg.Text()

menu_def = [
            [
                'File', 'Save',['Size',['24','30',]]
            ],
]
lcol = [
    [
        sg.Text('Curb: '), sg.DropDown(('N','S','E','W'),enable_events=True,k='curbddl'),
        sg.Radio('CL','roadtype',k='cl'), sg.Radio('RE','roadtype',k='re')
    ],
    [
        sg.Text('Street: '), sg.I(k='streetin',enable_events=True)
    ]
 ]

col = [
    [   
        notify, notify2
    ],
    [
        sg.Graph(
            canvas_size=(600, 600),
            graph_bottom_left=(0, HEIGHT),
            graph_top_right=(WIDTH, 0),
            background_color="white",
            key="graph",
            enable_events=True,
            drag_submits=True,
            expand_x=True,
            expand_y=True
        ),
    ],
    [
        sg.Button('Short Gas',enable_events=True)
    ],
    ]

layout = [
    [
        #sg.Column(lcol),
        sg.Menu(menu_def),
        sg.Column(col,expand_x=True,expand_y=True)
    ]
]

window = sg.Window(
    "EZ Draw",
    layout,
    finalize=True,
    font="Arial",
    resizable=True,
    return_keyboard_events=True,
    use_default_focus=True,
)
window.maximize()
graph = window["graph"]
TK = graph.TKCanvas
# DRAW HERE


mode = {0:'select', 1:'get points', 2:'draw'}
current_mode = 'regular'
x = y = a = b = None
isGrid = False
graph.bind('<B1-Motion>','drag')
graph.bind('<Motion>','motion')
#main()
#small loop
while True:
    event, values = window.read()
    notify2.update(event)
    if event == sg.WIN_CLOSED:
        break

    #change drawing size

    if event == 'Save':
        _savefile = popup_get_file('Save image as...',default_extension='*.png',save_as=True)
        window.bring_to_front()
        save_element_as_file(window['graph'],_savefile)
        

    if event == '24':
        sg.Graph.set_size(graph,(480,480))
        sg.Graph.change_coordinates(graph,(0,24),(24,0))
        graph.update()
    
    if event == '30':
        sg.Graph.set_size(graph,(600,600))
        sg.Graph.change_coordinates(graph,(0,24),(24,0))
        graph.update()

    #routines

    if event == 'Short Gas':
        short_gas()
    #left hand stuff

    if event == 'curbddl':
        
        if values['cl'] == True:
                rtype = 'CL'
        else:
                rtype = 'RE'
        if values['curbddl'] == 'N':
            road(NCURB[0],NCURB[1],NCURB[2],NCURB[3])
            hlabel(values['curbddl'] + rtype,WIDTH-3,NCURB[1]-1,10)
        elif values['curbddl'] == 'S':
            road(SCURB[0],SCURB[1],SCURB[2],SCURB[3])
            hlabel(values['curbddl'] + rtype,WIDTH-3,SCURB[1]+1,10)
        elif values['curbddl'] == 'W':
            road(WCURB[0],WCURB[1],WCURB[2],WCURB[3])
            vlabel(values['curbddl'] + rtype,HEIGHT-3,WCURB[0]-1,10)
        elif values['curbddl'] == 'E':
            road(ECURB[0],ECURB[1],ECURB[2],ECURB[3])
            vlabel(values['curbddl']+rtype,ECURB[0]-1,HEIGHT-3,10)
        graph.block_focus(False)

    if event == 'streetin':
        street = popup_get_text('Enter street name')
        if values['curbddl'] == 'N':
            hlabel(street,NSTREET[0],NSTREET[1],20)
        elif values['curbddl'] == "S":
            hlabel(street,SSTREET[0],SSTREET[1],20)
        elif values['curbddl'] == 'W':
            vlabel(street,WSTREET[0],WSTREET[1],20)
        elif values['curbddl'] == 'E':
            vlabel(street, ESTREET[0], ESTREET[1],20)
    
    if event == 'm' and current_mode=='chosen':
        notify.update('Please click location to move to')
        current_mode='move'

    if event.endswith('motion'):
        # try:
        #     if l1:
        #         graph.delete_figure(l1)
        #     if l2:
        #         graph.delete_figure(l2)
        # except NameError:
        #     pass
        # x,y = values['graph']
        notify2.update(values['graph'])
        # l1 = sg.Graph.draw_line(graph,(x,0),(x,HEIGHT))
        # l2 = sg.Graph.draw_line(graph,(0,y),(WIDTH,y))
        # sg.Graph.relocate_figure(graph,l1,x,y)
        # sg.Graph.relocate_figure(graph,l2,x,y)
        # graph.update()

    # if event.endswith('drag'):
    #     try:
    #         if db:
    #             graph.delete_figure(db)
    #     except NameError:
    #         pass
    #     x,y = values['graph']
    #     startx,starty = x,y
    #     currentx,currenty = startx,starty
    #     db = sg.Graph.draw_rectangle(graph,(startx,starty),(currentx,currenty),line_color='red')
    #     graph.update()
    if event == 'Escape:27':
        notify.update('Cancelled')
        #graph.delete_figure(bbr)

    if event == 's':
        current_mode = 'select'
        notify.update('Select figure')
    if event == 'i':
        img = popup_get_file('Select image')
        sg.Graph.draw_image(graph,location=(0,0),data=convert_to_bytes(img))
    if event == 'h':
        current_mode = 'harrow'
        notify.update('Please select first arrow point')
    if event == 'v':
        current_mode = 'varrow'
        notify.update('Please select first arrow point')
    if event == 'c':
        current_mode = 'cable'
        notify.update('Please click first point of cable line:')
    if event == 'o':
        current_mode = 'offsetline'
        notify.update('Please click first point of offset line:')
    if event == 'd':
        current_mode = 'digbox'
        notify.update('Please click first point of box: ')
    if event == 'b':
        current_mode = 'house'
        notify.update('Please click upper left corner of building: ')
    if event == 'r':
        current_mode = 'road'
        notify.update('Please click first point of curb line')
    if event == 'l':
        current_mode = 'line'
        notify.update('Please click first point of line')
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
    if event == 'x' and current_mode == 'chosen':
        if TK.itemcget(fig,'tag') is not None:
            graph.delete_figure(TK.itemcget(fig,'tag'))
        graph.delete_figure(fig)
    if event == 't':
        current_mode = 'text'
        entered_text = popup_get_text('Enter text')
        notify.update('Please click to enter text')
    if event == 'T':
        current_mode = 'vtext'
        entered_text = popup_get_text('Enter text')
        notify.update('Please click to enter text')
    if event == '1':
        current_mode = 'ped'
        notify.update('Click to place pedestal')
    if event == '2':
        current_mode = 'pole'
        notify.update('Click to place pole')
    if event.endswith('+UP'):
        if current_mode == 'cable':
            x, y = get_point1()
            point1 = draw_point1(x,y)
            notify.update('Click second point of line')
            current_mode='cable2'
        elif current_mode == 'offsetline':
            x, y = get_point1()
            point1 = draw_point1(x,y)
            notify.update('Click second point of line')
            current_mode='offsetline2'
        elif current_mode == 'digbox':
            x,y = get_point1()
            point1 = draw_point1(x,y,'green')
            notify.update('Click second point of line')
            current_mode = 'digbox2'
        elif current_mode == 'house':
            x,y = get_point1()
            point1 = draw_point1(x,y,'black')
            notify.update('Click lower right corner of building')
            current_mode = 'house2'
        elif current_mode == 'road':
            x,y = get_point1()
            point1 = draw_point1(x,y,'purple')
            notify.update('Click second point of curb')
            current_mode = 'road2'
        elif current_mode == 'line':
            x,y = get_point1()
            point1 = draw_point1(x,y,'blue')
            notify.update('Click second point of line')
            current_mode = 'line2'
        elif current_mode =='harrow':
            x,y = get_point1()
            point1 = draw_point1(x,y,'orange')
            notify.update('Click second arrow point')
            current_mode = 'harrow2'
        elif current_mode == 'varrow':
            x,y = get_point1()
            point1 = draw_point1(x,y,'orange')
            notify.update('Click second arrow point')
            current_mode = 'varrow2'
        elif current_mode == 'cable2':
            a, b = get_point2()
            point2 = draw_point2(x,y,'red')
            label = popup_get_text('Label? ')
            cable(x, y, a, b,label)
            cleanup_2point()
        elif current_mode == 'offsetline2':
            a, b = get_point2()
            point2 = draw_point2(x,y,'brown')
            offset_line(x,y,a,b)
            cleanup_2point()
            """ x=y=a=b=None
            current_mode='''
            graph.delete_figure(point1)
            graph.delete_figure(point2) """
        elif current_mode == 'digbox2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'green')
            digbox(x,y,a,b)
            cleanup_2point()
        elif current_mode == 'house2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'black')
            #TODO wrap this
            sg.Graph.draw_rectangle(graph,(x,y),(a,b),line_color='black',fill_color='white')
            cleanup_2point()
        elif current_mode == 'road2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'purple')
            road(x,y,a,b)
            cleanup_2point()
            current_mode = 'road'
        elif current_mode == 'line2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'blue')
            line(x,y,a,b)
            cleanup_2point()
            current_mode = 'line'
        elif current_mode == 'harrow2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'orange')
            meas = convert_measurement()
            h_arrow(x,a,y,meas)
            cleanup_2point()
        elif current_mode == 'varrow2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'orange')
            meas = convert_measurement()
            v_arrow(x,y,b,meas)
            cleanup_2point()
        elif current_mode == 'text':
            x, y = get_point1()
            hlabel(entered_text, x, y, 12)
            x=y=entered_text =None
        elif current_mode == 'vtext':
            x, y = get_point1()
            vlabel(entered_text,x,y,12)
            x = y = entered_text = None
        elif current_mode == 'ped':
            x, y = get_point1()
            ped(x,y)
            x=y=None
        elif current_mode == 'pole':
            x, y = get_point1()
            pole(x,y)
            x=y=None
        elif current_mode == 'select':
            drag_figures =sg.Graph.get_figures_at_location(graph,values['graph'])
            if drag_figures:
                for fig in drag_figures:
                    if TK.itemcget(fig,'tag') == 'grid':
                        pass
                    else:
                    #easy_print(graph.TKCanvas.type(fig))
                #easy_print(type(fig))
                        #bb = sg.Graph.get_bounding_box(graph,fig)
                        #bbr= sg.Graph.draw_rectangle(graph,(bb[0]),bb[1], line_color='blue')
                        #easy_print(TK.itemconfig(fig))
                        notify2.update(TK.type(fig) + ',' +TK.itemcget(fig,'tag'))
                        current_mode = 'chosen'
        elif current_mode=='move':
            try:
                x,y=get_point1()
                if TK.itemcget(fig,'tag') == 'arrow1':
                    graph.relocate_figure('arrow1',x,y)
                elif TK.itemcget(fig,'tag') == 'arrow2':
                    graph.relocate_figure('arrow2',x,y)
                elif TK.itemcget(fig,'tag') == 'cable':
                    graph.relocate_figure('cable',x,y)
                else:
                    graph.relocate_figure(fig,x,y)
                #sg.Graph.delete_figure(bbr)
                #TK.itemconfig(fig,fill='black')
                x=y=None
            except:
                logging.exception('There was an error')


window.close()
