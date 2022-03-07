import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import EasyPrint, easy_print

sg.theme("dark amber")
# ystem of 24x24 on this one - weird i know
# CONSTANTS

HEIGHT = 24
WIDTH = 24


# WRAPPER FUNCTIONS
def show_grid():
    """
    Turns grid on
    """
    # draws grid
    for x in range(WIDTH):
        graph.DrawLine((x, 0), (x, HEIGHT), color="grey")
    for y in range(HEIGHT):
        graph.DrawLine((0, y), (WIDTH, y), color="grey")

    # draws in numbers
    for a in range(0, WIDTH, 2):
        graph.DrawText(a, (a, 0.4), font="Arial 9 normal", angle=90)
    for b in range(0, HEIGHT, 2):
        graph.DrawText(
            b,
            (0.4, b),
            font="Arial 9 normal",
        )


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

    if x1 > x2:
        arrow("w", x1, y)
        arrow("e", x2, y)
        if measdir.lower() == "l":
            hlabel(meas, x2 - 2.8, y, 11)
        elif measdir.lower() == "r":
            hlabel(meas, x1 + 2.8, y, 11)
    else:
        arrow("e", x1, y)
        arrow("w", x2, y)
        if measdir.lower() == "l":
            hlabel(meas, x1 - 2.8, y, 11)
        elif measdir.lower() == "r":
            hlabel(meas, x2 + 2.8, y, 11)


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
    if y1 > y2:
        arrow("n", x, y1)
        arrow("s", x, y2)
        if measdir.lower() == "u":
            vlabel(meas, x, y2 - 2.8, 11)
        elif measdir.lower() == "d":
            vlabel(meas, x, y1 + 2.8, 11)
    else:
        arrow("s", x, y1)
        arrow("n", x, y2)
        if measdir.lower() == "u":
            vlabel(meas, x, y1 - 2.8, 11)
        elif measdir.lower() == "d":
            vlabel(meas, x, y2 + 2.8, 11)


def pole(x, y):
    graph.draw_circle((x, y), 0.4, fill_color="white")


def transformer(x, y):
    graph.draw_rectangle((x - 0.5, y - 0.5), (x + 0.5, y + 0.5), line_color="black")
    graph.draw_polygon(
        [(x, y - 0.5), (x - 0.5, y + 0.5), (x + 0.5, y + 0.5)], fill_color="black"
    )


def vault(util, x, y):
    vlbl = "FTG" if util.lower() == "b" else "HW"
    v1 = graph.draw_rectangle(
        (x - 0.7, y - 0.4), (x + 0.7, y + 0.4), line_color="black", fill_color=None
    )
    v2 = graph.draw_text(vlbl, (x, y), font="Arial 3 normal")
    # prfloat(v2)
    graph.bring_figure_to_front("v2")


def hlabel(msg, x, y, size):
    sg.Graph.draw_text(graph, msg, (x, y), font=f"Arial {str(size)} normal")


def vlabel(msg, x, y, size):
    sg.Graph.draw_text(
        graph, msg, (x, y), font=f"Arial {str(size)} normal", angle=90
    )


def ped(x, y):
    sg.Graph.draw_rectangle(
        graph, (x - 0.4, y - 0.4), (x + 0.4, y + 0.4), line_color="black", line_width=1
    )
    sg.Graph.draw_line(graph, (x - 0.4, y - 0.4), (x + 0.4, y + 0.4))
    sg.Graph.draw_line(graph, (x - 0.4, y + 0.4), (x + 0.4, y - 0.4))


def ped_1arm(x, y, direction="", distance=""):
    """
    Creates a ped with stub (with or without measurement)

        Parameters:
            x : x coord
            y: y coord
            direction(str): N, S, E or W
            distance: how many squares from ped

        Returns:
            None
    """
    ped(x, y)
    if direction.lower() == "n":
        cable(x, y - 0.4, x, y - distance)
    elif direction.lower() == "s":
        cable(x, y + 0.4, x, y + distance)
    elif direction.lower() == "w":
        cable(x - 0.4, y, x - distance, y)
    elif direction.lower() == "e":
        cable(x + 0.4, y, x + distance, y)


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
        v_arrow(x - arm_offset, y - arm_offset, y, meas1, "u")
        # lower measurement
        v_arrow(x - arm_offset2, y, y + arm_offset, meas2, "d")


