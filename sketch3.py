from io import FileIO
import sys
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
import datetime
from collections import namedtuple
from form import get_teldig_data, get_form, save_bitmap

FONT14 = ImageFont.truetype("arial.ttf", 14)
FONT16 = ImageFont.truetype("arial.ttf", 16)
FONT10 = ImageFont.truetype("arial.ttf", 10)
FONT24 = ImageFont.truetype("arial.ttf", 24)
FFONT = ImageFont.TransposedFont(FONT14, orientation=2)

"""
steps

want a clear locate sketch generated - end goal

    - get all info needed for paperwork (
        which form, page #, dig area, which warning, date etc)
    - get proper form - utility primary or secondary -
        can do this by reading station code and knowing what page - PARTIAL
    - other info captured by ahk and sent to text file (
        page numbers, dig area, warnings)
    - get date - DONE

- get blank form
    - in python? need to open sketchtool, export, save as bmp if primary sheet

- open blank version of correct form

- put info to form
    - using PIL
    - each item has coordinate , get text from list imported in first step

- load form into teldig - insert image - should be whole - very fast

"""

Rect = namedtuple("Rect", ["ulx", "uly", "lrx", "lry"])
sample = []


def get_filename(prompt:str) -> str:
    # Define the PySimpleGUI layout for the file selection dialog
    layout = [
        [sg.Text(prompt)],
        [sg.Input(key='file'), sg.FileBrowse()],
        [sg.Button('OK'), sg.Button('Cancel')]
    ]

    # Create the PySimpleGUI window
    window = sg.Window('Open File', layout)

    # Loop until the user closes the window or clicks the OK or Cancel button
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            # User closed the window or clicked the Cancel button
            window.close()
            return None

        if event == 'OK':
            # User clicked the OK button, return the selected file name
            file_name = values['file']
            window.close()
            return file_name

def get_date() -> str:
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    return f"{year}-{month:02}-{day:02}"

def read_clear_sheet(f: FileIO) -> dict:
    c = {}
    with open(f, "r") as clearfile:
        c["current_page"] = clearfile.readline().rstrip("\n")
        c["total_pages"] = clearfile.readline().rstrip("\n")
        c["units"] = clearfile.readline().rstrip("\n")
        c["type"] = clearfile.readline().rstrip("\n")
        c["north"] = clearfile.readline().rstrip("\n")
        c["south"] = clearfile.readline().rstrip("\n")
        c["west"] = clearfile.readline().rstrip("\n")
        c["east"] = clearfile.readline().rstrip("\n")
        c["file_name"] = clearfile.readline().rstrip("\n")
    return c

# function add_data_to_ticket. Using PIL, open ticket, write text on image using data from RP_FIXED tuples , save as "output.png"

def add_data_to_ticket(ticket: str, clearsheet_data: dict) -> None:
    # open ticket
    with Image.open(ticket) as im:
        draw = ImageDraw.Draw(im)
        # write text on image
        for key, value in RP_FIXED.items():
            draw.text(value, clearsheet_data[key], font=value[3])
        # save as output.png
        im.save("output.png")

rogers_clear: tuple = (241, 447, "NO ROGERS IN DIG AREA", FONT24)
aptum_clear: tuple = (241, 447, "NO APTUM FIBRE IN DIG AREA", FONT24)
envi_clear: tuple = ()

envi_prim_fixed: dict = {
    "units": (761, 96, FONT16),
    "north": (50, 254, "SOME ST", FONT14),
    "south": (448, 253, "SOME ST", FONT14),
    "west": (52, 281, "SOME ST", FONT14),
    "east": (449, 280, "SOME ST", FONT14),
    "paint": (96, 787, "x", FONT14),
    "property_line": (19, 750, "Property Line", FONT10),
    "road_edge": (20, 778, "Road Edge", FONT10),
    "pl": (115, 750, "PL", FONT10),
    "re": (90, 778, "RE", FONT10),
    "markfax": (546, 999, "x", FONT10),
    "name": (332, 962, "Craig Huckson", FONT16),
    "locator_id": (344, 996, "130003", FONT16),
    "date": (620, 975, get_date(), FONT16),
}

EP_VARIABLE:dict = {}

rogers_primary = {
    "units": {"x": 760, "y": 95, "text": "", "font": FONT14},
    "north": {"x": 49, "y": 235, "text": "", "font": FONT14},
    "south": {"x": 459, "y": 233, "text": "", "font": FONT14},
    "west": {"x": 52, "y": 263, "text": "", "font": FONT14},
    "east": {"x": 448, "y": 263, "text": "", "font": FONT14},
    "totalpages": {"x": 775, "y": 25, "text": "", "font": FONT14},
    "property_line": {"x": 18, "y": 752, "text": "Property Line", "font": FONT10},
    "road_edge": {"x": 18, "y": 774, "text": "Road Edge", "font": FONT10},
    "pl": {"x": 110, "y": 753, "text": "PL", "font": FONT14},
    "re": {"x": 111, "y": 774, "text": "RE", "font": FONT14},
    "paint": {"x": 42, "y": 818, "text": "x", "font": FONT10},
    "name": {"x": 332, "y": 962, "text": "Craig Huckson", "font": FONT16},
    "locator_id": {"x": 344, "y": 996, "text": "130003", "font": FONT16},
    "date": {"x": 620, "y": 975, "text": get_date(), "font": FONT16},
}

RP_VARIABLE:dict = {}

aptum_prim: dict = {
    "units": (756, 90, "1C", FONT14),
    "north": (53, 252, "SOME ST", FONT14),
    "south": (450, 252, "SOME ST", FONT14),
    "west": (53, 284, "SOME ST", FONT14),
    "east": (450, 279, "SOME ST", FONT14),
    "property_line": (22, 742, "Property Line", FONT10),
    "road_edge": (22, 753, "Road Edge", FONT10),
    "pl": (116, 737, "PL", FONT14),
    "re": (100, 757, "RE", FONT14),
    "paint": (93, 792, "x", FONT10),
    "name": (332, 965, "Craig Huckson", FONT16),
    "locator_id": (346, 991, "130003", FONT16),
    "date": (616, 963, get_date(), FONT16),
}


def main():
    ticket = get_filename("Select Ticket File")
    if ticket is None:
        sys.exit()
    clearsheet = get_filename("Select Clearsheet File")
    if clearsheet is None:
        sys.exit()
    # get clearsheet data
    clearsheet_data = read_clear_sheet(clearsheet)
    add_data_to_ticket(ticket, clearsheet_data)
    #show a message that it is done
    sg.popup_ok("Ticket saved to file", title="Done")



    
    


if __name__ == "__main__":

    # READ TELDIG DATA, CLEAR SHEET
    #GET TICKET NUMBER, FORM, UNITS, DIG AREA, CLEAR WARNING - THESE ARE VARIABLE DATA


    with Image.open("temp.bmp") as im:
        draw = ImageDraw.Draw(im)
        # units
