import datetime
from inspect import Attribute
import PySimpleGUI as sg
import PIL
from PIL import ImageGrab, ImageFont
from PIL import ImageDraw, Image
import io
import base64

from PySimpleGUI.PySimpleGUI import BUTTON_TYPE_READ_FORM, WIN_CLOSED

d = datetime.datetime.now()

#CONSTANTS
RPSIZE = (816,1056)
TOTALPAGES = (776,20)
UNITS = (765,105)
MFONT = 'Arial 12 normal'
LFONT = 'Arial 20 normal'
NBOUNDARY = (51,243)
SBOUNDARY = (449,244)
WBOUNDARY = (55,276)
EBOUNDARY = (449,274)
DATE = str('/'.join([d.strftime(x) for x in ['%Y', '%m', '%d']]))
NAME = 'CRAIG HUCKSON'
NAMECOORDS = (340,967)
LOCATORID = 130003
LOCATORIDCOORDS = (341,1003)
DATECOORDS = (620,967)
MOMTEXT = 'x'
MOMCOORDS = (40,810)
MEMAILTEXT = 'x'
MEMAILCOORDS = (544,1002)
CLEARIMAGECOORDS = (428,536)
rogclear = {'reg_clear':'rogclear.PNG','ftth':'ftthstamp.PNG','fo_only':'exclusion.PNG'}

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

lcol = [
    [sg.Text('Choose form:'),sg.I(k='infile',enable_events=True),sg.FileBrowse()],
    [sg.Text('Total pages: '), sg.Input(s=5,key='tp'),sg.Text('Units: '), 
    sg.Input(size=5,k='lunits')],
    [sg.Text('North Boundary: '), sg.Input(enable_events=True,key='nb')],
    [sg.Text('South Boundary: '), sg.Input(enable_events=True,key='sb')],
    [sg.Text('West Boundary: '), sg.Input(enable_events=True,key='wb')],
    [sg.Text('East Boundary: '), sg.Input(enable_events=True,key='eb')],
    [sg.Radio('Marked',group_id='mc',default=True,k='rmarked',enable_events=True), sg.Radio('Clear',group_id='mc', k='rclear',enable_events=True),sg.Text('Clear reason:'),
     sg.Combo(values=[rogclear['reg_clear'],rogclear['ftth'],rogclear['fo_only']], default_value=rogclear['reg_clear'],enable_events=True, k='clear_reason', visible=False)],
    [sg.B('Update',BUTTON_TYPE_READ_FORM),sg.Button('Display')]
]

rcol = [[sg.Image(size=(640,480),expand_y=True,key='img')]]

layout = [[sg.Column(lcol), sg.Column(rcol,scrollable=True,vertical_scroll_only=True,expand_x=True,expand_y=True)]]
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
    # shows stuff in right column
    if event == 'infile':
        window['img'].update(data=convert_to_bytes(values['infile']))
    if event == 'rclear':
        window['clear_reason'].update(visible=True)
    elif event == 'rmarked':
        window['clear_reason'].update(visible=False)
    if event == 'Update':
        #this writes in the dig area and other shiT
        with Image.open(values['infile']) as out:
            fntm = ImageFont.truetype('arialbd.ttf',size=12)
            fntl = ImageFont.truetype('arialbd.ttf',size=16)
            d = ImageDraw.Draw(out)
            tdict = {
            TOTALPAGES:str(values['tp']),
            UNITS:values['lunits'],
            NBOUNDARY:values['nb'],
            SBOUNDARY:values['sb'],
            WBOUNDARY:values['wb'],
            EBOUNDARY:values['eb'],
            NAMECOORDS:NAME,
            DATECOORDS:str(DATE),
            MEMAILCOORDS:MEMAILTEXT,
            LOCATORIDCOORDS:str(LOCATORID)
                    }

            for k,v in tdict.items():
                d.text(k, v, fill='black', font=fntm)
            if 'M' in values['lunits']:
                d.text(MOMCOORDS,MOMTEXT,fill='black',font=fntm)
            else:
                with Image.open(values['clear_reason']) as cr:
                    out.paste(cr,CLEARIMAGECOORDS)
            outfile = out.save('file.png')
        #except AttributeError:
            #pass
    if event == 'Display':
        window['img'].update(data=convert_to_bytes('file.png'))

window.close()