def road(*args):
    return graph.draw_line((args[0], args[1]), (args[2], args[3]), width=3)


def h_road(x1, x2, y):
    road(x1, y, x2, y)


def v_road(x, y1, y2):
    road(x, y1, x, y2)


def cable(x1, y1, x2, y2):
    cable = graph.DrawLine((x1, y1), (x2, y2), width="2")
    graph.TKCanvas.itemconfig(cable, dash=(10, 5))


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
            s = 0.25 if len(label) <= 2 else 0.6
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
            s = 0.25 if len(label) <= 2 else 0.6
            sg.Graph.draw_rectangle(
                graph,
                (x - s, y - s),
                (x + s, y + s),
                fill_color="white",
                line_color="white",
            )
            vlabel(label, x, y, 7)


def line():
    pass


def digbox(x1, y1, x2, y2):
    db = graph.draw_rectangle(
        (x1, y1), (x2, y2), fill_color="#D3D3D3", line_color="black"
    )
    graph.TKCanvas.itemconfig(db, stipple="gray50")
    graph.send_figure_to_back(db)


def located_area(x, y):
    sg.Graph.draw_text(graph, "LOCATED AREA", (x, y), font="Arial 12 bold")


def house(x, y, size, num):
    if size == "m":
        graph.draw_rectangle((x, y), (x + 4, y + 4))


# setup

tab2layout = [
    [
        sg.Text("Dig box size around pole"),
        sg.Combo((3, 4, 5), s=5, enable_events=True, key="dbsize", default_value=0),
    ],
    [
        sg.Text("Pole 2 location(x,y):"),
        sg.I(
            s=5,
            enable_events=True,
            key="pole2",
        ),
    ],
    [
        sg.Text("Curb: "),
        sg.Combo(["N", "S", "E", "W"], s=5, enable_events=True, key="curb"),
    ],
    [sg.Text("Street name: "), sg.I(s=10, key="sn", enable_events=True)],
    [
        sg.Text("Cables(x1,y1,x2,y2) "),
        sg.Text("1."),
        sg.I(
            s=5,
            key="cab1",
            justification="right",
            enable_events=True,
            default_text="0,0,0,0",
        ),
    ],
    [
        sg.Text("2.", justification="right"),
        sg.I(
            s=5,
            key="cab2",
            justification="right",
            enable_events=True,
            default_text="0,0,0,0",
        ),
    ],
    [
        sg.Text("3.", justification="right"),
        sg.I(
            s=5,
            key="cab3",
            justification="right",
            enable_events=True,
            default_text="0,0,0,0",
        ),
    ],
    [
        sg.Text("4.", justification="right"),
        sg.I(
            s=5,
            key="cab4",
            justification="right",
            enable_events=True,
            default_text="0,0,0,0",
        ),
    ],
    [
        sg.Text("Arrows (dir,x,y): "),
        sg.Text("1."),
        sg.I(key="a1", s=8, enable_events=True, default_text="n,0,0"),
    ],
    [
        sg.Text("2.", justification="right"),
        sg.I(key="a2", s=5, enable_events=True, default_text="n,0,0"),
    ],
    [
        sg.Text("3.", justification="right"),
        sg.I(key="a3", s=5, enable_events=True, default_text="n,0,0"),
        sg.Text("4.", justification="right"),
        sg.I(key="a4", s=5, enable_events=True, default_text="n,0,0"),
    ],
    [
        sg.Text("Horizontal labels(text,x,y):"),
        sg.Text("1."),
        sg.I(size=7, key="hl1", enable_events=True, default_text="'',0,0"),
        sg.Text("2."),
        sg.I(key="hl2", s=7, enable_events=True, default_text="'',0,0"),
        sg.Text("3."),
        sg.I(key="hl3", s=7, enable_events=True, default_text="'',0,0"),
        sg.Text("4."),
        sg.I(key="hl4", s=7, enable_events=True, default_text="'',0,0"),
    ],
    [
        sg.Text("Vertical labels(text,x,y):"),
        sg.Text("1."),
        sg.I(size=7, key="vl1", enable_events=True, default_text="'',0,0"),
        sg.Text("2."),
        sg.I(key="vl2", s=7, enable_events=True, default_text="'',0,0"),
        sg.Text("3."),
        sg.I(key="vl3", s=7, enable_events=True, default_text="'',0,0"),
        sg.Text("4."),
        sg.I(key="vl4", s=7, enable_events=True, default_text="'',0,0"),
    ],
    [
        sg.Text("Located area location:(x,y)"),
        sg.I(s=5, enable_events=True, key="la", default_text="0,0"),
    ],
    [
        sg.Text("Regular line(x1,y1,x2,y2"),
        sg.I(s=5, enable_events=True, key="laline", default_text="0,0,0,0"),
    ],
    [sg.Submit()],
]

