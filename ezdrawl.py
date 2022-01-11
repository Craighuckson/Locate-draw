import base64
import logging
import io
from typing import Collection
from PIL import ImageGrab

import PIL.Image
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import (Window, easy_print, main, popup, popup_error, popup_get_file,popup_get_text, popup_yes_no)
import pickle

sg.theme('hot dog stand')
logging.basicConfig(filename='ezdraw.log',level=logging.WARNING, format='%(asctime)s')
# CONSTANTS

HEIGHT = 30
WIDTH = 30

ECURB = [WIDTH/3,2,WIDTH/3,HEIGHT-2]
WCURB = [(WIDTH*2)/3,2,(WIDTH*2)/3,HEIGHT-2]
NCURB = [2,(HEIGHT*2)/3, WIDTH-2,(HEIGHT*2)/3]
SCURB = [2,HEIGHT/3,WIDTH-2,HEIGHT/3]

NSTREET = [WIDTH/2,(NCURB[1] + HEIGHT)/2]
SSTREET = [WIDTH/2, (SCURB[1])/2]
WSTREET = [(WCURB[0] + WIDTH)/2, HEIGHT/2]
ESTREET = [ECURB[0]/2, HEIGHT/2, 20]

NBLHOUSE1 = (2,8,'s') 
NBLHOUSE2 = (24,8,'s')
NWBLHOUSE = (8,8,'m')
NEBLHOUSE = (18,8,'m')
SBLHOUSE1 = (2,18,'s')
SBLHOUSE2 = (24,18,'s')
SWBLHOUSE = (9,16,'m')
SEBLHOUSE = (16,16,'m')
WBLHOUSE1 = (5,2,'s')
WBLHOUSE2 = (5,24,'s')
EBLHOUSE1 = (20,2,'s')
EBLHOUSE2 = (20,24,'s')

NPLTOPL_DIGBOX = (6,16,24,28)
NWPLTOPL_DIGBOX = (8,8,28,28)
NEPLTOPL_DIGBOX = (4,8,24,28)
SPLTOPL_DIGBOX = (6,2,24,14)
SWPLTOPL_DIGBOX = (9,3,27,22)
SEPLTOPL_DIGBOX = (3,3,22,22)
WPLTOPL_DIGBOX = (14,6,28,24)
EPLTOPL_DIGBOX = (2,2,15,28)

pointlist = []

#classes

# WRAPPER FUNCTIONS

def save_element_as_file(element, filename):
    """
    Saves any element as an image file.  Element needs to have an underlyiong Widget available (almost if not all of them do)
    :param element: The element to save
    :param filename: The filename to save to. The extension of the filename determines the format (jpg, png, gif, ?)
    """
    widget = element.Widget
    box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
    grab = ImageGrab.grab(bbox=box,include_layered_windows=True,)
    grab.save(filename)
    ImageGrab.grab(0)

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
        gdwg = 'grid.png'
        grid = sg.Graph.draw_image(graph, location=(0,0),data=convert_to_bytes(gdwg))
        TK.addtag_withtag('grid',grid)
        graph.send_figure_to_back('grid')
        TK.itemconfig('grid',state='disabled')
    except:
        popup('Error')
        logging.exception('Caught an error')

def snap_to_grid_off():
    sg.Graph.change_coordinates(graph,(0,600),(600,0))
    graph.update()

def snap_to_grid_on():
    sg.Graph.change_coordinates(graph,(0,30),(30,0))
    graph.update()

def hide_grid():
    TK.itemconfig('grid',state='hidden')
    #graph.delete_figure('grid')

def group(group_name,figure):
    TK.addtag_withtag(group_name,figure)

def wipe():
    confirm = popup_yes_no('Erase entire image?')
    if confirm == 'Yes':
        graph.erase()
    else:
        pass

def rarrow(x1,y1,x2,y2):
    try:
        slope = (y2-y1)/(x2-x1)
    except ZeroDivisionError:
        slope = None
    #horizontal
    meas = convert_measurement()
    #notify3.update(slope)
    try:

        if x1 < x2 and y1==y2:
            arrow1 = sg.Graph.draw_line(graph,(x1,y1),(x1-2,y1))
            arrow2 = sg.Graph.draw_line(graph,(x2,y2),(x2+2,y2))
            hlabelm(meas,x1-4,y1,11)
        elif x1 > x2 and y1==y2:
            arrow1 = sg.Graph.draw_line(graph,(x1,y1),(x1+2,y1))
            arrow2 = sg.Graph.draw_line(graph,(x2,y2),(x2-2,y2))
            hlabelm(meas,x1+4,y1,11)
        #vertical
        elif x1 == x2 and y1 < y2:
            arrow1 = sg.Graph.draw_line(graph,(x1,y1),(x1,y1-2))
            arrow2 = sg.Graph.draw_line(graph,(x2,y2),(x2,y2+2))
            vlabelm(meas,x1,y1-4,11)
        elif x1 == x2 and y1 > y2:
            arrow1 = sg.Graph.draw_line(graph,(x1,y1),(x1,y1+2))
            arrow2 = sg.Graph.draw_line(graph,(x2,y2),(x2,y2-2))
            vlabelm(meas,x1,y1+4,11)   
        else:
            popup('Cant do this')    
        #diagonal ?
    #elif x1 != x2 and y1 != y2:
        #arrow1 = sg.Graph.draw_line(graph,(x1,y1),(x1-(x2-x1),y1-(y2-y1)))
        #arrow2 = sg.Graph.draw_line(graph,(x2,y2),(x2-(x2-x1),y2-(y2-y1)))
    except:
        pass
    TK.itemconfig(arrow1,arrow='first')
    TK.itemconfig(arrow2,arrow='first')

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

