add_library('dashedlines')

from functions import *

sq = int(20)

def setup():
    size(600,600)
    background(255)
    global dash
    dash = DashedLines(this)
    dash.pattern(10,10)
    shapeMode(CENTER)
    imageMode(CENTER)
    noLoop()

def cable(x1,y1,x2,y2):
    stroke(0)
    strokeWeight(2)
    strokeCap(ROUND)
    dash.line(x1,y1,x2,y2)
        
def draw():
    #grid
    # strokeWeight(1)
    # stroke(200)
    # for i in range(0,width,20):
    #     line(i,0,i,height)
    # for j in range(0,height,20):
    #     line(0,j,width,j)
    smooth() 
    #test
    #draw_grid()
    road(400,0,400,height)
    vtext('A COOL ST',(400+width)/2,640/2,24) #passed
    cable(300,0,300,height) #passed
    cable(300,160,340,160)
    cable(300,240,400,240)
    digbox(40,40,400,height)
    ped(17*sq,15*sq)
    htext('LOCATED AREA',160,120,16)
    strokeWeight(3)
    fill(255,0)
    arc(400,320,80,80,0,radians(45))
    pole(340,160)
    
    
def north_arrow():
    arrow = createShape(GROUP)
