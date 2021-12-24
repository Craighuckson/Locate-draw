# TODO - MAKE SWITH FOR DIFFERENT FORMS BELL PRIM BELL AUX ROGERS PRIM AND AUX
# TODO - finish update button handling for bell primary and test

import shutil
import datetime
import PySimpleGUI as sg
import PIL
from PIL import ImageGrab, ImageFont
from PIL import ImageDraw, Image
import io
import base64


from PySimpleGUI.PySimpleGUI import BUTTON_TYPE_READ_FORM, WIN_CLOSED, popup

d = datetime.datetime.now()

# CONSTANTS
PAGESIZE = (816, 1056)
RP_TOTALPAGES = (776, 20)
BP_TOTALPAGES = (778, 23)
RP_UNITS = (765, 105)
BP_UNITS = (775, 104)
MFONT = "Arial 12 normal"
LFONT = "Arial 20 normal"
RP_NBOUNDARY = (51, 243)
RP_SBOUNDARY = (449, 244)
RP_WBOUNDARY = (55, 276)
RP_EBOUNDARY = (449, 274)
RA_NBOUNDARY = (60,220)
RA_SBOUNDARY = (443,220)
RA_WBOUNDARY = (57,238)
RA_EBOUNDARY = (443,238)
DATE = str("/".join([d.strftime(x) for x in ["%Y", "%m", "%d"]]))
NAME = "CRAIG HUCKSON"
RP_NAMECOORDS = (340, 967)
BP_NAMECOORDS = (345, 929)
LOCATORID = 130003
LOCATORIDCOORDS = (341, 1003)
RP_DATECOORDS = (620, 967)
BP_DATECOORDS = (368, 985)
BP_CABLE = (215, 276)
BP_CONDUIT = (303, 277)
BP_PAINT = (162, 310)
BP_FLAGS = (285, 311)
BP_GUIDELINES = (557, 939)
BP_MARKEMAIL = (558, 991)
BP_TEXT = "x"
RP_MOMTEXT = "x"
RP_MOMCOORDS = (40, 810)
RP_MEMAILTEXT = "x"
MEMAILCOORDS = (544, 1002)
RP_CLEARIMAGECOORDS = (428, 536)
rogclear = {
    "reg_clear": "rogclear.PNG",
    "ftth": "ftthstamp.PNG",
    "fo_only": "exclusion.PNG",
}

bell_stickers = {
    "bridge": {"file": "bsticker bridge.jpg", "coords": (227, 452)},
    "priority": {"file": "bsticker priority.jpg", "coords": (236, 567)},
    "cabcon": {"file": "bsticker cables mb in conduit.jpg", "coords": (22, 703)},
    "empty": {"file": "bsticker empty conduit.jpg", "coords": (30, 813)},
    "handdig": {"file": "bsticker hand dig.jpg", "coords": (480, 686)},
    "futureuse": {"file": "bsticker future use.jpg", "coords": (447, 808)},
}