def arc(x1,y1,x2,y2,line_type=None):
    '''
    Draws an arc from a horizontal plane to vertical
    (x1,y1) - horizontal starting point
    (x2,y2) - vertical starting point

    line_type -default is thin line, accepts 'road' or 'cable'
    '''
    if x2 > x1 and y2 > y1:
        #down and right
        id = sg.Graph.draw_arc(graph,(x1 - (x2-x1),y1),(x2,y2+(y2-y1)),-90,90,style='arc')
    elif x2 > x1 and y2 < y1:
        #up and to the right
        id = sg.Graph.draw_arc(graph,(x1 - (x2-x1),y2 - (y1-y2)),(x2,y1),90,270,style='arc')
    elif x2 < x1 and y2 > y1:
        #down and to the left
        id = sg.Graph.draw_arc(graph,(x2,y1),(x1 + (x1-x2), y2 + (y2-y1)),90,90,style='arc')
    elif x2 < x1 and y2 < y1:
        #up and to the left
        id = sg.Graph.draw_arc(graph,(x2,y2 - (y1-y2)),(x1 + (x1-x2),y1),-90,270,style='arc')
    try:
        if line_type == 'road':
            TK.itemconfig(id, width=3)
            group('road',id)
        elif line_type == 'cable':
            TK.itemconfig(id,width=2,dash= (10,5))
            group('cable',id)
        
        return id
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


def vault(x, y, utility=None):
    '''
    Draws vault at position x,y

    utility : 'b' gives label 'FTG', otherwise label is 'HW'
    '''

    if utility == "b":
        vault_label = "FTG"
    else:
        vault_label = "HW"
    v1 = graph.draw_rectangle(
        (x - 0.7, y - 0.4), (x + 0.7, y + 0.4), line_color="black", fill_color=None
    )
    v2 = graph.draw_text(vault_label, (x, y), font="Arial 7 bold")
    # prfloat(v2)
    graph.bring_figure_to_front(v2)

    for x in v1,v2:
        group('vault',x)

def catch_basin(x,y):
    sg.Graph.draw_rectangle(graph,(x-0.5,y-0.5),(x+0.5,y+0.5),line_color='black',line_width=1.5)


def hlabel(msg, x, y, size):
    try:
        if msg == 'la' or msg == 'LA':
            msg = 'LOCATED AREA'
        sg.Graph.draw_text(graph, msg.upper(), (x, y), font="Arial " + str(size) + " bold")
    except:
        logerror()

def hlabelm(msg, x, y, size):
    try:
        sg.Graph.draw_text(graph, msg.lower(), (x, y), font="Arial " + str(size) + " normal")
    except:
        logerror()

