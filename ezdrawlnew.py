# import section
from tkinter import W
import tkinter
from PySimpleGUI.PySimpleGUI import (
    easy_print,
    popup,
    popup_get_file,
    popup_get_text,
    popup_yes_no,
)
import typing
import base64
import io
import json
import logging
import pathlib
import pickle
import time
from enum import Enum
import PIL.Image
from PIL.Image import LANCZOS
import PySimpleGUI as sg



from typing import Final, Literal


# init canvas
sg.theme(new_theme="darkgrey11")
sg.set_global_icon(r"./resources/TICO.PNG")
sg.set_options(font=("Segoe UI", 10, "normal"))

logging.basicConfig(filename="ezdraw.log", level=logging.DEBUG, format="%(asctime)s")
Print = easy_print
# CONSTANTS

edge_type: str = ""
HEIGHT: int = 60  # height of drawing window
WIDTH: int = 70  # width of drawing window

grid_location = ".\\resources\\grid2.png"
# key mapping
# key handler class with method get keys
if sg.running_linux():
    keys: dict[str, str] = {
        "esc": "Escape:9",
        "g": "g:42",
        "down": "Down:116",
        "up": "Up:111",
        "right": "Right:114",
        "left": "Left:113",
        "r": "r:27",
        "R": "R:27",
        "c": "c:54",
        "C": "C:54",
        "s": "s:39",
        "d": "d:40",
        "w": "w:25",
        "a": "a:38",
        "e": "e:26",
        "E": "E:26",
        "q": "q:24",
        "z": "z:52",
        "x": "x:53",
        "f": "f:41",
        "v": "v:55",
        "t": "t:28",
        "T": "T:28",
        "y": "y:29",
        "u": "u:30",
        "i": "i:31",
        "o": "o:32",
        "p": "p:33",
        "h": "h:43",
        "j": "j:44",
        "k": "k:45",
        "l": "l:46",
        "n": "n:57",
        "m": "m:58",
        "b": "b:56",
        "B": "B:56",
        "V": "V:55",
        "1": "1:10",
        "2": "2:11",
        "3": "3:12",
        "4": "4:13",
        "5": "5:14",
        "6": "6:15",
        "7": "7:16",
        "8": "8:17",
        "9": "9:18",
        "0": "0:19",
        "=": "equal:21",
        "_": "underscore:20",
        ">": "greater:60",
        "F1": "F1:67",
        "F2": "F2:68",
    }
else:
    keys: dict[str,str]= {
        "esc": "Escape:27",
        "g": "g",
        "down": "Down:40",
        "up": "Up:38",
        "right": "Right:39",
        "left": "Left:37",
        "r": "r",
        "R": "R",
        "c": "c",
        "C": "C",
        "s": "s",
        "d": "d",
        "w": "w",
        "a": "a",
        "e": "e",
        "E": "E",
        "q": "q",
        "z": "z",
        "x": "x",
        "f": "f",
        "v": "v",
        "t": "t",
        "T": "T",
        "y": "y",
        "m": "m",
        "=": "=",
        "n": "n",
        "F2": "F2:113",
        "F1": "F1",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        ">": ">",
        "i": "i",
        "h": "h",
        "V": "V",
        "o": "o",
        "b": "b",
        "B": "B",
        "p": "p",
        "l": "l",
        "k": "k",
        "j": "j",
        "u": "u",
        "0": "0",
        "9": "9",
        "8": "8",
        "7": "7",
        "_": "_",



        # More keys can be added here
    }