# FUNCTIONS


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
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize(
            (int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS
        )
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


def move_files(form, filename):
    formdict = {
        "rp": "rpfile.png",
        "bp": "bpfile.png",
        "ra": "rafile.png",
        "ba": "bafile.png",
    }
    for k, v in formdict.items():
        if k == form:
            shutil.copy(v, f"C:\\Users\\Cr\\Documents\\{filename}")
    move_file_notification(filename)


def move_file_notification(filename):
    popup(f"File saved to C:\\Users\\Cr\Documents\\{filename}")


# LAYOUT

rp_tab = [
    [
        sg.Text("Total pages: "),
        sg.Input(s=5, key="tp"),
        sg.Text("Units: "),
        sg.Input(size=5, k="lunits"),
    ],
    [sg.Text("North Boundary: "), sg.Input(enable_events=True, key="nb")],
    [sg.Text("South Boundary: "), sg.Input(enable_events=True, key="sb")],
    [sg.Text("West Boundary: "), sg.Input(enable_events=True, key="wb")],
    [sg.Text("East Boundary: "), sg.Input(enable_events=True, key="eb")],
    [
        sg.Radio(
            "Marked", group_id="mc", default=True, k="rmarked", enable_events=True
        ),
        sg.Radio("Clear", group_id="mc", k="rclear", enable_events=True),
        sg.Text("Clear reason:"),
        sg.Combo(
            values=[rogclear["reg_clear"], rogclear["ftth"], rogclear["fo_only"]],
            default_value=rogclear["reg_clear"],
            enable_events=True,
            k="clear_reason",
            visible=False,
        ),
    ],
    [sg.Text("Insert Sketch:"), sg.I(k="rp_sketch"), sg.FileBrowse()],
    [
        sg.B("Update", BUTTON_TYPE_READ_FORM, k="rpupdate"),
        sg.Button("Display", k="rp-display"),
    ],
    [
        sg.Text("Save file name"),
        sg.I(k="rpsavefile"),
        sg.Button("Copy to Docs", k="rpfilemove"),
    ],
]

ra_tab = [
    [sg.Text("North Boundary: "), sg.Input(enable_events=True, key="ranb")],
    [sg.Text("South Boundary: "), sg.Input(enable_events=True, key="rasb")],
    [sg.Text("West Boundary: "), sg.Input(enable_events=True, key="rawb")],
    [sg.Text("East Boundary: "), sg.Input(enable_events=True, key="raeb")],
    [sg.Text("Insert Sketch:"), sg.I(k="ra_sketch"), sg.FileBrowse()],
    [
        sg.B("Update", BUTTON_TYPE_READ_FORM, k="raupdate"),
        sg.Button("Display", k="ra-display"),
    ],
    [
        sg.Text("Save file name"),
        sg.I(k="rasavefile"),
        sg.Button("Copy to Docs", k="rafilemove"),
    ],
]

bp_tab = [
    [
        sg.Text("Total pages: "),
        sg.Input(s=5, key="bptp"),
        sg.Text("Units: "),
        sg.Input(size=5, k="blunits"),
    ],
    [
        sg.Checkbox("Cable", enable_events=True, k="cable"),
        sg.Checkbox("Conduit", enable_events=True, k="conduit"),
    ],
    [sg.Text("Stickers:")],
    [sg.Checkbox("Bridge", enable_events=True, k="bridge")],
    [sg.Checkbox("Priority", enable_events=True, k="priority")],
    [sg.Checkbox("Cables MB In Conduit", enable_events=True, k="cabcon")],
    [sg.Checkbox("Hand Dig Only", enable_events=True, k="handdig")],
    [sg.Checkbox("Empty Conduits", enable_events=True, k="empty")],
    [sg.Checkbox("Future Use", enable_events=True, k="futureuse")],
    [
        sg.B("Update", BUTTON_TYPE_READ_FORM, k="bpupdate"),
        sg.Button("Display", k="bp-display"),
    ],
    [
        sg.Text("Save file name"),
        sg.I(k="bpsavefile"),
        sg.Button("Copy to Docs", k="bpfilemove"),
    ],
]

ba_tab = [[sg.Text("todo")]]

lcol = [
    [sg.Text("Choose form:"), sg.I(k="infile", enable_events=True), sg.FileBrowse()],
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Bell Primary", bp_tab),
                    sg.Tab("Bell Auxilliary", ba_tab),
                    sg.Tab("Rogers Primary", rp_tab),
                    sg.Tab("Rogers Auxilliary", ra_tab),
                ]
            ]
        )
    ],
]
rcol = [[sg.Image(expand_y=True,expand_x=True,key="img")]]

layout = [
    [
        sg.Column(lcol),
        sg.Column(
            rcol,
            scrollable=True,
            expand_x=True,
            expand_y=True,
        ),
    ]
]
# tp = input('Total pages: ')
# lunits = input('Units? ')
# nbound = input('North boundary?')
# sbound = input('South boundary?')
# wbound = input('West boundary? ')
# ebound = input('East boundary? ')
# clearmsg = input('Clear message? ')

window = sg.Window(
    "Locate form filler",
    layout,
    resizable=True,
    grab_anywhere=True,
    finalize=True,
)

# SETUP SECTION

fntm = ImageFont.truetype("arialbd.ttf", size=12)
fntl = ImageFont.truetype("arialbd.ttf", size=16)