def vlabel(msg, x, y, size):
    try:
        if msg == 'la' or msg == 'LA':
            msg = 'LOCATED AREA'
        sg.Graph.draw_text(
            graph, msg.upper(), (x, y), font="Arial " + str(size) + " bold", angle=90
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

def item_stamp(x,y):
    try:
        sg.Graph.draw_image(graph,location=(x-0.75,y-0.75),data=convert_to_bytes('Drilling.bmp'))
    except:
        logerror()


def ped(x,y):
    try:
        pedsq = sg.Graph.draw_rectangle(
            graph,(x-0.4,y-0.4), (x+0.4,y+0.4), line_color='black',fill_color='white',line_width=1
        )
        pedline1 = sg.Graph.draw_line(graph,(x-0.4,y-0.4), (x+0.4,y+0.4))
        pedline2 = sg.Graph.draw_line(graph,(x-0.4,y+0.4),(x+0.4,y-0.4))
        for item in [pedsq,pedline1,pedline2]:
            group('ped',item)
        
    except:
        logerror()

def ped_1arm(pedx,pedy,intercept_x, intercept_y):
    '''
    Creates a ped with cable stub

        Parameters:
            pedx : x coord
            pedy: y coord
            intercept_x : x coord of where stub meets connecting cable
            intercept_y :y coords of where stub meets connecting cable

        Returns:
            None
    '''
    cable(pedx,pedy,intercept_x,intercept_y)
    ped(pedx,pedy)

def pole_1arm(polex,poley,intercept_x, intercept_y):
    '''
    Creates a pole with cable stub

        Parameters:
            polex : x coord
            poley: y coord
            intercept_x : x coord of where stub meets connecting cable
            intercept_y :y coords of where stub meets connecting cable

        Returns:
            None
    '''
    cable(polex,poley,intercept_x,intercept_y)
    pole(polex,poley)


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
        v_arrow(x-arm_offset,y-arm_offset,y,meas1,'8u')
        #lower measurement
        v_arrow(x-arm_offset2,y,y+arm_offset,meas2,'d')   

def set_landbase(dir,edge_type='CL'):
    #draws a landbase
    if dir.lower() == 'n':
        h_road(2,WIDTH-2,23)
        hlabel(f'N{edge_type}',27,24,12)
    elif dir.lower() == 'ne':
        h_road(9,28,23)
        hlabel(f'N{edge_type}',27,24,11)
        v_road(9,2,23)
        vlabel(f'E{edge_type}',10,3,11)
    elif dir.lower() == 'nw':
        h_road(2,23,23)
        hlabel(f'N{edge_type}',3,22,11)
        v_road(23,2,23)
        vlabel(f'W{edge_type}',22,3,11)
    elif dir.lower() == 's':
        h_road(2,WIDTH-2, 7)
        hlabel(f'S{edge_type}',27,8,12)
    elif dir.lower() == 'sw':
        h_road(2,23,7)
        hlabel(f'S{edge_type}',3,8,11)
        v_road(23,7,28)
        swvcurbx = WIDTH - 7
        swvcurby1 = HEIGHT - 23
        swvcurby2 = HEIGHT - 2
        vlabel(f'W{edge_type}',swvcurbx - 1,swvcurby2 -1,11)
    elif dir.lower() == 'se':
        sehcurbx1 = 7
        sehcurbx2 = 28
        sehcurby = 7
        sevcurbx = 7
        sevcurby1 = 7
        sevcurby2 = 28
        h_road(sehcurbx1,sehcurbx2,sehcurby)
        hlabel(f'S{edge_type}',sehcurbx2-1,sehcurby - 1,11)
        v_road(sevcurbx,sevcurby1,sevcurby2)
        vlabel(f'E{edge_type}',sevcurbx+1, sevcurby2 - 1,11)

    elif dir.lower() == 'e':
        v_road(7,2,HEIGHT-2)
        vlabel(f'E{edge_type}',8,3,12)
    elif dir.lower() == 'w':
        v_road(23,2,HEIGHT-2)
        vlabel(f'W{edge_type}',22,3,12)
    landbase = dir
    return landbase

def set_street_name(street,landbase):
    #enters street name on sketch
    if landbase == 'n':
        hlabel(street,15,27,20)
    elif landbase == 's':
        hlabel(street,15,3,20)
    elif landbase == 'e':
        vlabel(street,3,15,20)
    elif landbase == 'w':
        vlabel(street,27,15,20)

def get_intersection_name():
    hstreet = get_input('Enter horizontal street name')
    vstreet = get_input('Enter vertical street name')
    return hstreet,vstreet

def set_intersection_name(hstreet,vstreet,landbase):
    if landbase == 'ne':
        set_street_name(hstreet,'n')
        set_street_name(vstreet,'e')
    elif landbase == 'nw':
        set_street_name(hstreet,'n')
        set_street_name(vstreet, 'w')
    elif landbase == 'se':
        set_street_name(hstreet,'s')
        set_street_name(vstreet,'e')
    elif landbase == 'sw':
        set_street_name(hstreet,'s')
        set_street_name(vstreet,'w')

def get_digbox():
    pass

def set_digbox():
    pass



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

def cable_poly(*points):
    try:
        cable = sg.Graph.draw_lines(graph,points,width='2')
        TK.itemconfig(cable,dash=(10,5))
        TK.addtag_withtag('cable',cable)
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
                    gap = 5
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
                    gap = 5
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

def get_figure_type(tag_or_id):
    fig_type = TK.type(tag_or_id)
    return fig_type

def get_figure_coords(tag_or_id):
    fig_coords = TK.coords(tag_or_id)
    return fig_coords

def clone_item(tag_or_ID):
    config = TK.itemconfig(tag_or_ID)
    clone = {key: config[key][-1] for key in config.keys()}
    return clone

def paste_figure(fig_type, coords,clone):
    if clone is not None:
        new_coords  = [coord + 10 for coord in coords]
        if fig_type == 'rectangle':
            TK.create_rectangle(new_coords, **clone)
        elif fig_type == 'oval':
            TK.create_oval(new_coords, **clone)
        elif fig_type == 'line':
            TK.create_line(new_coords, **clone)
        elif fig_type == 'text':
            TK.create_text(new_coords, **clone)
        elif fig_type == 'image':
            TK.create_image(new_coords, **clone)






def digbox(x1, y1, x2, y2):
    try:
        db = graph.draw_rectangle((x1, y1), (x2, y2), fill_color="gainsboro", line_color="black")
        graph.TKCanvas.itemconfig(db, stipple="gray25")
        graph.send_figure_to_back(db)
        TK.addtag_withtag('digbox',db)
    except:
        logerror()

def located_area(x, y):
    try:
        sg.Graph.draw_text(graph, "LOCATED AREA", (x, y), font="Arial 11 bold")
    except:
        logerror()

def house(x, y, size, num):
    if size == "m":
        bldng = sg.Graph.draw_rectangle(graph,(x,y),(x+6,y+6),line_color='black',fill_color='white')
        hnumber = hlabel(num,x+3,y+3,16)
        nbl = hlabel('NBL',x+3,y-1,10)
        sbl = hlabel('SBL',x+3,y+7,10)
        wbl = vlabel('WBL',x-1,y+3,10)
        ebl = vlabel('EBL',x+7,y+3,10)
        for x in bldng,hnumber,nbl,sbl,wbl,ebl:
            group('house_m','x')
    elif size == 'l':
        bldng = sg.Graph.draw_rectangle(graph,(x,y),(x+8,y+8),line_color='black',fill_color='white')
        hnumber = hlabel(num,x+4,y+4,16)
        nbl = hlabel('NBL',x+4,y-1,10)
        sbl = hlabel('SBL',x+4,y+9,10)
        wbl = vlabel('WBL',x-1,y+4,10)
        ebl = vlabel('EBL',x+9,y+4,10)
        for x in bldng,hnumber,nbl,sbl,wbl,ebl:
            group('house_l','x')
    elif size == 's':
        bldng = sg.Graph.draw_rectangle(graph,(x,y),(x+4,y+4),line_color='black',fill_color='white')
        hnumber = hlabel(num,x+2,y+2,16)
        nbl = hlabel('NBL',x+2,y-1,10)
        sbl = hlabel('SBL',x+2,y+5,10)
        wbl = vlabel('WBL',x-1,y+2,10)
        ebl = vlabel('EBL',x+5,y+2,10)
        for x in bldng,hnumber,nbl,sbl,wbl,ebl:
            group('house_s','x')

def centre_pole():
    pole(15,15)

def centre_ped():
    ped(15,15)

def centre_tx():
    transformer(15,15)

def centre_stamp():
    item_stamp(15,15)

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

def edit_text():
    try:
        string = popup_get_text('Enter new text')
        TK.itemconfig('current',text=string)
    except:
        popup('Not a text object')
        pass

def get_input(prompt):
    return popup_get_text(prompt)

def read_from_template(file):
    if file is not None:
        try:
            with open(file) as f:
                flist = f.readlines()
                lb_strlist = flist[0].split()
                dir = lb_strlist[0]
                edge_type = lb_strlist[1].strip()
                landbase = set_landbase(dir,edge_type)
                if dir in ['ne','nw','se','sw']:
                    set_intersection_name(flist[1],flist[2],landbase)
                else:
                    set_street_name(flist[1],landbase)

        except IndexError:
            pass

        except:
            logging.exception('error')
            popup('There was an error in template file')

def save_sketch_template(file=''):
    if file is not None:
        filename = file
    else:
        filename = popup_get_file('Save template as', save_as=True)
    typelist = []
    coordslist = []
    clonelist = []
    list_of_all_figures = []
    for id in TK.find_all():
        typelist.append(get_figure_type(id))
        coordslist.append(get_figure_coords(id))
        clonelist.append(clone_item(id))
    list_of_all_figures.extend([typelist,coordslist,clonelist])
    easy_print(list_of_all_figures)
    with open(filename+'.pkl','wb') as pk:
        pickled_obj = pickle.dump(list_of_all_figures,pk)

def load_sketch_template():
        try:
            filename = popup_get_file('Choose template file...')
            with open(f'{filename}.pkl','rb') as pk:
                list_of_all_figures = pickle.load(pk)
            typelist = list_of_all_figures[0]
            coordslist = list_of_all_figures[1]
            clonelist = list_of_all_figures[2]
            for x,y,z in zip(typelist,coordslist,clonelist):
                if x == 'rectangle':
                    TK.create_rectangle(y,**z)
                elif x == 'oval':
                    TK.create_oval(y, **z)
                elif x == 'line':
                    TK.create_line(y, **z)
                elif x == 'text':
                    TK.create_text(y, **z)
                #elif x == 'image':
                    #TK.create_image(y, **z)
                elif x == 'polygon':
                    TK.create_polygon(y, **z)
                elif x == 'arc':
                    TK.create_arc(y, **z)   
        except:
            pass 
#callback routines

def short_gas():
    try:
        dir = popup_get_text('N, S, E, W?')
        hnum = popup_get_text('House number?')
        street = popup_get_text('Street name?')
        landbase = set_landbase(dir)
        set_street_name(street,landbase)
        if dir.lower() == 'n':
            digbox(7,1,23,27)
            house(11,4,'l',hnum)
        elif dir.lower() == 's':
            digbox(7,3,23,29)
            house(11,18,'l',hnum)
            hlabel('LOCATED AREA',15,14,12)
        elif dir.lower() == 'e':
            digbox(3,7,29,23)
            house(18,11,'l',hnum)
        elif dir.lower() == 'w':
            digbox(1,7,27,23)
            house(4,11,'l',hnum)
        else:
            easy_print(logging.exception('err'))
            pass

    except:
        easy_print(logging.exception('err'))
        pass

def long_gas():
    try:
        dir = popup_get_text('N, S, E, W?')
        hnum = popup_get_text('House number?')
        street = popup_get_text('Street name?')
        if dir.lower() == 'n':
            h_road(2,28,16)
            h_road(2,28,22)
            hlabel('NRE',27,15,11)
            hlabel('SRE',27,21,11)
            digbox(4,0,26,29)
            house(12,3,'m',hnum)
            hlabel(street,15,19,20)
            pass
        elif dir.lower() =='s':
            h_road(2,28,8)
            h_road(2,28,14)
            hlabel('NRE',27,7,11)
            hlabel('SRE',27,15,11)
            digbox(4,1,26,30)
            house(11,20,'m',hnum)
            hlabel(street,15,11,20)
        elif dir.lower() =='e':
            pass
        elif dir.lower() == 'w':
            v_road(16,2,28)
            v_road(22,2,28)
            vlabel('WCL',15,3,11)
            vlabel('ECL',23,3,11)
            digbox(0,4,29,26)
            house(2,11,'m',hnum)
            vlabel(street,19,15,20)
        else:
            easy_print(logging.exception('err'))
    except:
        easy_print(logging.exception('err'))
        pass

def radius_sketch():
    feature = ['ped','pole','tree','transformer','waterbox']
    user_type = popup_get_text('Object type ?(ped,pole,tree,transformer,waterbox')
    radius = int(popup_get_text('Radius in m?(int)'))
    if user_type not in feature:
        popup_get_text('Not a valid entry')
        return
    radiusdict ={
                    'ped' : centre_ped,
                    'pole': centre_pole,
                    'tree': centre_stamp,
                    'transformer': centre_tx,
                    'waterbox': centre_stamp,
                }
    radiusdict[user_type]()
    if radius < 3:
        digbox(13,13,17,17)
    else:
        digbox(10,10,20,20)

def st_to_st():
    dir = popup_get_text('Landbase? (N,S,E,W)')
    street1 = popup_get_text('Street 1 (W or N)')
    street2 = popup_get_text('Street 2 (mid)')
    street3 = popup_get_text('Street 3 (S or E)')
    if dir.lower() == 'n':
        h_road(3,27,20)
        v_road(3,10,20)
        v_road(27,10,20)
        hlabel('NCL',25,19,11)
        vlabel('ECL',4,11,11)
        vlabel('WCL',26,11,11)
        vlabel(street1,1,15,20)
        hlabel(street2,15,23,20)
        vlabel(street3,29,15,20)

    elif dir.lower() == 's':
        h_road(3,27,10)
        v_road(3,10,20)
        v_road(27,10,20)
        hlabel('SCL',26,9,11)
        vlabel('ECL',27,21,11)
        vlabel('WCL',3,21,11)
        vlabel(street1,1,15,20)
        hlabel(street2,15,7,20)
        vlabel(street3,29,15,20)

    elif dir.lower() == 'w':
        v_road(20,3,27)
        h_road(10,20,3)
        h_road(10,20,27)
        hlabel('SCL',11,4,11)
        vlabel('WCL',21,15,11)
        hlabel('NCL',11,26,11)
        hlabel(street1,11,1,20)
        vlabel(street2,26,15,20)
        hlabel(street3,11,29,20)

    elif dir.lower() == 'e':
        v_road(10,3,27)
        h_road(10,20,3)
        h_road(10,20,27)
        hlabel('SCL',19,4,11)
        hlabel('NCL',19,26,11)
        vlabel('ECL',9,14,11)
        hlabel(street1,21,2,20)
        vlabel(street2,5,14,20)
        hlabel(street3,21,28,20)

def bl_to_bl():
    dir = get_input('N, S, E or W?')
    hnum1 = get_input('House number 1?')
    if dir in ['nw','ne','se','sw']:
        hstreet,vstreet = get_intersection_name()
        set_intersection_name(hstreet,vstreet,dir)
        landbase = set_landbase(dir)
    else:
        hnum2 = get_input('House number 2?')
        street = get_input('Street name?')
        landbase = set_landbase(dir)
        set_street_name(street,landbase)
    if dir.lower() == 'n':
        house(*NBLHOUSE1,hnum1)
        house(*NBLHOUSE2,hnum2)
        digbox(*NPLTOPL_DIGBOX)
    elif dir.lower() == 'nw':
        house(*NWBLHOUSE,hnum1)
        digbox(*NWPLTOPL_DIGBOX)
    elif dir.lower() == 'ne':
        house(*NEBLHOUSE,hnum1)
        digbox(*NEPLTOPL_DIGBOX)
    elif dir.lower() == 's':
        house(*SBLHOUSE1,hnum1)
        house(*SBLHOUSE2,hnum2)
        digbox(*SPLTOPL_DIGBOX)
    elif dir.lower() == 'sw':
        house(*SWBLHOUSE,hnum1)
        digbox(*SWPLTOPL_DIGBOX)
    elif dir.lower() == 'e':
        house(*EBLHOUSE1,hnum1)
        house(*EBLHOUSE2,hnum2)
        digbox(*EPLTOPL_DIGBOX)
    elif dir.lower() == 'w':
        house(*WBLHOUSE1,hnum1)
        house(*WBLHOUSE2,hnum2)
        digbox(*WPLTOPL_DIGBOX)
#barebones

notify = sg.Text()
notify2 = sg.Text()
notify3 = sg.Text()

menu_def = [
            ['File', ['Save','Save template as...', 'Load template']],
            ['Size',['24','30']],
]

tab2layout = [
    [
        sg.Text('Curb: '), sg.DropDown(('N','S','E','W'),k='curbddl'),
        sg.Radio('CL','roadtype',k='cl'), sg.Radio('RE','roadtype',k='re')
    ],
    [
        sg.B('Change street',k='tab1getstreet'), sg.T(k='tab1street'),
    ],
    [
        sg.B('Intersecting street:',k='tab2getstreet'), sg.I(k='tab1intersection')
    ],
    [
        sg.Submit(k='sketchbuild_submit')
    ]
 ]

tab1layout = [
    [
        sg.B('Read template',enable_events=True,k='read_file')
    ]
]
lcol = [
     [
         sg.TabGroup(
             [
             [
                 sg.Tab('SketchBuilder',tab1layout)
             ]
         ],visible=True
         )
     ]
 ]

canvasmenu = ['',['Snap to Grid']]

col = [
    [   
        notify, notify2, notify3
    ],
    [
        sg.Graph(
            canvas_size=(600, 600),
            graph_bottom_left=(0, HEIGHT),
            graph_top_right=(WIDTH, 0),
            background_color="white",
            right_click_menu=canvasmenu,
            key="graph",
            enable_events=True,
            drag_submits=True,
            expand_x=True,
            expand_y=True
        ),
    ],
    [
        sg.Button('Short Gas',enable_events=True),sg.Button('Long Gas',enable_events=True),
        sg.Button('Radius',enable_events=True),sg.Button('St to St',enable_events=True),sg.Button('BL to BL',enable_events=True)
    ],
    ]



layout = [
    [
        sg.Column(lcol),
        sg.Menu(menu_def),
        sg.Column(col)
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
graph = window["graph"]
TK = graph.TKCanvas
# DRAW HERE
#SETUP

mode = {0:'select', 1:'get points', 2:'draw'}
current_mode = 'regular'
x = y = a = b = None
isGrid = False
gridSnap = True
graph.bind('<B1-Motion>','drag')
graph.bind('<Motion>','motion')
selected = []
dragging = False
start_point = end_point = prior_rect = None

#cable_poly((14,0),(14,6),(20,6))

#testing unpacking this is neat

#small loop - lol not anymore
while True:
    event, values = window.read()
    notify2.update(selected)
    notify3.update(event)
    if event == sg.WIN_CLOSED:
        break

    #change drawing size

    if event == 'Save':
        _savefile = popup_get_text('Save file name?')
        try:
            save_element_as_file(graph, f'C:\\Users\\Cr\\Documents\\{_savefile}.png')
            save_sketch_template(_savefile)
        except ValueError:
            popup('Missing file extension. Please try again')
    if event == 'Save template only':
        save_sketch_template()
    if event == 'Load template':
        load_sketch_template()

    if event == 'Snap to Grid':
        if gridSnap == True:
            gridSnap = not gridSnap
            snap_to_grid_off()
            notify3.update(f'Snap to grid: {gridSnap}')
        else:
            gridSnap = not gridSnap
            snap_to_grid_on()
            notify3.update(f'Snap to grid: {gridSnap}')

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
    elif event == 'Long Gas':
        long_gas()
    elif event == 'Radius':
        radius_sketch()
    elif event == 'St to St':
        st_to_st()
    elif event == 'BL to BL':
        bl_to_bl()
    #left hand stuff

    if event == 'tab1getstreet':
        street = get_input('Enter street name')
        window['tab1street'].update(street)
    
    if event == 'read_file':
        file = popup_get_file('Choose template')
        read_from_template(file)

    if event == 'sketchbuild_submit':
        #draw sketchbuilder output
        
        if values['cl'] == True:
                rtype = 'CL'
        else:
                rtype = 'RE'
        if values['curbddl'] == 'N':
            road(NCURB[0],NCURB[1],NCURB[2],NCURB[3])
            hlabel(values['curbddl'] + rtype,WIDTH-3,NCURB[1]-1,9)
            hlabel(street,NSTREET[0],NSTREET[1],20)
        elif values['curbddl'] == 'S':
            road(SCURB[0],SCURB[1],SCURB[2],SCURB[3])
            hlabel(values['curbddl'] + rtype,WIDTH-3,SCURB[1]+1,9)
            hlabel(street,SSTREET[0],SSTREET[1],20)
        elif values['curbddl'] == 'W':
            road(WCURB[0],WCURB[1],WCURB[2],WCURB[3])
            vlabel(values['curbddl'] + rtype,WCURB[0]-1,HEIGHT-3,9)
            vlabel(street,WSTREET[0],WSTREET[1],20)
        elif values['curbddl'] == 'E':
            road(ECURB[0],ECURB[1],ECURB[2],ECURB[3])
            vlabel(values['curbddl']+rtype,ECURB[0]-1,HEIGHT-3,9)
            vlabel(street, ESTREET[0], ESTREET[1],20)
    
    if event == 'm' and current_mode=='chosen':
        notify.update('Please click location to move to')
        current_mode='move'


    if event.endswith('motion'):
        notify2.update(values['graph'])
        notify3.update(TK.find_withtag('current'))
    
    if event.endswith('motion') and current_mode == 'move':
        try:
            for item in selected:
                TK.itemconfig(item,state='disabled')
                sg.Graph.relocate_figure(graph,item,values['graph'][0],values['graph'][1])
                TK.itemconfig(item,state='normal')
        except IndexError:
            pass

    if event == 'graph' and current_mode == 'select':
        x,y = values['graph']
        if not dragging:
            start_point = (x,y)
            dragging = True
        else:
            end_point = (x,y)
        if prior_rect:
            graph.delete_figure(prior_rect)
    if event == 'graphdrag' and dragging == True:
        try:
            x,y = values['graph']
            end_point = (x,y)
            graph.delete_figure(prior_rect)
            prior_rect = sg.Graph.draw_rectangle(graph,start_point,end_point,line_color='blue',line_width=1)
            TK.coords(prior_rect,start_point[0]*20,start_point[1]*20,end_point[0]*20,end_point[1]*20)
        except:
            pass
    if event == 'graphdrag' and current_mode == 'chosen':
        x,y = values['graph']
        try:
            for item in selected:
                graph.relocate_figure(item,x,y)
        except IndexError:
            pass

    if event=='graphpoly':
        notify2.update('Polyline')


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
        if selected is not None:
            for item in selected:
                if TK.type(item) == 'rectangle' or TK.type(item) == 'ellipse':
                    TK.itemconfig(item,fill='white',outline='black')
                elif TK.type(item) == 'line' or TK.type(item) == 'text' or TK.type(item) =='polygon':
                    TK.itemconfig(item,fill='black')
                elif TK.type(item) == 'rectangle' and TK.itemcget(item,'tag') == 'digbox':
                    TK.itemconfig('digbox',fill='#D3D3D3',stipple='gray25')
                selected.remove(item)
        #graph.delete_figure(bbr)

    if event == 'n':
        current_mode = 'polyline'
        notify.update('Click next point of line')

    if event == 'F2:113':
        edit_text()
    if event =='>':
        current_mode = 'arrow1'
        notify.update('Please click first arrow head:')
    if event == 's':
        current_mode = 'select'
        notify.update('Select figure')
    if event == 'i':
        img = popup_get_file('Select image')
        sg.Graph.draw_image(graph,location=(0,0),data=convert_to_bytes(img))
    if event == 'a':
        current_mode = 'arc'
        notify.update('Please select first arc point')
    if event == 'h':
        current_mode = 'harrow'
        notify.update('Please select first arrow point')
    if event == 'v':
        current_mode = 'varrow'
        notify.update('Please select first arrow point')
    if event == 'c':
        current_mode = 'cable'
        notify.update('Please click first point of cable line:')
    if event == 'C':
        current_mode = 'cable arc'
        notify.update('Please click horizontal section of cable arc')
    if event == 'o':
        current_mode = 'offsetline'
        notify.update('Please click first point of offset line:')
    if event == 'd':
        current_mode = 'digbox'
        notify.update('Please click first point of box: ')
    if event == 'b':
        current_mode = 'building'
        notify.update('Please click upper left corner of building: ')
    if event == 'B':
        current_mode = 'house'
        notify.update('Please click upper left corner of house')
    if event == 'r':
        current_mode = 'road'
        notify.update('Please click first point of curb line')
    if event == 'R':
        current_mode = 'road arc'
        notify.update('Please click horizontal section of road arc')
    if event == 'l':
        current_mode = 'line'
        notify.update('Please click first point of line')
    if event == 'y':
        if TK.find_withtag('current') is not None:
            clone = clone_item('current')
            coords = get_figure_coords('current')
            figure_type = get_figure_type('current')
    if event == 'p':
        paste_figure(figure_type,coords,clone)
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
    if event == 'x':
        if TK.find_withtag('current') is not None:
            graph.delete_figure(TK.find_withtag('current'))
    if event == 't':
        current_mode = 'text'
        entered_text = popup_get_text('Enter text')
        notify.update('Please click to enter text')
    if event == 'T':
        current_mode = 'vtext'
        entered_text = popup_get_text('Enter text')
        notify.update('Please click to enter text')
    if event == 'e':
        current_mode = 'street text'
        entered_text = popup_get_text('Enter street name')
        notify.update('Please click to enter text')
    if event == 'E':
        current_mode = 'street vtext'
        entered_text = popup_get_text('Enter street name')
        notify.update('Please click to enter text')
    if event == '1':
        current_mode = 'ped'
        notify.update('Click to place pedestal')
    if event == '!':
        current_mode = 'ped stub'
        notify.update('Click on ped location')
    if event == '2':
        current_mode = 'pole'
        notify.update('Click to place pole')
    if event == '@':
        current_mode = 'pole stub'
        notify.update('Click on pole location')
    if event == '3':
        current_mode = 'itemstamp'
        notify.update('Click to place stamp')
    if event == '4':
        current_mode = 'transformer'
        notify.update('Click to place transformer')
    if event == '5':
        current_mode = 'vault'
        notify.update('Click to place vault')
    if event == '6':
        current_mode = 'catch basin'
        notify.update('Click on catch basin location')

    if event.endswith('+UP'):
        #signals end of drag 
        graph.delete_figure(prior_rect)
        dragging = False
        start_point = end_point = prior_rect = None

        if current_mode == 'cable':
            x, y = get_point1()
            point1 = draw_point1(x,y)
            notify.update('Click second point of line')
            current_mode='cable2'
        if current_mode == 'polyline':
            x, y = get_point1()
            point1 = draw_point1(x,y)
            notify.update('Click next point of line')
            current_mode = 'cablenext'
        elif current_mode == 'cable arc':
            x, y = get_point1()
            point1 = draw_point1(x,y)
            notify.update('Click vertical section of cable arc')
            current_mode = 'cable arc 2'
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
            hn = popup_get_text('House number:?')
            hs = popup_get_text('Size (s/m/l):')
            try:
                house(x,y,hs,hn)
            except:
                logging.exception('ERROR')

        elif current_mode == 'building':
            x,y = get_point1()
            point1 = draw_point1(x,y,'black')
            notify.update('Click lower right corner of building')
            current_mode = 'building2'
        elif current_mode == 'road':
            x,y = get_point1()
            point1 = draw_point1(x,y,'purple')
            notify.update('Click second point of curb')
            current_mode = 'road2'
        elif current_mode == 'road arc':
            x,y = get_point1()
            point1 = draw_point1(x,y,'purple')
            notify.update('Click vertical section of road arc')
            current_mode = 'road arc 2'
        elif current_mode == 'line':
            x,y = get_point1()
            point1 = draw_point1(x,y,'blue')
            notify.update('Click second point of line')
            current_mode = 'line2'
        elif current_mode == 'arc':
            x,y = get_point1()
            point1 = draw_point1(x,y,'purple')
            notify.update('Click second arc point')
            current_mode = 'arc2'
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
        elif current_mode == 'arrow1':
            x,y = get_point1()
            point1 = draw_point1(x,y,'orange')
            notify.update('Click second arrow head')
            current_mode = 'arrow2'
        elif current_mode == 'arrow2':
            a,b = get_point2()
            point2 = draw_point2(x,y,color='orange')
            try:
                rarrow(x,y,a,b)
            except:
                
                #FIXME - can't put 2 arrow heads on same point - crashes
                pass
            cleanup_2point()

        elif current_mode == 'cable2':
            a, b = get_point2()
            point2 = draw_point2(x,y,'red')
            label = popup_get_text('Label? ')
            cable(x, y, a, b,label)
            cleanup_2point()
            current_mode = 'cable'
        elif current_mode == 'cablenext':
            cpoints = []
            collecting = True
            while collecting:
                a,b = get_point2()
                point2 = draw_point2(a,b,'red')
        elif current_mode == 'cable arc 2':
            a, b = get_point2()
            point2 = draw_point2(x,y,'red')
            arc(x, y, a, b, 'cable')
            cleanup_2point()
            current_mode == 'cable arc'
        elif current_mode == 'offsetline2':
            a, b = get_point2()
            point2 = draw_point2(x,y,'brown')
            offset_line(x,y,a,b)
            cleanup_2point()
        elif current_mode == 'digbox2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'green')
            digbox(x,y,a,b)
            cleanup_2point()
        elif current_mode == 'building2':
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
        elif current_mode == 'road arc 2':
            a,b =get_point2()
            point2 =draw_point2(a,b,'purple')
            arc(x,y,a,b,'road')
            cleanup_2point()
            current_mode = 'road arc'
        elif current_mode == 'line2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'blue')
            line(x,y,a,b)
            cleanup_2point()
            current_mode = 'line'
        elif current_mode == 'arc2':
            a,b = get_point2()
            point2 = draw_point2(a,b,'purple')
            arc(x,y,a,b)
            cleanup_2point()
            current_mode = 'arc'
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
        elif current_mode == 'street text':
            x,y = get_point1()
            hlabel(entered_text,x,y,20)
            x=y=entered_text=None
        elif current_mode == 'street vtext':
            x,y = get_point1()
            vlabel(entered_text,x,y,20)
            x=y=entered_text=None
        elif current_mode == 'vtext':
            x, y = get_point1()
            vlabel(entered_text,x,y,12)
            x = y = entered_text = None
        elif current_mode == 'ped':
            x, y = get_point1()
            ped(x,y)
            x=y=None
        elif current_mode == 'ped stub':
            x, y = get_point1()
            point1 = draw_point1(x, y)
            notify.update('Click cable stub end')
            current_mode = 'ped stub 2'
        elif current_mode == 'ped stub 2':
            a, b = get_point2()
            point2 = draw_point2(x, y, 'red')
            ped_1arm(x,y,a,b)
            cleanup_2point()
        elif current_mode == 'pole':
            x, y = get_point1()
            pole(x,y)
            x=y=None
        elif current_mode == 'pole stub':
            x , y = get_point1()
            point1 = draw_point1(x, y)
            notify.update('Click cable stub end')
            current_mode = 'pole stub 2'
        elif current_mode == 'pole stub 2':
            a, b = get_point2()
            point2 = draw_point2(a, b, 'red')
            pole_1arm(x,y,a,b)
            cleanup_2point()
        elif current_mode == 'itemstamp':
            x,y = get_point1()
            item_stamp(x,y)
            x=y=None
        elif current_mode == 'transformer':
            x,y = get_point1()
            transformer(x,y)
            x=y=None
        elif current_mode == 'vault':
            x,y = get_point1()
            utility = get_input('Bell?')
            if utility in ['y','Y','yes','YES','Yes']:
                vault(x, y, 'b')
            else:
                vault(x,y)
        elif current_mode == 'catch basin':
            x,y = get_point1()
            catch_basin(x,y)
        elif current_mode == 'select':
            fig = TK.find_withtag('current')
            # drag_figures =sg.Graph.get_figures_at_location(graph,values['graph'])
            # if drag_figures:
            #     for fig in drag_figures:
            #         if TK.itemcget(fig,'tag') == 'grid':
            #             pass
            #         else:
                    #easy_print(graph.TKCanvas.type(fig))
                #easy_print(type(fig))
                        #bb = sg.Graph.get_bounding_box(graph,fig)
                        #bbr= sg.Graph.draw_rectangle(graph,(bb[0]),bb[1], line_color='blue')
                        #notify2.update(TK.type(fig) + ',' +TK.itemcget(fig,'tag'))
            if 'ped' in TK.gettags(fig):
                TK.itemconfig(fig,fill='green')
                TK.itemconfig(fig[0]+1,fill='green')
                selected.append(fig)
                selected.append(fig[0]+1)
            else:
                TK.itemconfig(fig,fill='red')
                selected.append(fig)
            current_mode = 'chosen'

        elif current_mode=='move':
            try:
                x,y=get_point1()
                for item in selected:
                    graph.relocate_figure(item,x,y)
                # if TK.itemcget(fig,'tag') == 'arrow1':
                #     graph.relocate_figure('arrow1',x,y)
                # elif TK.itemcget(fig,'tag') == 'arrow2':
                #     graph.relocate_figure('arrow2',x,y)
                # elif TK.itemcget(fig,'tag') == 'cable':
                #     graph.relocate_figure('cable',x,y)
                # else:
                #     graph.relocate_figure(fig,x,y)
                #sg.Graph.delete_figure(bbr)
                #TK.itemconfig(fig,fill='black')
                x=y=None
            except:
                logging.exception('There was an error')


window.close()