tab1layout = [[sg.Text("placeholder")]]
lcol = [
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("SketchBuilder", tab1layout, tooltip="Test"),
                    sg.Tab("Poles", tab2layout, tooltip="Pole drawings"),
                ]
            ]
        )
    ]
]

rcol = [
    [
        sg.Graph(
            canvas_size=(480, 480),
            graph_bottom_left=(0, HEIGHT),
            graph_top_right=(WIDTH, 0),
            background_color="white",
            key="graph",
            enable_events=True,
            drag_submits=True,
        )
    ]
]

layout = [
    [sg.Column(lcol), sg.Column(rcol)],
    # [sg.Text('Select Image:'),sg.Input(key='file',enable_events=True),sg.FileBrowse(enable_events=True)]
    # [sg.Button('Add to image',enable_events=True,key='add')]
]

window = sg.Window(
    "Graph test",
    layout,
    finalize=True,
    font="Arial",
    resizable=True,
    return_keyboard_events=True,
)

graph = window["graph"]
# graph for testing
# show_grid()


def draw_polesketch(street, dir, cabloc, msmt):
    pass


# pre loop drawing

# show_grid()
# s
road(4, 8, 20, 8)
hlabel("STRAWBERRY LN", 12, 2, 20)
h_cable(4, 20, 9, "B")
# cabloc n
v_arrow(18, 8, 9, "1.2m", "u")
sg.Graph.draw_rectangle(graph, (8, 14), (15, 18), line_color="black")
hlabel("571", 11.5, 16, 16)
h_arrow(15, 17, 12, "2.0m", "r")
hlabel("SRE", 5, 7, 11)
sg.Graph.draw_circle(graph, (17, 9), 0.3, fill_color="red")
vlabel("EBL", 16, 16, 11)
hlabel("100 pair damage", 10, 5, 11)

