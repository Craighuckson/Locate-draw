add_library('UiBooster')
add_library('dashedlines')

def setup():
    global dash, f, s, dir
    dash = DashedLines(this)
    dash.pattern(5,10)
    size(600,600)
    background(255)
    rectMode(CORNERS)
    #fontlist = PFont.list()
    #print(PFont.list()) 
    s = UiBooster().showTextInputDialog('Enter street name')
    dir = UiBooster().showSelectionDialog(
        "Choose landbase",
        "Landbase",["N", "W", "E", "S"])

def draw_cable(x1,y1,x2,y2):
    global dash
    strokeWeight(2)
    dash.line(x1,y1,x2,y2)
    
def drawCurb(dir):
        strokeWeight(3)
        if dir == 'E':
            line(width * .75, 0, width * .75, height)
        elif dir == 'W':
            line(width * .25, 0, width * .25, height)
        elif dir == 'N':
            line(0, height * 0.25, width, height * 0.25)
        else:
            line(0, height * 0.75, width, height * 0.75)             
    
def draw():   
    global s
    #textFont(f)
    fill(0)
    pushMatrix()
    translate(width*.9,height*0.4)
    rotate(radians(90))
    textSize(20)
    text(s, 0,0)
    popMatrix()
    drawCurb(dir)
    
def keyPressed():
    global dash
    if key == '1':
        draw_cable(mouseX,0,mouseX,height)
    if key == 'u':
        background(255)
    if key == 'm':
        triangle(mouseX,mouseY,mouseX+3,mouseY-3,mouseX+3,mouseY+3)
        strokeWeight(1)
        line(mouseX+3, mouseY, mouseX+25, mouseY)
