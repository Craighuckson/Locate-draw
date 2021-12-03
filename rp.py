import datetime
import PySimpleGUI as sg
from PIL import ImageGrab, ImageFont
from PIL import ImageDraw, Image
import io
import base64

from PySimpleGUI.PySimpleGUI import BUTTON_TYPE_READ_FORM, WIN_CLOSED

d = datetime.datetime.now()

#CONSTANTS
RPSIZE = (816,1056)
TOTALPAGES = (776,27)
UNITS = (765,105)
MFONT = 'Arial 12 normal'
LFONT = 'Arial 20 normal'
NBOUNDARY = ((12+243)/2, (229+258)/2)
SBOUNDARY = ((424+802)/2, (228+260)/2)
WBOUNDARY = ((12+243)/2, (259+290)/2)
EBOUNDARY = ((424+802)/2, (258+288)/2)
DATE = '/'.join([d.strftime(x) for x in ['%Y', '%m', '%d']])
NAME = 'Craig Huckson'
NAMECOORDS = (409,967)
DATECOORDS = (700,973)
MOMTEXT = 'x'
MOMCOORDS = (39,820)
MEMAILTEXT = 'x'
MEMAILCOORDS = (544,1008)

#FUNCTIONS

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

def save_element_as_file(element, filename):
    """
    Saves any element as an image file.  Element needs to have an underlyiong Widget available (almost if not all of them do)
    :param element: The element to save
    :param filename: The filename to save to. The extension of the filename determines the format (jpg, png, gif, ?)
    """
    try:
        widget = element.Widget
        box = (widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height())
        grab = ImageGrab.grab(bbox=box)
        grab.save(filename)
    except:
        print('couldnt save')

lcol = [
    [sg.Text('Choose form:'),sg.I(k='infile'),sg.FileBrowse()]
    [sg.Text('Total pages: '), sg.Input(s=5,key='tp'),sg.Text('Units: '), 
    sg.Input(size=5,k='lunits')],
    [sg.Text('North Boundary: '), sg.Input(enable_events=True)],
    [sg.Text('South Boundary: '), sg.Input(enable_events=True)],
    [sg.Text('West Boundary: '), sg.Input(enable_events=True)],
    [sg.Text('East Boundary: '), sg.Input(enable_events=True)],
    [sg.B('Update',BUTTON_TYPE_READ_FORM)]
]

rcol = [[sg.Image(size=(640,480),expand_y=True,key='img')]]

layout = [[sg.Column(lcol), sg.Column(rcol)]]
#tp = input('Total pages: ')
#lunits = input('Units? ')
#nbound = input('North boundary?')
#sbound = input('South boundary?')
#wbound = input('West boundary? ')
#ebound = input('East boundary? ')
#clearmsg = input('Clear message? ')

window = sg.Window('Locate form filler', layout, resizable=True,grab_anywhere=True, finalize=True)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Update':
        try:
            out = Image.new('RGB', (856,1056), color='white')
            fntm = ImageFont.truetype('Arial.ttf',12)
            d = ImageDraw.Draw(out)
            d.text(anchor='mm',xy=())
        except:
            pass
window.close()