# TODO - page numbers, dig area, dig area

import datetime
import subprocess
import webbrowser
from collections import namedtuple


Point = namedtuple("Point", "x y")
Rect = namedtuple("Rect", ["ulx", "uly", "lrx", "lry"])

envi_prim: dict = {
    "units": Point(761, 106),
    "north": Point(50, 269),
    "south": Point(448, 268),
    "west": Point(52, 291),
    "east": Point(449, 290),
    "paint": Point(96, 797),
    "sketchwin": Rect(150, 325, 790, 880),
    "size": (640, 555),
    "sketch_width": 640,
    "sketch_height": 555,
    "property_line": Point(19, 760),
    "road_edge": Point(20, 788),
    "pl": Point(115, 760),
    "re": Point(90, 788),
    "markfax": Point(546, 1009),
    "name": Point(332, 972),
    "locator_id": Point(344, 1006),
    "date": Point(620, 985),
}


class SketchDraw:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def start(self):
        return f"viewbox 0 0 {self.width} {self.height}\n"

    def horizontal_text(self, coords:Point, msg: str, font: int = 12) -> str:
        output: list = []
        output.append("push graphic-context")
        output.append(f"font-size {font} fill black stroke-width 1")
        output.append(f'text {coords.x} {coords.y} "{msg}"')
        output.append("pop graphic-context")
        return "\n".join(output)

    def vertical_text(self, x: int, y: int, msg: str, *, font: int = 12) -> str:
        output: list = []
        output.append("push graphic-context")
        output.append(f"font-size {font} fill black stroke-width 1")
        output.append(f"translate {x} {y}")
        output.append("rotate 90")
        output.append(f'text 0 0 "{msg}"')
        output.append("pop graphic-context")
        return "\n".join(output)

    def get_date(self) -> str:
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        return f"{year}-{month:02}-{day}"

    def rogers_envi_primary(self) -> str:
        output: list = []
        # left side text
        ep = envi_prim
        output.append("push graphic-context")
        output.append(
            "font-size 9 font Arial font-style normal fill black stroke-width 1 stroke-antialias 0"
        )
        output.append(f'text {ep["property_line"].x} {ep["property_line"].y} "Property Line"')
        output.append(f'text {ep["road_edge"].x} {ep["road_edge"].y} "Road Edge"')
        output.append(f'text {ep["markfax"].x} {ep["markfax"].y} "x"')
        output.append("font-size 12")
        output.append(f'text {ep["pl"].x} {ep["pl"].y} "PL"')
        output.append(f'text {ep["re"].x} {ep["re"].y} "RE"')
        output.append("font-size 18")
        output.append(f'text {ep["name"].x} {ep["name"].y} "Craig Huckson"')
        output.append(f'text {ep["locator_id"].x} {ep["locator_id"].y} "130003"')
        # insert date
        output.append(f'text {ep["date"].x} {ep["date"].y} "{str(self.get_date())}"')
        output.append("pop graphic-context")
        return "\n".join(output)

    def some_tet(coords:Point,msg:str):
        return coords + msg


if __name__ == "__main__":
    s = SketchDraw(816, 1056)
    #with open("test.mvg", "w") as envtest:
        #envtest.write(s.rogers_envi_primary())
    print(envi_prim["north"])
        #envtest.write(s.horizontal_text(f'{**envi_prim["north"]} "SOME DIG AREA"'))
    #subprocess.run("magick enviprimdemo.bmp -draw @test.mvg result.png")
    #webbrowser.open("result.png")