# MAIN LOOP

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        break

    # shows stuff in right column
    if event == "infile":
        window["img"].update(data=convert_to_bytes(values["infile"]))

    if event == "rclear":
        window["clear_reason"].update(visible=True)

    elif event == "rmarked":
        window["clear_reason"].update(visible=False)

    if event == "rpupdate":
        # this writes in the dig area and other shiT
        with Image.open(values["infile"]) as out:

            d = ImageDraw.Draw(out)

            """
               rp_dict = {
                    RP_TOTALPAGES: str(values["tp"]),
                    RP_UNITS: values["lunits"],
                    RP_NBOUNDARY: values["nb"],
                RP_SBOUNDARY: values["sb"],
                RP_WBOUNDARY: values["wb"],
                RP_EBOUNDARY: values["eb"],
                RP_NAMECOORDS: NAME,
                RP_DATECOORDS: str(DATE),
                MEMAILCOORDS: RP_MEMAILTEXT,
                LOCATORIDCOORDS: str(LOCATORID),
            }

            """
            rp_dict = {
                RP_NBOUNDARY: values["nb"],
                RP_SBOUNDARY: values["sb"],
                RP_WBOUNDARY: values["wb"],
                RP_EBOUNDARY: values["eb"],
            }

            for k, v in rp_dict.items():
                d.text(k, v, fill="black", font=fntm)

            # TODO
            # if "M" in values["lunits"]:
            #     d.text(RP_MOMCOORDS, RP_MOMTEXT, fill="black", font=fntm)
            # else:
            #     with Image.open(values["clear_reason"]) as cr:
            #         out.paste(cr, RP_CLEARIMAGECOORDS)

            if event == 'rclear':
                with Image.open(values['clear_reason']) as cr:
                    out.paste(cr, RP_CLEARIMAGECOORDS)

            if values["rp_sketch"]:
                with Image.open(values["rp_sketch"]) as skt:
                    rskt = skt.resize(
                        (718 - 142, 866 - 310),
                    )
                    out.paste(rskt, (142, 310))
            outfile = out.save("rpfile.png")
        # except AttributeError:
        # pass

    if event == "raupdate":
        with Image.open(values["infile"]) as out:

            d = ImageDraw.Draw(out)

            ra_dict = {
                RA_NBOUNDARY: values["ranb"],
                RA_SBOUNDARY: values["rasb"],
                RA_WBOUNDARY: values["rawb"],
                RA_EBOUNDARY: values["raeb"],
            }

            for k, v in ra_dict.items():
                d.text(k, v, fill="black", font=fntm)

            if values["ra_sketch"]:
                with Image.open(values["ra_sketch"]) as skt:
                    out.paste(skt, (70, 294))

            outfile = out.save("rafile.png")

    if event == "bpupdate":
        with Image.open(values["infile"]) as out:

            d = ImageDraw.Draw(out)
            bp_dict = {
                BP_TOTALPAGES: str(values["bptp"]),
                BP_UNITS: values["blunits"],
                BP_NAMECOORDS: NAME,
                BP_DATECOORDS: str(DATE),
                BP_GUIDELINES: BP_TEXT,
            }
            if values["cable"]:
                d.text(BP_CABLE, BP_TEXT, fill="black", font=fntm)
            if values["conduit"]:
                d.text(BP_CONDUIT, BP_TEXT, fill="black", font=fntm)
            if values["cable"] == True or values["conduit"] == True:
                d.text(BP_PAINT, BP_TEXT, fill="black", font=fntm)
            for k, v in bp_dict.items():
                d.text(k, v, fill="black", font=fntm)
            for item in bell_stickers:
                if values[item] == True:
                    with Image.open(bell_stickers[item]["file"]) as sf:
                        out.paste(sf, (bell_stickers[item]["coords"]))

            outfile = out.save("bpfile.png")

    if event == "rp-display":
        window["img"].update(data=convert_to_bytes("rpfile.png"))

    elif event == "bp-display":
        window["img"].update(data=convert_to_bytes("bpfile.png"))

    elif event == "ra-display":
        window["img"].update(data=convert_to_bytes("rafile.png"))

    if event == "rpfilemove":
        move_files("rp", values["rpsavefile"])

    elif event == "bpfilemove":
        move_files("bp", values["bpsavefile"])

    elif event == "rafilemove":
        move_files("ra", values["rasavefile"])

window.close()