graph.draw_line((11, 6), (17, 9))
"""
find_all finds all ids to use for undo / redo
ids = list(graph.TKCanvas.find_all())
for x in range(max(ids), max(ids)-10, -1):
    graph.delete_figure(x)
easy_print(graph.TKCanvas.find_all())
"""
# event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "u":
        ids = list(graph.TKCanvas.find_all())
        graph.delete_figure(ids[-1])
    elif event == "Submit":
        # clear graph first before redrawing
        graph.erase()

        # initial pole
        pole(12, 12)

        # dig box
        try:
            digbox(
                12 - int(values["dbsize"]),
                12 - int(values["dbsize"]),
                12 + int(values["dbsize"]),
                12 + int(values["dbsize"]),
            )
        except ValueError:
            pass

        # pole 2(optional)
        try:
            pl = values["pole2"].split(",")
            pole(float(pl[0]), float(pl[1]))

        except ValueError:
            pass

        # curb

        if values["curb"].lower() == "n":
            road(0, 16, 24, 16)
            hlabel("NCL", 22, 15, 12)
        elif values["curb"].lower() == "s":
            road(0, 8, 24, 8)
            hlabel("SCL", 22, 9, 12)
        elif values["curb"].lower() == "w":
            road(16, 0, 16, 24)
            vlabel("WCL", 15, 2, 12)
        elif values["curb"].lower() == "e":
            road(8, 0, 8, 24)
            vlabel("ECL", 9, 2, 12)

        # street name
        if values["curb"].lower() == "n":
            hlabel(values["sn"], 12, 20, 20)
        elif values["curb"].lower() == "s":
            hlabel(values["sn"], 12, 4, 20)
        elif values["curb"].lower() == "w":
            vlabel(values["sn"], 20, 12, 20)
        elif values["curb"].lower() == "e":
            vlabel(values["sn"], 4, 12, 20)

        # cables

        try:
            lcab1 = values["cab1"].split(",")
            cable(float(lcab1[0]), float(lcab1[1]), float(lcab1[2]), float(lcab1[3]))
            lcab2 = values["cab2"].split(",")
            cable(float(lcab2[0]), float(lcab2[1]), float(lcab2[2]), float(lcab2[3]))
            lcab3 = values["cab3"].split(",")
            cable(float(lcab3[0]), float(lcab3[1]), float(lcab3[2]), float(lcab3[3]))
            lcab4 = values["cab4"].split(",")
            cable(float(lcab4[0]), float(lcab4[1]), float(lcab4[2]), float(lcab4[3]))
        except:
            pass
        # arrows:
        try:
            la1 = values["a1"].split(",")
            arrow(la1[0], float(la1[1]), float(la1[2]))
            la2 = values["a2"].split(",")
            arrow(la2[0], float(la2[1]), float(la2[2]))
            la3 = values["a3"].split(",")
            arrow(la3[0], float(la3[1]), float(la3[2]))
            la4 = values["a4"].split(",")
            arrow(la4[0], float(la4[1]), float(la4[2]))
        except:
            pass

        # h label
        try:
            lhl1 = values["hl1"].split(",")
            hlabel(lhl1[0], float(lhl1[1]), float(lhl1[2]), 11)
            lhl2 = values["hl2"].split(",")
            hlabel(lhl2[0], float(lhl2[1]), float(lhl2[2]), 11)
            lhl3 = values["hl3"].split(",")
            hlabel(lhl3[0], float(lhl3[1]), float(lhl3[2]), 11)
            lhl4 = values["hl4"].split(",")
            hlabel(lhl4[0], float(lhl4[1]), float(lhl4[2]), 11)
        except:
            pass

        # v label
        try:
            lvl1 = values["vl1"].split(",")
            vlabel(lvl1[0], float(lvl1[1]), float(lvl1[2]), 11)
            lvl2 = values["vl2"].split(",")
            vlabel(lvl2[0], float(lvl2[1]), float(lvl2[2]), 11)
            lvl3 = values["vl2"].split(",")
            vlabel(lvl3[0], float(lvl3[1]), float(lvl3[2]), 11)
            lvl4 = values["vl2"].split(",")
            vlabel(lvl4[0], float(lvl4[1]), float(lvl4[2]), 11)
        except:
            pass

        # located area
        try:
            lla = values["la"].split(",")
            hlabel("LOCATED AREA", float(lla[0]), float(lla[1]), 12)
        except:
            pass
        # line
        try:
            llaline = values["laline"].split(",")
            sg.Graph.draw_line(
                graph,
                (float(llaline[0]), float(llaline[1])),
                (float(llaline[2]), float(llaline[3])),
            )
        except:
            pass
        # graph.delete_figure(newroad)
        # road(values['culx'], values['culy'], values['clrx'], values['clry'])
    # if event == 'add':
    # prfloat(values['file'])
    # graph.DrawText((values['file']), (200,200))
    # graph.draw_image(filename=values['file'],location=(100,100))
window.close()
