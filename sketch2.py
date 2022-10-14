import PySimpleGUI as sg
import PIL.Image
import io
import base64

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

class App:

    file_chosen: str = ""
    __want_saved: str = ""


layout = [
    [
        sg.Graph(
            canvas_size=(800, 600),
            graph_bottom_left=(0, 600),
            graph_top_right=(800, 0),
            background_color="white",
            key="graph",
            pad=10,
            enable_events=True
        )
    ]
]
a = App()
print(a.file_chosen)
window = sg.Window(
    "Sketch",
    layout,
    finalize=True,
    return_keyboard_events=True,
    resizable=True,
)

graph = window["graph"]
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "q":
        break
    if event == "t":
        pass
    if event == "i":
        img = sg.popup_get_file('Image?')
        try:
            im = sg.Graph.draw_image(graph, location=(0, 0),  data=convert_to_bytes(img))
        except:
            print('Could not open image')
    if event == "l":
        graph.draw_line((0, 100), (400, 100), color="green", width=1.5)
    if event == "e":
        sg.Graph.draw_line(graph, (0, 100), (400, 100), color="white", width=1.5)
    if event == "s":
        App.__want_saved = sg.popup_yes_no("Save picture?")
        if App.__want_saved == "Yes":
            sg.popup("Unfortunately I cant do that yet")

window.close()