# moved to separate constants file
# the four values correspond to int values of points on a line (x1,y1,x2,y2)
ECURB: list[int] = [WIDTH // 3, HEIGHT * 0.067, WIDTH // 3, HEIGHT * 0.933]
WCURB: list = [(WIDTH * 2) // 3, HEIGHT * 0.067, (WIDTH * 2) // 3, HEIGHT * 0.933]
NCURB: list = [
    WIDTH * (1 / WIDTH),
    HEIGHT * 2 // 3,
    WIDTH * 69 // WIDTH,
    HEIGHT * 2 // 3,
]
SCURB: list = [WIDTH * (1 / WIDTH), HEIGHT // 3, WIDTH - 2, HEIGHT // 3]
HNCURB: list = [NCURB[0], SCURB[1] + HEIGHT / 15, NCURB[2], SCURB[1] + HEIGHT / 15]
HSCURB: list = [SCURB[0], NCURB[1] - HEIGHT / 15, NCURB[2], NCURB[1] - HEIGHT / 15]

# these are x,y (int) coordinates for street text labels
NSTREET: list = [WIDTH // 2, (NCURB[1] + HEIGHT) // 2]
SSTREET: list = [WIDTH / 2, (SCURB[1]) / 2]  # type: ignore
WSTREET: list = [(WCURB[0] + WIDTH) / 2, HEIGHT / 2]
ESTREET: list = [ECURB[0] / 2, HEIGHT / 2]

HSTREET: list = [WIDTH / 2, HEIGHT / 2]

# curb labels
HNCURBLABEL: list = [(65 / 70) * WIDTH, (42 / 60) * HEIGHT, 12]  # x, y , fontsize
HSCURBLABEL: list = [(65 / 70) * WIDTH, (18 / 60) * HEIGHT, 12]
WCURBLABEL: list = [(40 / 70) * WIDTH, (6 / 60) * HEIGHT, 12]
ECURBLABEL: list = [(22 / 70) * WIDTH, (6 / 60) * HEIGHT, 12]


NBLHOUSE1: tuple = (WIDTH * 0.10, HEIGHT * 0.2, "m")
NBLHOUSE2: tuple = (WIDTH * 0.80, HEIGHT * 0.2, "m")
NWBLHOUSE: tuple = (8, 8, "m")
NEBLHOUSE: tuple = (18, 8, "m")
SBLHOUSE1: tuple = (WIDTH * 0.1, HEIGHT * 0.7, "m")
SBLHOUSE2: tuple = (WIDTH * 0.8, HEIGHT * 0.7, "m")
SWBLHOUSE: tuple = (9, 16, "m")
SEBLHOUSE: tuple = (16, 16, "m")
WBLHOUSE1: tuple = (WIDTH * 0.2, HEIGHT * 0.1, "m")
WBLHOUSE2: tuple = (WIDTH * 0.2, HEIGHT * 0.8, "m")
EBLHOUSE1: tuple = (WIDTH * 0.7, HEIGHT * 0.1, "m")
EBLHOUSE2: tuple = (WIDTH * 0.7, HEIGHT * 0.8, "m")

NPLTOPL_DIGBOX: Final = (6, 16, 24, 28)
NWPLTOPL_DIGBOX: Final = (8, 8, 28, 28)
NEPLTOPL_DIGBOX: Final = (4, 8, 24, 28)
SPLTOPL_DIGBOX: Final = (6, 2, 24, 14)
SWPLTOPL_DIGBOX: Final = (9, 3, 27, 22)
SEPLTOPL_DIGBOX: Final = (3, 3, 22, 22)
WPLTOPL_DIGBOX: Final = (14, 6, 28, 24)
EPLTOPL_DIGBOX: Final = (2, 2, 15, 28)

N_DW1 = ()
N_DW2 = ()
S_DW1 = ()
S_DW2 = ()
W_DW1 = ()
W_DW2 = ()
E_DW1 = ()
E_DW2 = ()
NW_DW = ()
NE_DW = ()
SW_DW = ()
SE_DW = ()


h_cursor_line = None
v_cursor_line = None
input_mode = "mouse"
notify = sg.Text()
notify2 = sg.Text()
notify3 = sg.Text()
notify_inputmode = sg.Text(input_mode)


class CurrentMode(Enum):
    """
    Enum representing the current mode of the application.

    Modes:
    SELECT: The user is in selection mode.
    CHOSEN: An object has been selected.
    DRAW: The user is in drawing mode.
    MEASURE: The user is in measurement mode.
    DELETE: The user is in delete mode.
    MOVE: The user is in move mode.
    EDIT: The user is in edit mode.
    """
    SELECT = 1
    CHOSEN = 2
    DRAW = 3
    MEASURE = 4
    DELETE = 5
    MOVE = 6
    EDIT = 7



# classes


class TDInterface:
    def __init__(self):
        pass


# WRAPPER FUNCTIONS


def event_switch(modestring: str, notifystring: str, notification_element) -> str:
    mode = modestring
    notification_element.update(notifystring)
    return mode


def save_element_as_file(element, filename):
    """
    Saves any element as an image file.  Element needs to have an underlyiong Widget available (almost if not all of them do)
    :param element: The element to save
    :param filename: The filename to save to. The extension of the filename determines the format (jpg, png, gif, ?)
    """
    widget = element.Widget
    box = (
        widget.winfo_rootx(),
        widget.winfo_rooty(),
        widget.winfo_rootx() + widget.winfo_width(),
        widget.winfo_rooty() + widget.winfo_height(),
    )
    grab = ImageGrab.grab(
        bbox=box,
        include_layered_windows=True,
    )
    grab.save(filename)
    ImageGrab.grab(0)  # type: ignore


def add_figure_to_record(record: list, figtype: str, *args) -> None:
    figstr = ""
    figstr += figtype + ";"
    figstr += ";".join([str(x) for x in args])
    record.append(figstr)
    Print(record)


def convert_to_bytes(file_or_bytes, resize=None):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            logging.exception(e)
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize(
            (int(cur_width * scale), int(cur_height * scale)), resample=LANCZOS
        )
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def convert_measurement(meas:str=None) -> str | None:
    """
    Converts a measurement string to a formatted string with the unit 'm'.
    The input measurement string should be a number with one, two or three digits.
    If the input measurement is empty, None is returned.
    :return: A formatted string with the unit 'm'.
    :rtype: str or None

     Example:
       >>> convert_measurement('123')
    '1.23m'

    """
    newmeas:str = ""
    if meas is None:
        meas = sg.popup_get_text("Enter measurement(int)")
    if not isinstance(meas, str):
        meas = str(meas)

    try:
        if len(meas) == 1:
            newmeas = "0." + meas + "m"
            return newmeas
        elif len(meas) == 2:
            newmeas = meas[0] + "." + meas[1] + "m"
            return newmeas
        elif len(meas) == 3:
            newmeas = meas[0] + meas[1] + "." + meas[2] + "m"
            return newmeas
    except TypeError:
        logging.exception("empty measurement")
        return


def convert_multi_measurement() -> list:
    """
    returns a measurement list
    """
    measurements = popup_get_text("Enter measurements(int) separated by comma")
    lom: list = []
    if measurements is None:
        logging.exception("empty measurement")
        return []
    for p in measurements.split(","):
        if len(p) == 1:
            lom.append("0." + p + "m")
        elif len(p) == 2:
            lom.append(p[0] + "." + p[1] + "m")
        elif len(p) == 3:
            lom.append([0] + p[1] + "." + p[2] + "m")
    if len(lom) < 1:
        logging.exception("insufficent measurements")
        return []


def logerror(e):
    logging.exception(e)


def show_grid():
    """
    Displays an image of a grid on the drawing surface

    This function retrieves the grid image location, converts it to bytes, and then draws it on the .
    It then tags the grid for future reference, sends it to the back of all other figures on the graph,
    and disables any interactions with it.
    """
    grid_filename:str = grid_location
    grid_id:int = sg.Graph.draw_image(graph, location=(0, 0), data=convert_to_bytes(grid_filename))
    TK.addtag_withtag("grid", grid_id)
    sg.Graph.send_figure_to_back(graph, grid_id)
    TK.itemconfig(tagOrId="grid", state="disabled")


def snap_to_grid_off() -> None:
    """
    Turns off the snap-to-grid feature in the drawing window.

    This function changes the coordinates of the drawing window to a standard Cartesian plane,
    with the origin (0,0) at the top left. It also updates the global WIDTH and HEIGHT
    variables to match the new dimensions of the drawing window, and then updates the drawing to reflect these changes.
    """
    sg.Graph.change_coordinates(graph, (0, 600), (700, 0))
    global HEIGHT
    global WIDTH
    WIDTH = 700
    HEIGHT = 600
    graph.update()


def snap_to_grid_on():
    global HEIGHT
    global WIDTH
    HEIGHT = 60
    WIDTH = 70
    sg.Graph.change_coordinates(graph, (0, 60), (70, 0))
    graph.update()


def hide_grid():
    TK.itemconfig("grid", state="hidden")


def group(group_name: str, figure: int):
    TK.addtag_withtag(group_name, figure)


def wipe():

    """
    Erases drawing

    """

    confirm: str = popup_yes_no("Erase entire image?")
    if confirm == "Yes":
        graph.erase()
    else:
        pass


def draw_line_and_label(x1, y1, x2, y2, meas, is_horizontal):
    arrow1 = sg.Graph.draw_line(graph, (x1, y1), (x2, y2))
    arrow2 = sg.Graph.draw_line(graph, (x2, y2), (x1, y1))
    if is_horizontal:
        hlabelm(meas, min(x1, x2) - 4, y1, 11)
    else:
        vlabelm(meas, x1, min(y1, y2) - 4, 11)
    return arrow1, arrow2


def rarrow(x1, y1, x2, y2, meas=None):
    if meas is None:
        meas = convert_measurement()
    try:
        if y1 == y2:  # horizontal
            arrow1, arrow2 = draw_line_and_label(x1, y1, x2, y2, meas, True)
        elif x1 == x2:  # vertical
            arrow1, arrow2 = draw_line_and_label(x1, y1, x2, y2, meas, False)
        else:
            raise ValueError("Coordinates must form a horizontal or vertical line")
    except ValueError as e:
        popup(str(e))
        return
    TK.itemconfig(arrow1, arrow="first")
    TK.itemconfig(arrow2, arrow="first")

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
                [
                    (x, y),
                    (x - ((0.25 / 30) * HEIGHT), y + ((0.5 / 30) * HEIGHT)),
                    (x + ((0.25 / 30) * HEIGHT), y + ((0.5 / 30) * HEIGHT)),
                ],
                fill_color="black",
                line_color="black",
            )
            graph.DrawLine(
                (x, y + ((0.5 / 30) * HEIGHT)),
                (x, y + ((1.5 / 30) * HEIGHT)),
                width=1.5,
            )
        elif dir == "s":
            graph.DrawPolygon(
                [
                    (x, y),
                    (x - ((0.25 / 30) * HEIGHT), y - ((0.5 / 30) * HEIGHT)),
                    (x + ((0.25 / 30) * HEIGHT), y - ((0.5 / 30) * HEIGHT)),
                ],
                fill_color="black",
                line_color="black",
            )
            graph.DrawLine(
                (x, y - ((0.5 / 30) * HEIGHT)),
                (x, y - ((1.5 / 30) * HEIGHT)),
                width=1.5,
            )
        elif dir == "e":
            graph.DrawPolygon(
                [
                    (x, y),
                    (x - ((0.5 / 30) * HEIGHT), y - ((0.25 / 30) * HEIGHT)),
                    (x - ((0.5 / 30) * HEIGHT), y + ((0.25 / 30) * HEIGHT)),
                ],
                fill_color="black",
                line_color="black",
            )
            graph.DrawLine(
                (x - ((0.5 / 30) * HEIGHT), y),
                (x - ((1.5 / 30) * HEIGHT), y),
                width=1.5,
            )
        else:
            graph.DrawPolygon(
                [
                    (x, y),
                    (x + ((0.5 / 30) * HEIGHT), y + ((0.25 / 30) * HEIGHT)),
                    (x + ((0.5 / 30) * HEIGHT), y - ((0.25 / 30) * HEIGHT)),
                ],
                fill_color="black",
                line_color="black",
            )
            graph.DrawLine(
                (x + ((0.5 / 30) * HEIGHT), y),
                (x + ((1.5 / 30) * HEIGHT), y),
                width=1.5,
            )
    except Exception as e:
        logging.exception("caught an error")


def h_arrow(x1, x2, y, meas, measdir="l"):
    """
    Draws a set of horizontal arrows with measurement

        Parameters:
            x1(int or float): 1st horizontal coordinate
            x2(int or float): 2nd horizontal coordinate
            y(int or float): vertical coordinate
            meas(str): measurement to display
            measdir(str): where the measurement will be displayed relative to arrows('l' or 'r')

        Returns:
            None
    """
    try:
        if x1 > x2:
            arrow("w", x1, y)
            arrow("e", x2, y)
            if measdir.lower() == "l":
                hlabelm(meas, x2 - (1/WIDTH), y, (11/HEIGHT) * HEIGHT)
            elif measdir.lower() == "r":
                hlabelm(meas, x1 + (1/WIDTH), y, (11/HEIGHT) * HEIGHT)

        else:
            arrow("e", x1, y)
            arrow("w", x2, y)
            if measdir.lower() == "l":
                hlabelm(meas, x1 - 2.8, y, 11)
            elif measdir.lower() == "r":
                hlabelm(meas, x2 + 2.8, y, 11)
    except Exception as e:
        logerror(e)


def v_arrow(x, y1, y2, meas, measdir="u"):
    """
    Draws a set of vertical arrows with measurement

        Parameters:
        x(int or float): horizontal coordinate
        y1(int or float): 1st vertical coordinate
        y2(int or float): 2nd vertical coordinate
        meas(str): measurement to output
        measdir(str): where the measurement will be relative to arrows('u' or 'd')

        Returns:
            None
    """
    try:
        if y1 > y2:
            arrow("n", x, y1)
            arrow("s", x, y2)
            if measdir.lower() == "u":
                vlabelm(meas, x, y2 - 2.8, 11)
            elif measdir.lower() == "d":
                vlabelm(meas, x, y1 + 2.8, 11)
        else:
            arrow("s", x, y1)
            arrow("n", x, y2)
            if measdir.lower() == "u":
                vlabelm(meas, x, y1 - 2.8, 11)
            elif measdir.lower() == "d":
                vlabelm(meas, x, y2 + 2.8, 11)
    except Exception as e:
        logerror(e)


def v_multi_arrow(x, yo, y1, y2, meas, measdir="u"):
    # pass
    try:
        if yo > y1:
            arrow("n", x, yo)
            arrow("s", x, y1)
            arrow("s", x, y2)
            if measdir.lower() == "u":
                vlabelm(meas, x, y2 - 3.3, 11)
            else:
                vlabelm(meas, x, yo + 3.3, 11)
        else:
            arrow("s", x, yo)
            arrow("n", x, y1)
            arrow("n", x, y2)
            if measdir.lower == "u":
                vlabelm(meas, x, yo - 3.3, 11)
            else:
                vlabelm(meas, x, y2 + 3.3, 11)
    except Exception as e:
        logerror(e)


def pole(x, y):
    try:
        p = graph.draw_circle((x, y), 1, fill_color="white")
        TK.itemconfig(p, activeoutline="red")
    except Exception as e:
        logerror(e)


def ped_stub(pedx, pedy, stub_endx, stub_endy):
    pass


def draw_arc_with_style(graph, start, end, start_angle, end_angle, line_type=None):
    id = sg.Graph.draw_arc(graph, start, end, start_angle, end_angle, style="arc")
    if line_type == "road":
        TK.itemconfig(id, width=3)
        group("road", id)
    elif line_type == "cable":
        TK.itemconfig(id, width=2, dash=(10, 5))
        group("cable", id)
    TK.itemconfig(id, activefill="red")
    return id

def arc(x1, y1, x2, y2, line_type=None):
    """
    Draws an arc from a horizontal plane to vertical
    (x1,y1) - horizontal starting point
    (x2,y2) - vertical starting point

    line_type -default is thin line, accepts 'road' or 'cable'
    """
    try:
        if x2 > x1 and y2 > y1:
            # down and right
            return draw_arc_with_style(graph, (x1 - (x2 - x1), y1), (x2, y2 + (y2 - y1)), -90, 90, line_type)
        elif x2 > x1 and y2 < y1:
            # up and to the right
            return draw_arc_with_style(graph, (x1 - (x2 - x1), y2 - (y1 - y2)), (x2, y1), 90, 270, line_type)
        elif x2 < x1 and y2 > y1:
            # down and to the left
            return draw_arc_with_style(graph, (x2, y1), (x1 + (x1 - x2), y2 + (y2 - y1)), 90, 90, line_type)
        elif x2 < x1 and y2 < y1:
            # up and to the left
            return draw_arc_with_style(graph, (x2, y2 - (y1 - y2)), (x1 + (x1 - x2), y1), -90, 270, line_type)

    except Exception as e:
        logerror(e)




def transformer(x, y):
    try:
        txr = graph.draw_rectangle(
            (x - ((1 / HEIGHT) * HEIGHT), y - ((1 / HEIGHT) * HEIGHT)),
            (x + ((1 / HEIGHT) * HEIGHT), y + ((1 / HEIGHT) * HEIGHT)),
            line_color="black",
        )
        txtri = graph.draw_polygon(
            [
                (x, y - ((1 / HEIGHT) * HEIGHT)),
                (x - ((1 / HEIGHT) * HEIGHT), y + ((1 / HEIGHT) * HEIGHT)),
                (x + ((1 / HEIGHT) * HEIGHT), y + ((1 / HEIGHT) * HEIGHT)),
            ],
            fill_color="black",
        )
        TK.addtag_withtag("transformer", txr)
        TK.addtag_withtag("transformer", txtri)
        add_figure_to_record(record,"transformer", x, y)
    except Exception as e:
        logerror(e)


def vault(x, y, utility=None):
    """
    Draws vault at position x,y

    utility : 'b' gives label 'FTG', otherwise label is 'HW'
    """

    if utility == "b":
        vault_label = "FTG"
    else:
        vault_label = "HW"
    v1 = graph.draw_rectangle(
        (x - 2, y - 1), (x + 2, y + 1), line_color="black", fill_color="White"
    )
    TK.itemconfig(v1, activeoutline="red")

    v2 = graph.draw_text(vault_label, (x, y), font="Arial 7 bold")
    TK.itemconfig(v2, activefill="red")
    # prfloat(v2)
    graph.bring_figure_to_front(v2)

    for x in v1, v2:
        group("vault", x)


def catch_basin(x, y):
    cb = sg.Graph.draw_rectangle(
        graph,
        (x - ((1 / HEIGHT) * HEIGHT), y - ((1 / HEIGHT) * HEIGHT)),
        (x + ((1 / HEIGHT) * HEIGHT), y + ((1 / HEIGHT) * HEIGHT)),
        line_color="black",
        line_width=1.5,
    )
    TK.itemconfig(cb, activeoutline="red")
    group("cb", cb)


def hlabel(msg, x, y, size, bold=True):
    try:
        if msg in ("la", "LA"):
            msg = "LOCATED AREA"
        isbold = " bold" if bold else " normal"
        fontstr = f"Arial {str(size)} {isbold}"
        ht = sg.Graph.draw_text(graph, msg.upper(), (x, y), font=fontstr)
        TK.itemconfig(ht, activefill="red")
        return ht
    except Exception as e:
        logerror(e)


def hlabelm(msg, x, y, size):
    try:
        h = sg.Graph.draw_text(
            graph, msg.lower(), (x, y), font="Arial " + str(size) + " normal"
        )
        return h
    except Exception as e:
        logerror(e)()


def vlabel(msg, x, y, size, bold=True):
    try:
        if msg in ("la", "LA"):
            msg = "LOCATED AREA"
        isbold = " bold" if bold else " normal"
        fontstr = f"Arial {str(size)} {isbold}"
        vt = sg.Graph.draw_text(graph, msg.upper(), (x, y), font=fontstr, angle=90)
        TK.itemconfig(vt, activefill="red")
        return vt
    except Exception as e:
        logerror(e)()


def vlabelm(msg, x, y, size):
    try:
        sg.Graph.draw_text(
            graph, msg.lower(), (x, y), font="Arial " + str(size) + " normal", angle=90
        )
    except Exception as e:
        logerror(e)()


def item_stamp(x, y):
    try:
        im = sg.Graph.draw_image(
            graph, location=(x - 0.75, y - 0.75), data=convert_to_bytes("Drilling.bmp")
        )
        TK.itemconfig(im, activeoutline="red")
    except Exception as e:
        logerror(e)()


def ped(x, y):
    try:
        pedsq = sg.Graph.draw_rectangle(
            graph,
            (x - 1, y - 1),
            (x + 1, y + 1),
            line_color="black",
            fill_color="white",
            line_width=1,
        )
        pedline1 = sg.Graph.draw_line(graph, (x - 1, y - 1), (x + 1, y + 1))
        pedline2 = sg.Graph.draw_line(graph, (x - 1, y + 1), (x + 1, y - 1))
        for item in [pedsq, pedline1, pedline2]:
            group("ped", item)
        TK.tag_bind("ped","<Button-1>",lambda x: popup('Hey now'))

    except Exception as e:
        logerror(e)()


def ped_1arm(pedx, pedy, intercept_x, intercept_y):
    """
    Creates a ped with cable stub

        Parameters:
            pedx : x coord
            pedy: y coord
            intercept_x : x coord of where stub meets connecting cable
            intercept_y :y coords of where stub meets connecting cable

        Returns:
            None
    """
    cable(pedx, pedy, intercept_x, intercept_y)
    ped(pedx, pedy)


def pole_1arm(polex, poley, intercept_x, intercept_y):
    """
    Creates a pole with cable stub

        Parameters:
            polex : x coord
            poley: y coord
            intercept_x : x coord of where stub meets connecting cable
            intercept_y :y coords of where stub meets connecting cable

        Returns:
            None
    """
    cable(polex, poley, intercept_x, intercept_y)
    pole(polex, poley)


def ped_multiarm(x, y, direction, meas1, meas2, distance, third_arm=False):
    """
    minimum distance = 3 (for measurements)
    """
    ped_offset = 0.4
    arm_offset = 1
    arm_offset2 = 2
    if distance < 3:
        return
    ped(x, y)

    if direction.lower() == "n":
        # left arm
        cable(x, y - ped_offset, x - arm_offset, y - arm_offset)
        cable(x - arm_offset, y - arm_offset, x - arm_offset, y - distance)
        # right arm
        cable(x, y - ped_offset, x + arm_offset, y - arm_offset)
        cable(x + arm_offset, y - arm_offset, x + arm_offset, y - distance)
        # if third arm
        if third_arm:
            cable(x, y - ped_offset, x, y - distance)
        # left arm measurement
        h_arrow(x, x - arm_offset, y - arm_offset, meas1, "l")
        # right arm measurement
        h_arrow(x, x + arm_offset, y - arm_offset2, meas2, "r")

    elif direction.lower() == "s":
        pass  # dont need yet

    elif direction.lower() == "w":
        # upper arm
        cable(x - ped_offset, y, x - arm_offset, y - arm_offset)
        cable(x - arm_offset, y - arm_offset, x - distance, y - arm_offset)
        # lower arm
        cable(x - ped_offset, y, x - arm_offset, y + arm_offset)
        h_cable(x - distance, x - arm_offset, y + arm_offset)
        # if third arm
        if third_arm:
            h_cable(x - distance, x - ped_offset, y)
        # upper measurement
        v_arrow(x - arm_offset, y - arm_offset, y, meas1, "8u")
        # lower measurement
        v_arrow(x - arm_offset2, y, y + arm_offset, meas2, "d")


def set_landbase(dir, edge_type="CL"):
    try:
        # draws a landbase
        if dir.lower() == "n":
            road(*NCURB)
            hlabel(f"N{edge_type}", *HNCURBLABEL)
        elif dir.lower() == "ne":
            h_road(9, 28, 23)
            hlabel(f"N{edge_type}", 27, 24, 10)
            v_road(9, 2, 23)
            vlabel(f"E{edge_type}", 10, 3, 10)
        elif dir.lower() == "nw":
            h_road(2, 23, 23)
            hlabel(f"N{edge_type}", 3, 22, 10)
            v_road(23, 2, 23)
            vlabel(f"W{edge_type}", 22, 3, 10)
        elif dir.lower() == "s":
            road(*SCURB)
            hlabel(f"S{edge_type}", *HSCURBLABEL)
        elif dir.lower() == "sw":
            h_road(2, 23, 7)
            hlabel(f"S{edge_type}", 3, 8, 10)
            v_road(23, 7, 28)
            swvcurbx = WIDTH - 7
            swvcurby1 = HEIGHT - 23
            swvcurby2 = HEIGHT - 2
            vlabel(f"W{edge_type}", swvcurbx - 1, swvcurby2 - 1, 10)
        elif dir.lower() == "se":
            sehcurbx1 = 7
            sehcurbx2 = 28
            sehcurby = 7
            sevcurbx = 7
            sevcurby1 = 7
            sevcurby2 = 28
            h_road(sehcurbx1, sehcurbx2, sehcurby)
            hlabel(f"S{edge_type}", sehcurbx2 - 1, sehcurby - 1, 10)
            v_road(sevcurbx, sevcurby1, sevcurby2)
            vlabel(f"E{edge_type}", sevcurbx + 1, sevcurby2 - 1, 10)

        elif dir.lower() == "e":
            road(*ECURB)
            vlabel(f"E{edge_type}", *ECURBLABEL)
        elif dir.lower() == "w":
            road(*WCURB)
            vlabel(f"W{edge_type}", *WCURBLABEL)
        elif dir.lower() == "h":
            road(*HNCURB)
            hlabel(f"N{edge_type}", *HNCURBLABEL)
            road(*HSCURB)
            hlabel(f"S{edge_type}", *HSCURBLABEL)
        landbase = dir.lower()
        return landbase
    except AttributeError:
        logerror(e)()


def set_street_name(street, landbase):
    # enters street name on sketch
    if landbase.lower() == "n":
        hlabel(street, *NSTREET, 16, bold=False)
    elif landbase.lower() == "s":
        hlabel(street, *SSTREET, 16, bold=False)
    elif landbase.lower() == "e":
        vlabel(street, *ESTREET, 16, bold=False)
    elif landbase.lower() == "w":
        vlabel(street, *WSTREET, 16, bold=False)
    elif landbase.lower() == "h":
        hlabel(street, *HSTREET, 16, bold=False)


def get_intersection_name():
    hstreet = get_input("Enter horizontal street name")
    vstreet = get_input("Enter vertical street name")
    return hstreet, vstreet


def set_intersection_name(hstreet, vstreet, landbase):
    if landbase.lower() == "ne":
        set_street_name(hstreet, "n")
        set_street_name(vstreet, "e")
    elif landbase.lower() == "nw":
        set_street_name(hstreet, "n")
        set_street_name(vstreet, "w")
    elif landbase.lower() == "se":
        set_street_name(hstreet, "s")
        set_street_name(vstreet, "e")
    elif landbase.lower() == "sw":
        set_street_name(hstreet, "s")
        set_street_name(vstreet, "w")


def get_digbox():
    pass


def set_digbox():
    pass


def road(x1, y1, x2, y2):
    """
    Draws a road

    params:
        x1, y1: start point
        x2, y2: end point
    """
    try:
        r = graph.DrawLine((x1, y1), (x2, y2), width="3")
        graph.TKCanvas.itemconfig(r, activefill="red")
        TK.itemconfig(r, capstyle="round")
        TK.addtag_withtag("road", r)
    except Exception as e:
        logerror(e)()


def road_corner(start, arc_start, arc_end, end):
    """
    Draws a road corner

    params:
        start: start point (x, y)
        arc_start: arc start point (x, y)
        arc_end: arc end point (x, y)
        end: end point (x, y)
    """
    road(*start, *arc_start)
    arc(*arc_start, *arc_end, "road")
    road(*arc_end, *end)


def h_road(x1, x2, y):
    """
    Draws a horizontal road

    params:
        x1, x2: start and end points
        y: y coordinate

    """
    road(x1, y, x2, y)


def v_road(x, y1, y2):
    road(x, y1, x, y2)


def offset_line(x1, y1, x2, y2):
    try:
        offset = graph.draw_line((x1, y1), (x2, y2), width="1")
        graph.TKCanvas.itemconfig(offset, dash=(2, 7))
        TK.itemconfig(offset, capstyle="round")
        TK.itemconfig(offset, activefill="red")
        TK.addtag_withtag("oline", offset)
    except Exception as e:
        logerror(e)()


def cable_poly(*points):
    try:
        cablepoly = sg.Graph.draw_lines(graph, points, width="3")
        TK.itemconfig(cablepoly, dash=(20, 10))
        TK.itemconfig(cablepoly, activefill="red")
        TK.itemconfig(cablepoly, capstyle="round")
    except Exception as e:
        logerror(e)()


def cable(x1, y1, x2, y2, label=""):
    try:
        cable = sg.Graph.draw_line(graph, (x1, y1), (x2, y2), width="3")
        TK.itemconfig(cable, dash=(20, 10))
        TK.itemconfig(cable, activefill="red")
        TK.itemconfig(cable, capstyle="round")
        if label:
            # check for horizontal or vertical lines
            if x1 == x2:
                # vertical cable
                if (abs(y1 - y2) < 4) or (abs(y2 - y1) < 4):
                    gap = 2
                else:
                    gap = 5
                for y in range(round(y1), round(y2), gap):
                    # white box
                    if len(label) <= 2:
                        s = (((0.25 / 30) * HEIGHT) / 30) * HEIGHT
                    else:
                        s = 0.6
                    tbox = sg.Graph.draw_rectangle(
                        graph,
                        (x1 - s, y - s),
                        (x1 + s, y + s),
                        fill_color="white",
                        line_color="white",
                    )
                    TK.addtag_withtag("cable", "tbox")
                    tlab = sg.Graph.draw_text(
                        graph, label.upper(), (x1, y), font="Arial 7 normal"
                    )
                    TK.addtag_withtag("cable", tlab)

            elif y1 == y2:
                # horizontal cable
                # check for cable length to determine spacing
                if (abs(x1 - x2) < 4) or (abs(x2 - x1) < 4):
                    gap = 2
                else:
                    gap = 5
                for x in range(round(x1), round(x2), gap):
                    # white box
                    # check for text size
                    if len(label) <= 2:
                        s = (((0.25 / 30) * HEIGHT) / 30) * HEIGHT
                    else:
                        s = 0.6
                    tbox = sg.Graph.draw_rectangle(
                        graph,
                        (x - s, y1 - s),
                        (x + s, y1 + s),
                        fill_color="white",
                        line_color="white",
                    )
                    TK.addtag_withtag("cable", tbox)
                    # text
                    tlab = sg.Graph.draw_text(
                        graph, label.upper(), (x, y1), font="Arial 7 normal"
                    )
                    TK.addtag_withtag("cable", tlab)
    except Exception as e:
        logerror(e)()


def h_cable(x1, x2, y, label=""):
    cable(x1, y, x2, y)
    if label:
        # check for cable length to determine spacing
        if (abs(x1 - x2) < 4) or (abs(x2 - x1) < 4):
            gap = 2
        else:
            gap = 6
        for x in range(round(x1), round(x2), gap):
            # white box
            # check for text size
            if len(label) <= 2:
                s = (((0.25 / 30) * HEIGHT) / 30) * HEIGHT
            else:
                s = 0.6
            sg.Graph.draw_rectangle(
                graph,
                (x - s, y - s),
                (x + s, y + s),
                fill_color="white",
                line_color="white",
            )
            # text
            hlabel(label, x, y, 7)


def v_cable(x, y1, y2, label=""):
    cable(x, y1, x, y2)
    if label:
        if (abs(y1 - y2) < 4) or (abs(y2 - y1) < 4):
            gap = 2
        else:
            gap = 6
        for y in range(round(y1), round(y2), gap):
            # white box
            if len(label) <= 2:
                s = (((0.25 / 30) * HEIGHT) / 30) * HEIGHT
            else:
                s = 0.6
            sg.Graph.draw_rectangle(
                graph,
                (x - s, y - s),
                (x + s, y + s),
                fill_color="white",
                line_color="white",
            )
            vlabel(label, x, y, 7)


def line(x1, y1, x2, y2):
    try:
        l = sg.Graph.draw_line(graph, (x1, y1), (x2, y2))
        TK.itemconfig(l, activefill="red")
        TK.itemconfig(l, capstyle="round")
    except Exception as e:
        logerror(e)()


def h_line(x1, x2, y):
    line(x1, y, x2, y)


def v_line(x, y1, y2):
    line(x, y1, x, y2)


def get_figure_type(tag_or_id: int):
    """
    Returns the type of figure (rectangle, oval, line, etc.)

    :param tag_or_id: The tag or ID of the figure
    :return: The type of figure

    """
    fig_type = TK.type(tag_or_id)
    return fig_type


def get_figure_coords(tag_or_id):
    """
    Returns the coordinates of the figure

    :param tag_or_id: The tag or ID of the figure
    :return: The coordinates of the figure

    """

    fig_coords = TK.coords(tag_or_id)
    return fig_coords


def clone_item(tag_or_ID):
    config = TK.itemconfig(tag_or_ID)
    clone = {key: config[key][-1] for key in config.keys()}
    return clone


def paste_figure(fig_type, coords, clone):
    try:
        if clone is not None:
            new_coords = [coord + 10 for coord in coords]
            if fig_type == "rectangle":
                TK.create_rectangle(new_coords, **clone)
            elif fig_type == "oval":
                TK.create_oval(new_coords, **clone)
            elif fig_type == "line":
                TK.create_line(new_coords, **clone)
            elif fig_type == "text":
                TK.create_text(new_coords, **clone)
            elif fig_type == "image":
                TK.create_image(new_coords, **clone)
    except NameError:
        sg.popup("Nothing to paste")


def digbox(x1, y1, x2, y2):
    try:
        db = graph.draw_rectangle(
            (x1, y1), (x2, y2), fill_color="gainsboro", line_color="black"
        )
        graph.TKCanvas.itemconfig(db, stipple="gray25", activeoutline="red")
        sg.Graph.send_figure_to_back(graph, db)
        TK.addtag_withtag("digbox", db)
    except Exception as e:
        logerror(e)()


def building(x1, y1, x2, y2):
    try:
        b = sg.Graph.draw_rectangle(
            graph,
            (x1, y1),
            (x2, y2),
            fill_color="white",
            line_color="black",
            line_width=1,
        )
        TK.itemconfig(b, activeoutline="red")
    except Exception as e:
        logerror(e)


def located_area(x, y):
    try:
        sg.Graph.draw_text(graph, "LOCATED AREA", (x, y), font="Arial 11 bold")
    except Exception as e:
        logerror(e)()


def house(x, y, size, num):
    # draws a house of size (size) at (x,y)
    # parameters: x, y, size, num
    # size: s, m, l
    # num: house number

    if size == "m":
        house_size = 8
    elif size == "l":
        house_size = 10
    elif size == "s":
        house_size = 6

    bldng = sg.Graph.draw_rectangle(
        graph,
        (x, y),
        (x + house_size, y + house_size),
        line_color="black",
        fill_color="white",
    )
    hnumber = hlabel(num, x + (house_size / 2), y + (house_size / 2), 16)
    nbl = hlabel("NBL", x + (house_size / 2), y - 1, 10)
    sbl = hlabel("SBL", x + (house_size / 2), y + (house_size + 1), 10)
    wbl = vlabel("WBL", x - 1, y + (house_size / 2), 10)
    ebl = vlabel("EBL", x + (house_size + 1), y + (house_size / 2), 10)
    # group all items
    for _ in (bldng, hnumber, nbl, sbl, wbl, ebl):
        group(f"house{size}", _)


def centre_pole():
    pole(WIDTH // 2, HEIGHT // 2)


def centre_ped():
    ped(WIDTH // 2, HEIGHT // 2)


def centre_tx():
    transformer(WIDTH // 2, HEIGHT // 2)


def centre_stamp():
    item_stamp(WIDTH // 2, HEIGHT // 2)


def get_point1():
    x, y = values["graph"]
    return x, y


def get_point2():
    a, b = values["graph"]
    return a, b


def get_point3():
    c, d = values["graph"]
    return c, d


def get_point():
    x, y = values["graph"]
    return x, y


def draw_point1(x, y, color="red"):
    try:
        point1 = sg.Graph.draw_point(
            graph, (x, y), size=((0.5 / 30) * HEIGHT), color=color
        )
        return point1
    except Exception as e:
        logerror(e)()


def draw_point2(x, y, color="blue"):
    try:
        point2 = sg.Graph.draw_point(
            graph, (x, y), size=((0.5 / 30) * HEIGHT), color=color
        )
        return point2
    except Exception as e:
        logerror(e)()


def draw_point3(x, y, color="green"):
    try:
        point3 = sg.Graph.draw_point(
            graph, (x, y), size=((0.5 / 30) * HEIGHT), color=color
        )
        return point3
    except Exception as e:
        logerror(e)()


def draw_point4(x, y, color="orange"):
    try:
        point4 = sg.Graph.draw_point(
            graph, (x, y), size=((0.5 / 30) * HEIGHT), color=color
        )
        return point4
    except Exception as e:
        logerror(e)()


def cleanup_2point():
    x = y = a = b = None
    current_mode = "select"
    graph.delete_figure(point1)
    graph.delete_figure(point2)


def edit_text():
    try:
        string = popup_get_text("Enter new text")
        TK.itemconfig("current", text=string)
    except Exception as e:
        popup("Not a text object")
        pass


def get_input(prompt):
    return popup_get_text(prompt)


def draw_cursor(input_mode):
    if input_mode != "keyboard":
        return
    c1 = sg.Graph.draw_line(graph, (15, 14), (15, 16), color="blue")
    c2 = sg.Graph.draw_line(graph, (14, 15), (16, 15), color="blue")
    cursorid = (c1, c2)
    for _ in cursorid:
        TK.addtag_withtag("cursor", _)
    return cursorid


def update_cursor_position(cursor):
    refline = TK.coords(cursor[0])
    cursorx = refline[0] / 20
    cursory = (refline[1] + refline[3]) / 2 / 20
    # Print(cursorx, cursory)
    return [cursorx, cursory]


def hide_cursor(cursorid):
    TK.itemconfig("cursor", state="hidden")


def read_from_template(file):
    """
    Reads a template from a given text file and loads a base sketch
    """

    if file is not None:
        try:
            with open(file) as f:
                flist = f.readlines()
                lb_strlist = flist[0].split()
                dir = lb_strlist[0]
                edge_type = lb_strlist[1].strip()
                landbase = set_landbase(dir, edge_type)
                if dir in ["ne", "nw", "se", "sw"]:
                    set_intersection_name(flist[1], flist[2], landbase)
                else:
                    set_street_name(flist[1], landbase)

        except IndexError:
            pass

        except Exception as e:
            logging.exception("error")
            popup("There was an error in template file")


def save_sketch_template(file=""):
    if file is not None:
        filename = file
    else:
        filename = popup_get_file("Save template as", save_as=True)
    typelist = []
    coordslist = []
    clonelist = []
    list_of_all_figures = []
    for id in TK.find_all():
        typelist.append(get_figure_type(id))
        coordslist.append(get_figure_coords(id))
        clonelist.append(clone_item(id))
    list_of_all_figures.extend([typelist, coordslist, clonelist])
    if filename is not None:
        with open(filename + ".pkl", "wb") as pk:
            pickle.dump(list_of_all_figures, pk)
        with open(filename + ".json", "w") as js:
            json.dump(list_of_all_figures, js)


def load_sketch_template() -> None:
    filename: str = popup_get_file("Choose template file...")
    with open(f"{filename}", "rb") as pk:
        list_of_all_figures: list = pickle.load(pk)
    typelist = list_of_all_figures[0]
    coordslist = list_of_all_figures[1]
    clonelist = list_of_all_figures[2]
    for x, y, z in zip(typelist, coordslist, clonelist):
        if x == "rectangle":
            TK.create_rectangle(y, **z)
        elif x == "oval":
            TK.create_oval(y, **z)
        elif x == "line":
            TK.create_line(y, **z)
        elif x == "text":
            TK.create_text(y, **z)
        elif x == "image":
            pass
        elif x == "polygon":
            TK.create_polygon(y, **z)
        elif x == "arc":
            TK.create_arc(y, **z)


def parse_bl_string(bl_string: str) -> dict:
    """
    Parses a string representing a drawing template and returns a dictionary

    The input string should have the following format:
    "street_name,landbase,choice,house1,house2,measurement"

    The function returns a dictionary with the following keys:
    - street_name: a string representing the name of the street
    - landbase: a string representing the direction of the landbase (n, e, s, w)
    - choice: a string representing the choice (o, i, se, nw)
    - house1: a string representing the first house number
    - house2: a string representing the second house number
    - measurement: a string representing the measurement (a positive integer)

    If the input string does not have the expected format, the function returns None.
    """

    bl_list = bl_string.split(",")
    if len(bl_list) < 6:
        return None
    else:
        # check that landbase is one of n,e,s,w
        if bl_list[1].strip().lower() not in ["n", "e", "s", "w"]:
            return None
        # check that choice is one of o,i,se,nw
        if bl_list[2].strip().lower() not in ["o", "i", "se", "nw"]:
            return None
        # check that measurement is a positive integer
        if not bl_list[5].strip().isdigit():
            return None
        bl_dict = {
            "street_name": bl_list[0].strip().upper(),
            "landbase": bl_list[1].strip(),
            "choice": bl_list[2].strip(),
            "house1": bl_list[3].strip(),
            "house2": bl_list[4].strip(),
            "measurement": bl_list[5].strip(),
        }
        return bl_dict


def render_template(bl_string: str = None):
    """
    Renders a drawing template

    Steps:
    parse bl string -> dictionary
    from dictionary -> get street name, landbase, choice, house1, house2, measurement
    bl_to_bl(dir=landbase,house1,house2,street_name)
    render_cable(landbase,choice)
    render_measurement(landbase,measurement)

    """
    if not bl_string:
        bl_string = sg.popup_get_text(
            "Enter BL string - Separate fields with commas (street name, landbase, choice, house1, house2, measurement))"
        )
    try:
        bl_dict = parse_bl_string(bl_string)
    except AttributeError:
        popup("Invalid BL string")
        return
    if bl_dict is None:
        # dont want to do anything if the bl string is invalid so just return
        popup("Invalid BL string")
        return
    else:
        bl_to_bl(
            bl_dict["landbase"],
            bl_dict["house1"],
            bl_dict["house2"],
            bl_dict["street_name"],
        )
        c = get_cable(bl_dict["landbase"], bl_dict["choice"])
        cable(*c, "TMX")
        m = convert_measurement(bl_dict["measurement"])
        ac = get_arrow_coords(bl_dict["landbase"])
        rarrow(*ac, m)
        savefile = f'{bl_dict["street_name"]} {bl_dict["house1"]} to {bl_dict["house2"]} tmx.png'
        path = pathlib.Path(r"C:\Users\Cr\Documents")
        save_choice = sg.popup_yes_no(f"Save as {savefile}?")
        if save_choice == "Yes":
            save_element_as_file(graph, path / f"{savefile}")
            save_sketch_template(savefile)
            popup(f"Saved as {savefile}")

        # render_measurement(landbase,bl_dict["mmeasurement)


def get_cable(landbase: str, choice: str) -> tuple:
    """
    Gets the coordinates for a cable according to the landbase and choice parameters

    Returns a tuple of coordinates (x1, y1, x2, y2)

    Parameters:
    - landbase: a string representing the direction of the landbase (n, e, s, w)
    - choice: a string representing the choice (o, i, se, nw)
    """

    if landbase == "n":
        y1 = NCURB[1] - 2
        y2 = NCURB[1] - 2
        if choice == "o":
            # wbl to ebl
            x1 = NBLHOUSE1[0]
            x2 = NBLHOUSE2[0] + 8
        elif choice == "i":
            # ebl to wbl
            x1 = NBLHOUSE1[0] + 8
            x2 = NBLHOUSE2[0]
        elif choice == "se":
            # ebl to ebl
            x1 = NBLHOUSE1[0] + 8
            x2 = NBLHOUSE2[0] + 8
        elif choice == "nw":
            # wbl to wbl
            x1 = NBLHOUSE1[0]
            x2 = NBLHOUSE2[0]

    elif landbase == "s":
        y1 = SCURB[1] + 2
        y2 = SCURB[1] + 2
        if choice == "o":
            # wbl to ebl
            x1 = SBLHOUSE1[0]
            x2 = SBLHOUSE2[0] + 8
        elif choice == "i":
            # ebl to wbl
            x1 = SBLHOUSE1[0] + 8
            x2 = SBLHOUSE2[0]
        elif choice == "se":
            # ebl to ebl
            x1 = SBLHOUSE1[0] + 8
            x2 = SBLHOUSE2[0] + 8
        elif choice == "nw":
            # wbl to wbl
            x1 = SBLHOUSE1[0]
            x2 = SBLHOUSE2[0]

    elif landbase == "e":
        x1 = ECURB[0] + 2
        x2 = ECURB[0] + 2
        if choice == "o":
            # nbl to sbl
            y1 = EBLHOUSE1[1]
            y2 = EBLHOUSE2[1] + 8
        elif choice == "i":
            # sbl to nbl
            y1 = EBLHOUSE1[1] + 8
            y2 = EBLHOUSE2[1]
        elif choice == "se":
            # sbl to sbl
            y1 = EBLHOUSE1[1] + 8
            y2 = EBLHOUSE2[1] + 8
        elif choice == "nw":
            # nbl to nbl
            y1 = EBLHOUSE1[1]
            y2 = EBLHOUSE2[1]

    elif landbase == "w":
        x1 = WCURB[0] - 2
        x2 = WCURB[0] - 2
        if choice == "o":
            # nbl to sbl
            y1 = WBLHOUSE1[1]
            y2 = WBLHOUSE2[1] + 8
        elif choice == "i":
            # sbl to nbl
            y1 = WBLHOUSE1[1] + 8
            y2 = WBLHOUSE2[1]
        elif choice == "se":
            # sbl to sbl
            y1 = WBLHOUSE1[1] + 8
            y2 = WBLHOUSE2[1] + 8
        elif choice == "nw":
            # nbl to nbl
            y1 = WBLHOUSE1[1]
            y2 = WBLHOUSE2[1]

    return x1, y1, x2, y2


def get_arrow_coords(landbase: str) -> list:
    """
    Gets the coordinates of the offset arrows according to the landbase as a list [x1, y1, x2, y2]

    Parameters:
    - landbase: a string representing the direction of the landbase (n, e, s, w)

    Implementation:
    - For a n landbase, the arrows are placed at (37,38) and (37,40)
    - For a s landbase, the arrows are placed at (37,20) and (37,22)
    - For a e landbase, the arrows are placed at (23,28) and (25,28)
    - For a w landbase, the arrows are placed at (44,28) and (46,28)

    """

    if landbase == "n":
        return [37, 38, 37, 40]
    elif landbase == "s":
        return [37, 20, 37, 22]
    elif landbase == "e":
        return [23, 28, 25, 28]
    elif landbase == "w":
        return [44, 28, 46, 28]


# callback routines


def short_gas():
    try:
        dir = popup_get_text("N, S, E, W?")
        hnum = popup_get_text("House number?")
        street = popup_get_text("Street name?")
        landbase = set_landbase(dir)
        set_street_name(street, landbase)
        if dir.lower() == "n":
            digbox(7, 1, 23, 27)
            house(11, 4, "l", hnum)
        elif dir.lower() == "s":
            digbox(7, 3, 23, 29)
            house(11, 18, "l", hnum)
            hlabel("LOCATED AREA", 15, 14, 12)
        elif dir.lower() == "e":
            digbox(3, 7, 29, 23)
            house(18, 11, "l", hnum)
        elif dir.lower() == "w":
            digbox(1, 7, 27, 23)
            house(4, 11, "l", hnum)
        else:
            easy_print(logging.exception("err"))
            pass

    except Exception as e:
        easy_print(logging.exception("err"))
        pass


def long_gas():
    try:
        dir = popup_get_text("N, S, E, W?")
        hnum = popup_get_text("House number?")
        street = popup_get_text("Street name?")
        if dir.lower() == "n":
            h_road(2, 28, 16)
            h_road(2, 28, 22)
            hlabel("NRE", 27, 15, 11)
            hlabel("SRE", 27, 21, 11)
            digbox(4, 0, 26, 29)
            house(12, 3, "m", hnum)
            hlabel(street, 15, 19, 20)
            pass
        elif dir.lower() == "s":
            h_road(2, 28, 8)
            h_road(2, 28, 14)
            hlabel("NRE", 27, 7, 11)
            hlabel("SRE", 27, 15, 11)
            digbox(4, 1, 26, 30)
            house(11, 20, "m", hnum)
            hlabel(street, 15, 11, 20)
        elif dir.lower() == "e":
            pass
        elif dir.lower() == "w":
            v_road(16, 2, 28)
            v_road(22, 2, 28)
            vlabel("WCL", 15, 3, 11)
            vlabel("ECL", 23, 3, 11)
            digbox(0, 4, 29, 26)
            house(2, 11, "m", hnum)
            vlabel(street, 19, 15, 20)
        else:
            easy_print(logging.exception("err"))
    except Exception as e:
        easy_print(logging.exception("err"))
        pass


def radius_sketch() -> None:
    feature: list[str] = ["ped", "pole", "tree", "transformer", "waterbox"]
    user_type = popup_get_text("Object type ?(ped,pole,tree,transformer,waterbox")
    try:
        radius = int(popup_get_text("Radius in m?(int)"))
    except ValueError:
        return
    if user_type not in feature:
        popup_get_text("Not a valid entry")
        return
    radiusdict = {
        "ped": centre_ped,
        "pole": centre_pole,
        "tree": centre_stamp,
        "transformer": centre_tx,
        "waterbox": centre_stamp,
    }
    radiusdict[user_type]()
    if radius < 3:
        digbox(13, 13, 17, 17)
    else:
        digbox(10, 10, 20, 20)


def st_to_st():
    dir = popup_get_text("Landbase? (N,S,E,W)")
    street1 = popup_get_text("Street 1 (W or N)")
    street2 = popup_get_text("Street 2 (mid)")
    street3 = popup_get_text("Street 3 (S or E)")

    if dir.lower() is None:
        return

    actions = {
        "n": [
            (h_road, (3, 27, 20)),
            (v_road, (3, 10, 20)),
            (v_road, (27, 10, 20)),
            (hlabel, ("NCL", 25, 19, 11)),
            (vlabel, ("ECL", 4, 11, 11)),
            (vlabel, ("WCL", 26, 11, 11)),
            (vlabel, (street1, 1, 15, 20)),
            (hlabel, (street2, 15, 23, 20)),
            (vlabel, (street3, 29, 15, 20))
        ],
        "s": [
            (h_road, (3, 27, 10)),
            (v_road, (3, 10, 20)),
            (v_road, (27, 10, 20)),
            (hlabel, ("SCL", 26, 9, 11)),
            (vlabel, ("ECL", 27, 21, 11)),
            (vlabel, ("WCL", 3, 21, 11)),
            (vlabel, (street1, 1, 15, 20)),
            (hlabel, (street2, 15, 7, 20)),
            (vlabel, (street3, 29, 15, 20))
        ],
        "w": [
            (v_road, (20, 3, 27)),
            (h_road, (10, 20, 3)),
            (h_road, (10, 20, 27)),
            (hlabel, ("SCL", 11, 4, 11)),
            (vlabel, ("WCL", 21, 15, 11)),
            (hlabel, ("NCL", 11, 26, 11)),
            (hlabel, (street1, 11, 1, 20)),
            (vlabel, (street2, 26, 15, 20)),
            (hlabel, (street3, 11, 29, 20))
        ],
        "e": [
            (v_road, (10, 3, 27)),
            (h_road, (10, 20, 3)),
            (h_road, (10, 20, 27)),
            (hlabel, ("SCL", 19, 4, 11)),
            (hlabel, ("NCL", 19, 26, 11)),
            (vlabel, ("ECL", 9, 14, 11)),
            (hlabel, (street1, 21, 2, 20)),
            (vlabel, (street2, 5, 14, 20)),
            (hlabel, (street3, 21, 28, 20))
        ]
    }

    for action, params in actions.get(dir.lower(), []):
        action(*params)


def bl_to_bl(dir=None, hnum1=None, hnum2=None, street=None):
    if not dir:
        dir = get_input("N, S, E or W?")
    if not hnum1:
        hnum1 = get_input("House number 1?")
    if dir in ["nw", "ne", "se", "sw"]:
        hstreet, vstreet = get_intersection_name()
        set_intersection_name(hstreet, vstreet, dir)
    else:
        if not hnum2:
            hnum2 = get_input("House number 2?")
        if not street:
            street = get_input("Street name?")
        set_street_name(street, set_landbase(dir))

    houses = {
        "n": [(*NBLHOUSE1, hnum1), (*NBLHOUSE2, hnum2)],
        "nw": [(*NWBLHOUSE, hnum1)],
        "ne": [(*NEBLHOUSE, hnum1)],
        "s": [(*SBLHOUSE1, hnum1), (*SBLHOUSE2, hnum2)],
        "sw": [(*SWBLHOUSE, hnum1)],
        "e": [(*EBLHOUSE1, hnum1), (*EBLHOUSE2, hnum2)],
        "w": [(*WBLHOUSE1, hnum1), (*WBLHOUSE2, hnum2)]
    }

    for params in houses.get(dir.lower(), []):
        house(*params)


def get_parser_string(input):
    return input
    
            


# barebones

menu_def = [
    ["File", ["Save", "Save template as...", "Load template", "Exit"]],
    ["Size", ["24", "30"]],
    ["Input", ["Mouse/Keyboard", "Keyboard"]],
]

tab2layout = [
    [
        sg.Text("Curb: "),
        sg.DropDown(("N", "S", "E", "W"), key="curbddl"),
        sg.Radio("CL", "roadtype", key="cl"),
        sg.Radio("RE", "roadtype", k="re"),
    ],
    [
        sg.Button("Change street", key="tab1getstreet"),
        sg.T(k="tab1street"),
    ],
    [sg.B("Intersecting street:", k="tab2getstreet"), sg.I(k="tab1intersection")],
    [sg.Submit(k="sketchbuild_submit")],
]
tab1layout: list = [[]]
lcol = [
    [sg.Sizer(0, 0)],
    [notify_inputmode],
    [sg.Button("Select", button_color=("yellow", "black"))],
    [sg.Button("Line")],
    [sg.Button("Cable")],
    [sg.Button("Road")],
    [sg.Button("Small Text")],
    [sg.Button("Large Text")],
    [sg.Button("H.Arrow")],
    [sg.Button("V.Arrow")],
]

canvasmenu = ["", ["Snap to Grid", "Render Template"]]

col = [
    [notify, sg.VerticalSeparator(), notify2, sg.VerticalSeparator(), notify3],
    [
        sg.Graph(
            canvas_size=(700, 600),
            graph_bottom_left=(0, HEIGHT),
            graph_top_right=(WIDTH, 0),
            background_color="white",
            right_click_menu=canvasmenu,
            key="graph",
            enable_events=True,
            motion_events=True,
            drag_submits=True,
        ),
    ],
    [
        sg.Button("Short Gas", enable_events=True),
        sg.Button("Long Gas", enable_events=True),
        sg.Button("Radius", enable_events=True),
        sg.Button("St to St", enable_events=True),
        sg.Button("BL to BL", enable_events=True),
        sg.B("Read template", enable_events=True, k="read_file",auto_size_button="true"),
        sg.B("Form"),
    ],
    [sg.StatusBar("",k="stb_notify", relief="ridge", expand_x=True,background_color = "yellow",text_color="black",s=2)],
]

rcol = [
    [sg.T("0, 0", k="ccord")],
    [sg.T("", k="startpoint")],
    [sg.T("", k="endpoint")],
    [sg.T("", k="enclosing_rect_coords")],
    [sg.T("", k="selected_id")],
    [sg.Text("Object features")],
    [
        sg.Text(
            "Object type:",
        ),
        sg.Input(k="lblobject_type", readonly=True),
    ],
    [sg.Text("Coords:"), sg.Input(k="objcoords", readonly=True, text_color='black')],
    [sg.Text("Tag:"), sg.I(k="tag", readonly=True, text_color='black')],
    [sg.T("ID"), sg.I(k="ID", readonly=True, text_color='black')],
    [sg.T("*PARSER")],
    [sg.Input(do_not_clear=False, k="parser_input"), sg.Submit(k="parser_submit")],
]


layout = [
    [
        sg.Menu(menu_def),
        sg.Column(
            lcol,
            justification="left",
            element_justification="left",
            vertical_alignment="t",
        ),
        sg.Column(
            col, justification="left", element_justification="left", expand_x=True
        ),
        sg.Column(rcol, justification="left", element_justification="left"),
    ]
]


def make_form_window() -> sg.Window:
    landbases: list[str] = [
        "NORTH",
        "SOUTH",
        "EAST",
        "WEST",
        "NORTHEAST",
        "NORTHWEST",
        "SOUTHEAST",
        "SOUTHWEST",
        "HORIZONTAL",
        "VERTICAL",
    ]

    layout2:list = [
        [sg.Text("Landbase:"), sg.Combo(landbases, k="landbase")],
        [sg.Text("Primary Street (Horizontal)"), sg.Input(k="street")],
        [sg.Text("Secondary Street (Vertical)"), sg.I(k="street2")],
        [sg.Submit(k="form_submit")],
    ]

    return sg.Window("Sketch Builder", layout2,modal=True,finalize=True)


window: sg.Window = sg.Window(
    "EZ Draw",
    layout,
    finalize=True,
    auto_size_buttons=False,
    return_keyboard_events=True,
    use_default_focus=True,
    use_ttk_buttons=False,
    resizable=True,
    margins=(0, 0),
    border_depth=0,
    element_padding=(0),
    location=((0, 0)),
    use_custom_titlebar=False,
    titlebar_icon = r"./resources/TICO.PNG"
)

graph:dict = window.key_dict["graph"]


window.bind("<Control-n>", "NEW FILE")
window.bind("<Control-w>", "QUIT")
window.bind("<Control-a>", "SELECT_ALL")
sg.Graph.bind(graph,"<Enter>", "GRAPH_ENTER")
graph.bind("<Leave>", "GRAPH_LEAVE")

TK: tkinter.Canvas = graph.TKCanvas
# DRAW HERE
# SETUP

# dictionary for key input to draw function mapping

buttoniomulti = {
    "a": arc,
    "b": building,
    "B": house,
    "c": cable,
    "C": arc,
    "d": digbox,
    "h": h_arrow,
    "l": line,
    "n": cable,
    "o": offset_line,
    "r": road,
    "R": arc,
    "v": v_arrow,
    "!": ped_1arm,
    "@": pole_1arm,
}

buttoniosingle = {
    "1": ped,
    "2": pole,
    "3": item_stamp,
    "4": transformer,
    "5": vault,
    "6": catch_basin,
}


class DrawManager:
    pass


class PolyLine:
    pass


class Grid:
    def __init__(self, snap, visible):
        self.snap = snap
        self.visible = visible

    @property
    def snap(self):
        return self.snap

    @snap.setter
    def snap(self, state):
        self.snap = state

    @property
    def visible(self):
        return self.visible

    @visible.setter
    def visible(self, value):
        self.visible = value

    def show(self):
        pass

    def hide(self):
        pass

def handle_mode(mode, new_mode, color, message):
    if input_mode == "keyboard":
        x, y = update_cursor_position(cursor)
    else:
        x, y = get_point1()
    start_point = (x, y)
    current_mode = new_mode
    point1 = draw_point1(x, y, color)
    notify.update(message)

mode_handlers = {
    "building": ("building2", "black", "Click lower right corner of building"),
    "road": ("road2", "purple", "Click second point of curb"),
    "road arc": ("road arc 2", "purple", "Click vertical section of road arc"),
    "line": ("line2", "blue", "Click second point of line"),
    "corner": ("corner2", "purple", "Click horizontal section of arc"),
    "arc": ("arc2", "purple", "Click second point of arc"),
}
# FOR LATER - code to handle mode changes
# insert the code below in the main loop
#
#if current_mode in mode_handlers:
 #   handle_mode(*mode_handlers[current_mode])

# THESE GLOBALS ARE AN EMBARRASSMENT

mode = {0: "select", 1: "get points", 2: "draw"}
current_mode = "select"
x = y = a = b = 0
isGrid = False
gridSnap = True
graph.bind("<B1-Motion>", "drag")
graph.set_cursor("crosshair")
# graph.bind("<Motion>", "motion")
# graph.bind("<KeyPress-g>",'gridon')
# graph.bind("<KeyRelease-g>",'gridoff')
selected = []
spoints = []
enclosing = []
dragging = False
start_point = end_point = prior_rect = (0, 0)
etext = 0
entered_text = ""
collecting = False
cpoints = []
cnodes = []
input_mode = "mouse"
cursorx = 0
cursory = 0
cursor = (0, 0)
hashline = None
hashrect = None
outline = None
newmouse = None
in_graph = False
record = []

# cable_poly((14,0),(14,6),(20,6))

# testing unpacking this is neat

# small loop - lol not anymore

while True:
    event, values = window.read()
    try:
        window["ccord"].update(f'Coordinates:{values["graph"]}  Dragging:{dragging}')
        window["startpoint"].update(f'Start point {start_point}')
        window["endpoint"].update(f'End point {end_point}')
        window["enclosing_rect_coords"].update(f'Enclosed rectangle coordinates {enclosing}')
        window["selected_id"].update(f'Selected items ID {selected}')
        notify2.update(f"Event: {event} ")
        notify3.update(f"Mode: {current_mode} ")
    except:
        pass
    
    if event == sg.WIN_CLOSED:
        break
    if event == "parser_submit":
        p_in = get_parser_string(values["parser_input"])
        print(p_in)
        tokens = p_in.split(" ")
        print(tokens)
        graph.set_focus()
        if tokens[0] == "line":
            road(int(tokens[1]),int(tokens[2]),int(tokens[3]),int(tokens[4]))
            
    if event == "Form":
        window2 = make_form_window()
        event,values = window2.read()

    if event == 'form_submit':
        popup(values['landbase'])
        window2.close()
              
     
        
    if event.endswith("ENTER"):
        in_graph = True

    if event.endswith("LEAVE"):
        in_graph = False
        graph.delete_figure(h_cursor_line)
        graph.delete_figure(v_cursor_line)

    if event.endswith("QUIT"):
        app_done = sg.popup_yes_no("Close application?")
        if app_done == "Yes":
            window.close()

    if event.endswith("SELECT_ALL"):
        [selected.append(x) for x in TK.find_all()]
        
    if event == "Save":
        _savefile = popup_get_text("Save file name?")
        # small = sg.popup_yes_no("Save as smaller image?")
        try:
            _savefile = _savefile.upper()
            graph.delete_figure(h_cursor_line)
            graph.delete_figure(v_cursor_line)
            save_element_as_file(graph, f"C:\\Users\\Cr\\Documents\\{_savefile}.png")
            # makes a smaller image
            """
            if small == "Yes":
                skt = f"C:\\Users\\Cr\\Documents\\{_savefile}.png"
                with PIL.Image.open(skt) as im:
                    rs = im.resize((570,560), PIL.Image.BILINEAR)
                    rs.save(skt)
                    sg.popup('Saved in 600x600 format')
            """
            save_sketch_template(_savefile)
        except ValueError:
            # prevents crashing if file extension not added
            popup("Missing file extension. Please try again")
        except AttributeError:
            # prevents a crash if dialog is cancelled
            pass

    if event == "Save template as...":
        save_sketch_template()
    if event == "Load template":
        try:
            load_sketch_template()
        except FileNotFoundError:
            popup("Could not load template")

    if event == "Snap to Grid":

        if gridSnap is True:
            gridSnap = not gridSnap
            snap_to_grid_off()
            notify3.update(f"Snap to grid: {gridSnap}")
        else:
            gridSnap = not gridSnap
            snap_to_grid_on()
            notify3.update(f"Snap to grid: {gridSnap}")

    if event == "Render Template":
        try:
            render_template()
        except FileNotFoundError:
            popup("Could not load template")
            
    if event == "Exit":
        window.close()

##    if event == "Keyboard":
##        input_mode = "keyboard"
##        # if cursor was previously disabled, re-enable it
##
##        if TK.itemcget("cursor", "state") == "hidden":
##            TK.itemconfig("cursor", state="normal")
##
##        # draw_cursor if it wasn't already created
##        if not TK.find_withtag("cursor"):
##            cursor = draw_cursor(input_mode)

    if event == "Mouse/Keyboard":
        input_mode = ""
        hide_cursor(cursor)

    if event == "24":
        sg.Graph.set_size(graph, (480, 480))
        sg.Graph.change_coordinates(graph, (0, 24), (24, 0))
        graph.update()

    if event == "30":
        sg.Graph.set_size(graph, (600, 600))
        sg.Graph.change_coordinates(graph, (0, 24), (24, 0))
        graph.update()

    # routines

    if event == "Short Gas":
        short_gas()
    elif event == "Long Gas":
        long_gas()
    elif event == "Radius":
        radius_sketch()
    elif event == "St to St":
        st_to_st()
    elif event == "BL to BL":
        bl_to_bl()
    # left hand stuff

    if event == "tab1getstreet":
        street = get_input("Enter street name")
        window["tab1street"].update(street)

    if event == "read_file":
        file = popup_get_file("Choose template")
        read_from_template(file)

  

    if event == keys["m"] and current_mode == "chosen":
        current_mode = event_switch(
            "move", "Please click location to move to, press Esc when finished", window["stb_notify"]
        )

    if event.endswith("MOVE") and (current_mode == "text"):

        notify2.update(end_point)
        notify3.update(current_mode)
        try:
            end_point = values["graph"]
            sg.Graph.delete_figure(graph, etext)
            etext = sg.Graph.draw_text(
                graph,
                entered_text.upper(),
                end_point,
                color="black",
                font="Arial 10 bold",
            )
        except Exception as e:
            logerror(e)

    if event.endswith("MOVE"):
        notify3.update(end_point)

##    if event.endswith("MOVE") and in_graph is True:
##        try:
##            code to show an outline on highlighted figure
##            graph.delete_figure(outline)
##            bbox  = graph.get_bounding_box(TK.find_withtag("current"))
##            outline = graph.draw_rectangle((bbox[0][0],bbox[0][1]), (bbox[1][0],bbox[1][1]),line_color='blue',line_width=2)
##            sg.Graph.send_figure_to_back(graph, outline)
##            TK.itemconfig(outline, state="disabled", dash=(2,2))
##        except:
##            pass

    if event.endswith("MOVE") and (
        current_mode == "line2"
        or current_mode == "endcable"
        or current_mode == "offsetline2"
        or current_mode == "road2"
    ):
        notify2.update(end_point)
        notify3.update(current_mode)
        try:
            # notify2.update(TK.itemcget(hashline))
            end_point = values["graph"]
            sg.Graph.delete_figure(graph, hashline)
            # TK.coords(hashline,start_point[0]*20,start_point[1]*20,end_point[0]*20,end_point[1*20])
            hashline = sg.Graph.draw_line(graph, start_point, end_point, color="black")
            TK.itemconfig(hashline, dash=(2, 2))

        except Exception as e:
            logerror(e)

    if event.endswith("MOVE") and (
        current_mode == "building2" or current_mode == "digbox2"
    ):
        notify2.update(end_point)
        notify3.update(current_mode)
        try:
            # notify2.update(TK.itemcget(hashline))
            end_point = values["graph"]
            sg.Graph.delete_figure(graph, hashrect)
            # TK.coords(hashline,start_point[0]*20,start_point[1]*20,end_point[0]*20,end_point[1*20])
            hashrect = sg.Graph.draw_rectangle(
                graph, start_point, end_point, line_color="black"
            )
            TK.itemconfig(hashrect, dash=(2, 2))

        except Exception as e:
            pass

    if event.endswith("MOVE") and current_mode == "move":
        try:
            for item in selected:
                TK.itemconfig(item, state="disabled")
                sg.Graph.relocate_figure(
                    graph, item, values["graph"][0], values["graph"][1]
                )
                TK.itemconfig(item, state="normal")
        except IndexError:
            pass

    if event.endswith("MOVE") and current_mode == "chosen":
        if selected is None:
            current_mode = "select"
   

    # if event.endswith('drag'):
    #     try:
    #         if db:
    #             graph.delete_figure(db)
    #     except NameError:
    #         pas
    #     x,y = values['graph']
    #     startx,starty = x,y
    #     currentx,currenty = startx,starty
    #     db = sg.Graph.draw_rectangle(graph,(startx,starty),(currentx,currenty),line_color='red')
    #     graph.update()

    # keyboard cursor control
    if event == keys["down"] and input_mode == "keyboard":
        for section in cursor:
            sg.Graph.move_figure(graph, section, 0, 1)
            cursorpos = update_cursor_position(cursor)
            # Print(cursorpos)

    elif event == keys["up"] and input_mode == "keyboard":
        for section in cursor:
            sg.Graph.move_figure(graph, section, 0, -1)
            cursorpos = update_cursor_position(cursor)

    elif event == keys["right"] and input_mode == "keyboard":
        for section in cursor:
            sg.Graph.move_figure(graph, section, 1, 0)
            cursorpos = update_cursor_position(cursor)
    elif event == keys["left"] and input_mode == "keyboard":
        for section in cursor:
            sg.Graph.move_figure(graph, section, -1, 0)
            cursorpos = update_cursor_position(cursor)

    if (event == keys["esc"] or event == keys["="]) and current_mode == "nextcable":
        collecting = False
        cable_poly(*cpoints)
        cpoints.clear()
        for x in cnodes:
            sg.Graph.delete_figure(graph, x)
        cnodes.clear()

    if event == keys["esc"] or event == keys["="]:
        window["stb_notify"].update("Cancelled")
        graph.delete_figure(hashline)
        graph.delete_figure(hashrect)
        dragging = False
        try:
            graph.delete_figure(figrect)
        except NameError:
            pass
        if selected is not None:
      #      for item in selected[:]:
             for item in selected:
                if TK.type(item) == "rectangle" and "digbox" in TK.itemcget(
                    item, "tag"
                ):
                    TK.itemconfig("digbox", fill="#D3D3D3", stipple="gray25")
                elif TK.type(item) == "rectangle" or TK.type(item) == "oval":
                    TK.itemconfig(item, fill="white", outline="black")
                elif (
                    TK.type(item) == "line"
                    or TK.type(item) == "text"
                    or TK.type(item) == "polygon"
                ):
                    TK.itemconfig(item, fill="black")

                selected.remove(item)

        current_mode = "select"

    # try it out...

    if event in buttoniosingle.keys():
        notify.update("Choose insertion point")
        x, y = get_point1()
        try:
            buttoniosingle[event](x, y)
        except Exception as e:
            print(e)

    if event == "NEW FILE":
        sg.popup("New file")
        print(event, values)

    if event == keys["n"]:
        current_mode = event_switch("polyline", "Click next point of line", window["stb_notify"])

    if event == keys["F2"]:
        edit_text()

    if event == keys[">"]:
        current_mode = event_switch("arrow1", "Please click first arrow head", window["stb_notify"])
    if event == keys["s"]:
        current_mode = event_switch("select", "Select figure", window["stb_notify"])
    if event == keys["i"]:
        try:
            img = popup_get_file("Select image")
            sg.Graph.draw_image(graph, location=(0, 0), data=convert_to_bytes(img))
        except (PIL.UnidentifiedImageError, AttributeError):
            pass
    if event == keys["a"]:
        current_mode = event_switch("arc", "Please select first arc point", window["stb_notify"])
    if event == keys["h"]:
        current_mode = event_switch("harrow", "Please select first arrow point", window["stb_notify"])
    if event == keys["v"]:
        current_mode = event_switch("varrow", "Please select first arrow point", window["stb_notify"])
    if event == keys["V"]:
        current_mode = event_switch("vmultiarrow", "Please select reference point", window["stb_notify"])
    if event == keys["c"]:
        current_mode = event_switch("cable", "Please click first point of cable line:", window["stb_notify"])
    if event == keys["C"]:
        current_mode = event_switch(
            "cable arc", "Please click horizontal section of cable arc", window["stb_notify"]
        )
    if event == keys["o"]:
        current_mode = event_switch(
            "offsetline", "Please click first point of offset line:", window["stb_notify"]
        )
    if event == keys["d"]:
        current_mode = event_switch("digbox", "Please click first point of box:", window["stb_notify"])
    if event == keys["b"]:
        current_mode = event_switch(
            "building", "Please click upper left corner of building:", window["stb_notify"]
        )
    if event == keys["z"]:
        current_mode = "resize"
    if event == keys["B"]:
        current_mode = event_switch("house", "Please click upper left corner of house", window["stb_notify"])
    if event == keys["r"] or event == "Road":
        current_mode = event_switch("road", "Please click first point of curb line", window["stb_notify"])
    if event == keys["R"]:
        current_mode = event_switch(
            "road arc", "Please click horizontal section of road arc", window["stb_notify"]
        )
    if event == keys["_"]:
        current_mode = event_switch("corner", "Please click start point", window["stb_notify"])
    if event == keys["l"] or event == "Line":
        current_mode = event_switch("line", "Please click first point of line", window["stb_notify"])
    if event == keys["y"]:
        if TK.find_withtag("current") is not None:
            clone = clone_item("current")
            coords = get_figure_coords("current")
            figure_type = get_figure_type("current")
    if event == keys["p"]:
        try:
            paste_figure(figure_type, coords, clone)
        except NameError:
            pass
    if event == keys["g"]:
        if isGrid is False:
            isGrid = not isGrid
            try:
                show_grid()
            except FileNotFoundError:
                sg.popup('"grid2.png" could not be found - check location')
        else:
            if isGrid is True:
                isGrid = not isGrid
            try:
                hide_grid()
            except FileNotFoundError:
                sg.popup('"grid2.png" could not be found - check location')
    if event == keys["u"]:
        ids = list(graph.TKCanvas.find_all())
        if len(ids) < 1:
            pass
        else:
            graph.delete_figure(ids[-1])
    if event == keys["w"]:
        wipe()
    if event == keys["x"]:
        if TK.find_withtag("current") is not None:
            graph.delete_figure(TK.find_withtag("current"))
        if selected is not None:
            for item in selected:
                graph.delete_figure(item)
    if event == keys["t"]:
        entered_text = popup_get_text("Enter text")
        current_mode = event_switch("text", "Please click to enter text", window["stb_notify"])
    if event == keys["T"]:
        entered_text = popup_get_text("Enter text")
        current_mode = event_switch("vtext", "Please click to enter text", window["stb_notify"])
    if event == keys["e"]:
        entered_text = popup_get_text("Enter street name")
        current_mode = event_switch("street text", "Please click to enter text", window["stb_notify"])
    if event == keys["E"]:
        entered_text = popup_get_text("Enter street name")
        current_mode = event_switch("street vtext", "Please click to enter text", window["stb_notify"])
    # if event == "1":
    #     current_mode = event_switch('ped', 'Click to place pedestal')
    # if event == "!":
    #     current_mode = event_switch('ped stub', 'Click on ped location')
    # if event == "2":
    #     current_mode = event_switch('pole', 'Click to place pole')
    # if event == "@":
    #     current_mode = event_switch('pole stub', 'Click on pole location')
    # if event == "3":
    #     current_mode = "itemstamp"
    #     notify.update("Click to place stamp")
    # if event == "4":
    #     current_mode = "transformer"
    #     notify.update("Click to place transformer")
    # if event == "5":
    #     current_mode = "vault"
    #     notify.update("Click to place vault")
    # if event == "6":
    #     current_mode = "catch basin"
    #     notify.update("Click on catch basin location")

    """
    All events for button click
    
    """

     # BUTTON CLICK WITHOUT MOVEMENT
    if event == "graph" and current_mode == "select":
        x, y = values["graph"]
        if not dragging:
            start_point = (x, y)
            dragging = True
        else:
            end_point = (x, y)
        if prior_rect:
            graph.delete_figure(prior_rect)
        start_point = (x, y)

    if event == "graph" and current_mode == "chosen":
        x, y = values["graph"]
        if not dragging:
            start_point = (x, y)
            dragging = True
        else:
            end_point = (x, y)

    if event == "graphdrag" and dragging and current_mode == "select":
        try:
            x, y = values["graph"]
            end_point = (x, y)
            graph.delete_figure(prior_rect)
            prior_rect = sg.Graph.draw_rectangle(
                graph,
                start_point,
                end_point,
                fill_color=None,
                line_color="blue",
                line_width=1,
            )
        except IndexError:
            pass

    if event == "graphdrag" and current_mode == "chosen":
        x, y = values["graph"]
        end_point = (x, y)
        try:
            for idx, item in enumerate(selected):
                dx = end_point[0] - start_point[0]
                dy = end_point[1] - start_point[1]
                graph.move_figure(item, dx, dy)
            start_point = end_point
        except Exception as e:
            pass
        
    if event.endswith("+UP"):
        # signals end of drag or button click
        if dragging:
            try:
                enclosing = TK.coords(prior_rect)
                print(f'Enclosing rectangle coords: {enclosing}')
                enclosed_items = TK.find_enclosed(*enclosing)
                graph.delete_figure(prior_rect)
                enclosed_items = list(enclosed_items)
                print(f'Enclosed item IDS are: {enclosed_items}')
                #enclosed_items.remove(prior_rect)
                for item in enclosed_items:
                    print(item)
                    TK.itemconfig(item, fill="red")
                    selected.append(item)
                print(selected)
                enclosing = []
                
            except Exception as e:
                print(e)
            start_point = end_point = prior_rect = None
            dragging = False

        if current_mode == "cable":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            current_mode = "endcable"
            start_point = (x, y)
            point1 = draw_point1(x, y)
            # had to add this in since the event was registering 2 clicks for some reason?
            time.sleep(0.15)
            current_mode = "endcable"
            # easy_print("obtained point1")
            window["stb_notify"].update("Click second point of line")

        elif current_mode == "polyline":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y)
            cpoints.append((x, y))
            cnodes.append(point1)
            x = y = point1 = None
            notify.update("Click next point of line")
            current_mode = "nextcable"
            
        elif current_mode == "cable arc":
            x, y = get_point1()
            point1 = draw_point1(x, y)
            notify.update("Click vertical section of cable arc")
            current_mode = "cable arc 2"
        elif current_mode == "offsetline":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            start_point = (x, y)
            current_mode = "offsetline2"
            point1 = draw_point1(x, y)
            notify.update("Click second point of line")

        elif current_mode == "digbox":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            start_point = (x, y)
            point1 = draw_point1(x, y, "green")
            notify.update("Click second point of line")
            current_mode = "digbox2"
        elif current_mode == "house":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            hn = popup_get_text("House number:?")
            hs = popup_get_text("Size (s/m/l):")
            try:
                house(x, y, hs, hn)
            except Exception as e:
                logging.exception("ERROR")

        elif current_mode == "building":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            start_point = (x, y)
            point1 = draw_point1(x, y, "black")
            notify.update("Click lower right corner of building")
            current_mode = "building2"
        elif current_mode == "road":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            start_point = (x, y)
            current_mode = "road2"
            point1 = draw_point1(x, y, "purple")
            notify.update("Click second point of curb")

        elif current_mode == "road arc":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y, "purple")
            notify.update("Click vertical section of road arc")
            current_mode = "road arc 2"
        elif current_mode == "line":

            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            start_point = (x, y)
            current_mode = "line2"
            point1 = draw_point1(x, y, "blue")
            notify.update("Click second point of line")
        elif current_mode == "corner":
            x, y = get_point1()
            start_point = (x, y)
            current_mode = "corner2"
            point1 = draw_point1(x, y, "purple")
            notify.update("Click horizontal section of arc")
        elif current_mode == "arc":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y, "purple")
            notify.update("Click second arc point")
            current_mode = "arc2"
        elif current_mode == "harrow":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y, "orange")
            notify.update("Click second arrow point")
            current_mode = "harrow2"
        elif current_mode == "varrow":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y, "orange")
            notify.update("Click second arrow point")
            current_mode = "varrow2"
        elif current_mode == "vmultiarrow":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y, "orange")
            notify.update("Click first cable")
            current_mode = "vmultiarrow2"

        elif current_mode == "arrow1":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y, "orange")
            notify.update("Click second arrow head")
            current_mode = "arrow2"
        elif current_mode == "arrow2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point1()
            point2 = draw_point2(a, b, color="orange")
            try:
                rarrow(x, y, a, b)
            except Exception as e:

                # FIXME - can't put 2 arrow heads on same point - crashes
                logerror(e)
            cleanup_2point()

        elif current_mode == "endcable":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point1()
            point2 = draw_point2(a, b, "red")
            # easy_print("received point 2")
            # label = popup_get_text('Label? ')
            cable(x, y, a, b)
            add_figure_to_record(record, "cable", x, y, a, b)
            cleanup_2point()
            current_mode = "cable"
        elif current_mode == "nextcable":
            collecting = True
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "red")
            cpoints.append((a, b))
            cnodes.append(point2)
            a = b = point2 = None
        elif current_mode == "cable arc 2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(x, y, "red")
            arc(x, y, a, b, "cable")
            cleanup_2point()
            current_mode == "cable arc"
        elif current_mode == "offsetline2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(x, y, "brown")
            offset_line(x, y, a, b)
            cleanup_2point()
        elif current_mode == "digbox2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "green")
            digbox(x, y, a, b)
            cleanup_2point()
            current_mode == "select"
        elif current_mode == "building2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "black")
            # TODO wrap this
            building(x, y, a, b)
            cleanup_2point()
        elif current_mode == "road2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "purple")
            road(x, y, a, b)
            add_figure_to_record(record, "road", x, y, a, b)
            cleanup_2point()
            current_mode = "road"
        elif current_mode == "road arc 2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "purple")
            arc(x, y, a, b, "road")
            cleanup_2point()
            current_mode = "road arc"
        elif current_mode == "corner2":
            a, b = get_point()
            point2 = draw_point2(a, b)
            current_mode = "corner3"
            notify.update("Please click arc end")

        elif current_mode == "corner3":
            c, d = get_point()
            point3 = draw_point3(c, d)
            current_mode = "corner4"
            notify.update("Please click road end")

        elif current_mode == "corner4":
            e, f = get_point()
            point4 = draw_point4(e, f)
            road_corner((x, y), (a, b), (c, d), (e, f))
            graph.delete_figure(point1)
            graph.delete_figure(point2)
            graph.delete_figure(point3)
            graph.delete_figure(point4)
            x = y = a = b = c = d = e = f = 0
            current_mode = "select"

        elif current_mode == "line2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "blue")
            line(x, y, a, b)
            cleanup_2point()
            current_mode = "line"
        elif current_mode == "arc2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "purple")
            arc(x, y, a, b)
            cleanup_2point()
            current_mode = "arc"
        elif current_mode == "harrow2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "orange")
            meas = convert_measurement()
            h_arrow(x, a, y, meas)
            cleanup_2point()
        elif current_mode == "varrow2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "orange")
            meas = convert_measurement()
            v_arrow(x, y, b, meas)
            cleanup_2point()
        elif current_mode == "vmultiarrow2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "orange")
            current_mode = "vmultiarrow3"
            notify.update("Please select 2ndcable")
            
        elif current_mode == "vmultiarrow3":
            c, d = get_point3()
            point3 = draw_point3(c, d, "orange")
            newmeas = convert_multi_measurement()
            try:
                v_multi_arrow(x, y, b, d, f"{newmeas[0]},{newmeas[1]}")
            except IndexError:
                logerror(e)
            x = y = a = b = c = d = None
            for _ in (point1, point2, point3):
                graph.delete_figure(_)
            current_mode = "select"
            
        elif current_mode == "text":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            hlabel(entered_text, x, y, 12)
            graph.delete_figure(etext)
            x = y = entered_text = None
            
        elif current_mode == "street text":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            hlabel(entered_text, x, y, 20, bold=False)
            x = y = entered_text = None
            
        elif current_mode == "street vtext":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            vlabel(entered_text, x, y, 20, bold=False)
            x = y = entered_text = None
            
        elif current_mode == "vtext":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            vlabel(entered_text, x, y, 12)
            x = y = entered_text = None
            
        elif current_mode == "ped":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            ped(x, y)
            x = y = None
            
        elif current_mode == "ped stub":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y)
            notify.update("Click cable stub end")
            current_mode = "ped stub 2"
            
        elif current_mode == "ped stub 2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "red")
            ped_1arm(x, y, a, b)
            cleanup_2point()
            
        elif current_mode == "pole":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            pole(x, y)
            x = y = None
            
        elif current_mode == "pole stub":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            point1 = draw_point1(x, y)
            notify.update("Click cable stub end")
            current_mode = "pole stub 2"
            
        elif current_mode == "pole stub 2":
            if input_mode == "keyboard":
                a, b = update_cursor_position(cursor)
            else:
                a, b = get_point2()
            point2 = draw_point2(a, b, "red")
            pole_1arm(x, y, a, b)
            cleanup_2point()
            
        elif current_mode == "itemstamp":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            item_stamp(x, y)
            x = y = None
        elif current_mode == "transformer":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            transformer(x, y)
            x = y = None
        elif current_mode == "vault":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            utility = get_input("Bell?")
            if utility in ["y", "Y", "yes", "YES", "Yes"]:
                vault(x, y, "b")
            else:
                vault(x, y)
        elif current_mode == "catch basin":
            if input_mode == "keyboard":
                x, y = update_cursor_position(cursor)
            else:
                x, y = get_point1()
            catch_basin(x, y)
            
        elif current_mode == "select":
            fig = TK.find_withtag("current")
            if fig != ():
                window["lblobject_type"].update(TK.type(fig))
                window["objcoords"].update(graph.get_bounding_box(fig))
                window["tag"].update(TK.itemcget(fig, "tag"))
                window["ID"].update(graph.get_figures_at_location(values["graph"]))
            # drag_figures =sg.Graph.get_figures_at_location(graph,values['graph'])
            # if drag_figures:
            #     for fig in drag_figures:
            #         if TK.itemcget(fig,'tag') == 'g/rid':
            #             pass
            #         else:
            # easy_print(graph.TKCanvas.type(fig))
            # easy_print(type(fig))
            # bb = sg.Graph.get_bounding_box(graph,fig)
            # bbr= sg.Graph.draw_rectangle(graph,(bb[0]),bb[1], line_color='blue')
            # notify2.update(TK.type(fig) + ',' +TK.itemcget(fig,'tag'))
            if "ped" in TK.gettags(fig):
                TK.itemconfig(fig, fill="red")
                TK.itemconfig(fig[0] + 1, fill ="red")
                TK.itemconfig(fig[0] + 2, fill="red")
                selected.append(fig)
                selected.append(fig[0] + 1)
                selected.append(fig[0] + 2)
                
            elif TK.type(fig) == "image":
                imgb = graph.get_bounding_box(fig)
                print(imgb)
                figrect = sg.Graph.draw_rectangle(
                    graph,
                    (imgb[0][0], imgb[0][1]),
                    (imgb[1][0], imgb[1][1]),
                    line_color="red",
                    fill_color="",
                )
                selected.append(fig)
                selected.append(figrect)
            else:
                TK.itemconfig(fig, fill="red")
                selected.append(fig)
            # for i in selected:
            #     try:
            #         ulc = TK.bbox(i)
            #         print(ulc)
            #         ulc = (ulc[0] // 20,ulc[1] //20)
            #         spoints.append(ulc)
            #     except TypeError:
            #         pass
            # print(spoints)
            current_mode = "chosen"

        elif current_mode == "move":
            try:
                x, y = get_point1()
                for item in selected:
                    graph.move((x - start_point[0]), (y - start_point[1]))
                # if TK.itemcget(fig,'tag') == 'arrow1':

                #     graph.relocate_figure('arrow1',x,y)
                # elif TK.itemcget(fig,'tag') == 'arrow2':
                #     graph.relocate_figure('arrow2',x,y)
                # elif TK.itemcget(fig,'tag') == 'cable':
                #     graph.relocate_figure('cable',x,y)
                # else:
                #     graph.relocate_figure(fig,x,y)
                # sg.Graph.delete_figure(bbr)
                # TK.itemconfig(fig,fill='black')
                x = y = None
            except Exception as e:
                logging.exception("There was an error")


window.close()
