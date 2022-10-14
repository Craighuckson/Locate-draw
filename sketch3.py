from io import FileIO
import sys
from PIL import Image, ImageDraw, ImageFont
import datetime
from collections import namedtuple
from form import get_teldig_data, get_form, save_bitmap

font14 = ImageFont.truetype("arial.ttf", 14)
font16 = ImageFont.truetype("arial.ttf", 16)
font10 = ImageFont.truetype("arial.ttf", 10)
font24 = ImageFont.truetype("arial.ttf", 24)
ffont = ImageFont.TransposedFont(font14, orientation=2)

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


def get_date() -> str:
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    return f"{year}-{month:02}-{day:02}"


def read_clear_sheet(f: FileIO) -> dict:
    ct = []
    with open(f, "r") as clearfile:
        for line in clearfile:
            line = line.replace("\n", "")
            ct.append(line)
    c = {
        "current_page": ct[0],
        "total_pages": ct[1],
        "units": ct[2],
        "type": ct[3],
        "north": ct[4],
        "south": ct[5],
        "west": ct[6],
        "east": ct[7],
        "file_name": ct[8],
    }
    del ct
    return c


rogers_clear: tuple = ()
aptum_clear: tuple = (241, 447, "No Aptum Fibre in Dig Area", font24)
envi_clear: tuple = ()

envi_prim_fixed: dict = {
    "units": (761, 96, "1C", font16),
    "north": (50, 254, "SOME ST", font14),
    "south": (448, 253, "SOME ST", font14),
    "west": (52, 281, "SOME ST", font14),
    "east": (449, 280, "SOME ST", font14),
    "paint": (96, 787, "x", font14),
    "property_line": (19, 750, "Property Line", font10),
    "road_edge": (20, 778, "Road Edge", font10),
    "pl": (115, 750, "PL", font10),
    "re": (90, 778, "RE", font10),
    "markfax": (546, 999, "x", font10),
    "name": (332, 962, "Craig Huckson", font16),
    "locator_id": (344, 996, "130003", font16),
    "date": (620, 975, get_date(), font16),
}

EP_VARIABLE:dict = {}

RP_FIXED: dict = {
    "units": (760, 95, "1C", font14),
    "north": (49, 235, "some at", font14),
    "south": (459, 233, "some st", font14),
    "west": (52, 263, "some st", font14),
    "east": (448, 263, "some st", font14),
    "totalpages": (775, 25, "1", font14),
    "property_line": (18, 752, "Property Line", font10),
    "road_edge": (18, 774, "Road Edge", font10),
    "pl": (110, 753, "PL", font14),
    "re": (111, 774, "RE", font14),
    "paint": (42, 818, "x", font10),
    "name": (332, 962, "Craig Huckson", font16),
    "locator_id": (344, 996, "130003", font16),
    "date": (620, 975, get_date(), font16),
}
RP_VARIABLE:dict = {}

aptum_prim: dict = {
    "units": (756, 90, "1C", font14),
    "north": (53, 252, "SOME ST", font14),
    "south": (450, 252, "SOME ST", font14),
    "west": (53, 284, "SOME ST", font14),
    "east": (450, 279, "SOME ST", font14),
    "property_line": (22, 742, "Property Line", font10),
    "road_edge": (22, 753, "Road Edge", font10),
    "pl": (116, 737, "PL", font14),
    "re": (100, 757, "RE", font14),
    "paint": (93, 792, "x", font10),
    "name": (332, 965, "Craig Huckson", font16),
    "locator_id": (346, 991, "130003", font16),
    "date": (616, 963, get_date(), font16),
}


# with Image.open('aptumprim.bmp') as im:
#     draw = ImageDraw.Draw(im)

#     for item in aptum_prim.values():

#     draw.text((item[0], item[1]), item[2], fill=(0, 0, 0), font=item[3])
#     draw.text(
#       (aptum_clear[0], aptum_clear[1]),
#       aptum_clear[2], fill=(0,0, 0),font=aptum_clear[3]
#      )
#     im.resize((im.width, im.height), Image.NEAREST)
#     im.show()
if __name__ == "__main__":

    # READ TELDIG DATA, CLEAR SHEET
    #GET TICKET NUMBER, FORM, UNITS, DIG AREA, CLEAR WARNING - THESE ARE VARIABLE DATA

    td:dict = get_teldig_data()
    tkt_num:str = td["ticket_number"]
    cs:dict = read_clear_sheet(f'{tkt_num}-1.txt')
    form:str = get_form(td["station_code"], cs["current_page"])

    units:int = cs["units"]

    with Image.open("temp.bmp") as im:
        draw = ImageDraw.Draw(im)
        # units
