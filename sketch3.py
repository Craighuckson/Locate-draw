from io import FileIO
import sys
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
import datetime

FONT14 = ImageFont.truetype("arial.ttf", 14)
FONT16 = ImageFont.truetype("arial.ttf", 16)
FONT10 = ImageFont.truetype("arial.ttf", 10)
FONT24 = ImageFont.truetype("arial.ttf", 24)
FFONT = ImageFont.TransposedFont(FONT14, orientation=2)


def get_filename(prompt:str) -> str:
    """
    Displays a file dialog window with the given prompt and returns the selected file name.

    Parameters:
        prompt (str): The prompt to display in the file dialog window.

    Returns:
        str: The selected file name, or None if the user cancels the dialog.

    Raises:
        None
    """
    layout = [[sg.Text(prompt)],
                [sg.Input(k='file'), sg.FileBrowse(file_types=(("Bitmap", "*.bmp"), ("JPEG", "*.jpg"), ("PNG", "*.png"), ("Text", "*.txt")))],
                [sg.OK(), sg.Cancel()]]
    
    window = sg.Window('Open File', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return None

        if event == 'OK':
            file_name = values['file']
            window.close()
            return file_name
        

def get_date() -> str:
    """
    Returns the current date in the format "YYYY-MM-DD".

    Parameters:
        None

    Returns:
        str: The current date in the format "YYYY-MM-DD".

    Raises:
        None
    """
    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    return f"{year}-{month:02}-{day:02}"


def read_clear_sheet(f: FileIO) -> dict:
    """
    Reads text file containing data to fill out a clear locate form and returns a dictionary containing its contents.

    Parameters:
        f (FileIO): A file-like object representing the text file.

    Returns:
        dict: A dictionary containing the contents of the clear sheet file.

    Raises:
        None
    """
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


def complete_dict_from_clearsheet(clearsheet_data: dict, utility_data: dict) -> None:
    """
    Updates the  utility_data dictionary with values from the `clearsheet_data` dictionary.

    For each key in `clearsheet_data`, if the key is also present in  utility_data`, the corresponding value in  utility_data` is updated with the value from `clearsheet_data`.
    If the key is not present in  utility_data`, it is ignored.

    Parameters:
        clearsheet_data (dict): A dictionary containing data from a clear sheet.
     utility_data (dict): A dictionary containing form data.

    Returns:
        None

    Raises:
        None
    """
    for key, value in clearsheet_data.items():
        form_field = utility_data.get(key)
        if form_field is not None:
            form_field["text"] = value
        else:
            #disregard the key
            pass


def add_image_to_image(existing: Image, incoming_filename: str, x: int, y: int) -> Image:
    """
    Pastes an incoming image onto an existing image at the specified x and y coordinates.

    Parameters:
        existing (Image): The image to paste onto.
        incoming (Image): The image to paste.
        x (int): The x coordinate to paste the incoming image.
        y (int): The y coordinate to paste the incoming image.

    Returns:
        Image: The modified existing image with the incoming image pasted onto it.

    Raises:
        None
    """
    with Image.open(incoming_filename) as incoming:
        existing.paste(incoming, (x, y))
    return existing


def handle_clear_type(clear_type:str) -> str:
    clear_type = int(clear_type)
    if clear_type == 1:
        return "msg"
    elif clear_type == 2:
        return "ftth"
    elif clear_type == 3:
        return "foonly"


def add_items_to_image(ticket: str, utility: dict) -> None:
    # open ticket
    with Image.open(ticket) as im:
        draw = ImageDraw.Draw(im)
        ct = handle_clear_type(utility["type"])
        if ct == "msg":
            #write on image using rogers_clear tuple
            draw.text(rogers_clear[0:2], rogers_clear[2], font=rogers_clear[3])
        elif ct == "ftth":
            add_image_to_image(im, "ftth.png", rogers_clear[0], rogers_clear[1])
        elif ct == "foonly":
            add_image_to_image(im, "foonly.png", rogers_clear[0], rogers_clear[1])
        

rogers_clear: tuple = (241, 447, "NO ROGERS IN DIG AREA", FONT24)
aptum_clear: tuple = (241, 447, "NO APTUM FIBRE IN DIG AREA", FONT24)
envi_clear: tuple = ()

ENVI_PRIMARY: dict = {
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

ROGERS_PRIMARY = {
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


APTUM_PRIMARY: dict = {
    "units": (756, 90, "", FONT14),
    "north": (53, 252, "", FONT14),
    "south": (450, 252, "", FONT14),
    "west": (53, 284, "", FONT14),
    "east": (450, 279, "", FONT14),
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
    complete_dict_from_clearsheet(clearsheet_data, ROGERS_PRIMARY)
    #add_items_to_image(ticket, clearsheet_data)
    #show a message that it is done
    sg.popup_ok("Ticket saved to file", title="Done")


if __name__ == "__main__":

    # READ TELDIG DATA, CLEAR SHEET
    #GET TICKET NUMBER, FORM, UNITS, DIG AREA, CLEAR WARNING - THESE ARE VARIABLE DATA
    main()
