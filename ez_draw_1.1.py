#locate draw v2
import base64
import io
import json
import logging
import pathlib
import pickle
import time
import constants
from enum import Enum
from typing import List, Tuple, Union

import PIL.Image
from PIL.Image import LANCZOS
import PySimpleGUI as sg

#use no globals in this program


#------------------
class Application:

    @staticmethod
    def init_settings():
        sg.theme('darkgray')
        sg.set_options(font=('Segoe UI',10,'normal'))

    @staticmethod
    def init_canvas():
        return Canvas()

    @staticmethod
    def init_tools():
        ...

    def init_menus():
        main_menu = Menu.create('Main',
        [
        ["File", ["Save", "Save template as...", "Load template", "Exit"]],
        ["Size", ["24", "30"]],
        ["Input", ["Mouse/Keyboard", "Keyboard"]],
        ])

    def init_ui():
        ...


    def main():
        ...

#------------------

class Canvas:


    def __init__(self):
        self.input_mode = "mouse"  # default to mouse input

    def switch_input_mode(self):
        if self.input_mode == "mouse":
            self.input_mode = "keyboard"
        else:
            self.input_mode = "mouse"
    ...

class KeyHandler:

    def __init__(self):
        if sg.running_linux():
            self.keys = {
                'esc':'Escape:9',
        'g':'g:42',
        'down':'Down:116',
        'up':'Up:111',
        'right':'Right:114',
        'left':'Left:113',
        'r':'r:27',
        'R':'R:27',
        'c':'c:54',
        'C':'C:54',
        's':'s:39',
        'd':'d:40',
        'w':'w:25',
        'a':'a:38',
        'e':'e:26',
        'E':'E:26',
        'q':'q:24',
        'z':'z:52',
        'x':'x:53',
        'f':'f:41',
        'v':'v:55',
        't':'t:28',
        'T':'T:28',
        'y':'y:29',
        'u':'u:30',
        'i':'i:31',
        'o':'o:32',
        'p':'p:33',
        'h':'h:43',
        'j':'j:44',
        'k':'k:45',
        'l':'l:46',
        'n':'n:57',
        'm':'m:58',
        'b':'b:56',
        'B':'B:56',
        'V':'V:55',
        '1':'1:10',
        '2':'2:11',
        '3':'3:12',
        '4':'4:13',
        '5':'5:14',
        '6':'6:15',
        '7':'7:16',
        '8':'8:17',
        '9':'9:18',
        '0':'0:19',
        '=':'equal:21',
        '_':'underscore:20',
        '>':'greater:60',
        'F1':'F1:67',
        'F2':'F2:68',
            }
        else:
            self.keys = {
        'esc':'Escape:27',
        'g':'g',
        'down':'Down:40',
        'up':'Up:38',
        'right':'Right:39',
        'left':'Left:37',
        'r':'r',
        'R':'R',
        'c':'c',
        'C':'C',
        's':'s',
        'd':'d',
        'w':'w',
        'a':'a',
        'e':'e',
        'E':'E',
        'q':'q',
        'z':'z',
        'x':'x',
        'f':'f',
        'v':'v',
        't':'t',
        'T':'T',
        'y':'y',

            }

    def get_key(self, event):
        return self.keys.get(event)

#-------------------

class Entity:
    ...


class Rectangle(Entity):
    ...


class Line(Entity):
    ...

class Text(Entity):
    ...


#------------------
class Tools:
    ...

class SelectTool(Tools):
    ...

class ThinLineTool(Tools):
    ...

class RoadTool(Tools):
    ...

class CableTool(Tools):
    ...

class SmallTextTool(Tools):
    ...

class LargeTextTool(Tools):
    ...

class MeasureTool(Tools):
    ...

#------------------
class UI:
    pass

class Menu(UI):

    def create(name,layout):
        return sg.Menu(layout, key=name)

class Tab(UI):

        def __init__(self, name, layout):
            self.name = name
            self.layout = layout

        def _create(self, name):
            return sg.Tab(self.layout, key=name)

class Dialogs(UI):
    ...

class StatusBar(UI):
    ...

class Toolbar(UI):
    ...

class Window(UI):
    ...


class Events:
    ...



if __name__ == '__main__':
    Application.main()
