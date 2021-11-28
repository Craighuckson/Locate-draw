def push():
    pushMatrix()
    
def pop():
    popMatrix()

def road(x1,y1,x2,y2):
    push()
    stroke(0)
    strokeWeight(3)
    line(x1*20,y1*20,x2*20,y2*20)
    pop()

def digbox(ulx,uly,lrx,lry):
    push()
    ulx,uly,lrx,lry = ulx*20, uly*20,lrx*20,lry*20
    strokeWeight(1.5)
    fill(170,40)
    rectMode(CORNERS)
    stroke(0)
    if (lry == height):
        lry = lry - 2            
    rect(ulx,uly,lrx,lry)
    pop()
    
def draw_grid():
    push()
    stroke(200)
    textAlign(CENTER,CENTER)
    for i in range(0,width,20):
        line(i,0,i,height)
    for j in range(0,height,20):
        line(0,j,width,j)
    fill(0)
    strokeWeight(1)
    for k in range(0,width,40):
        x = k/20
        text(x,k,10)
    for l in range(0,height,40):
        y = l/20
        text(y,10,l)
    pop()

#text
def htext(string,x,y,font):
    x = x*20
    y = y*20
    push()
    textAlign(CENTER,CENTER)
    fill(0)
    textSize(font)
    text(string,x,y)
    pop()

def vtext(string,x,y,font):
    x = x*20
    y = y*20
    push()
    textAlign(CENTER,CENTER)
    fill(0)
    textSize(font)
    pushMatrix()
    translate(x,y)
    rotate(-HALF_PI)
    text(string,0,0)
    popMatrix()
    pop()
    
                
#buildings
    
def ped(x,y):
    x = x * 20
    y = y * 20
    push()
    fill(255)
    stroke(0)
    strokeWeight(1)
    p = createShape(GROUP)
    r = createShape(RECT,0,0,15,15)
    b1 = createShape(LINE,0,0,15,15)
    b2 = createShape(LINE,0,15,15,0)
    p.addChild(r)
    p.addChild(b1)
    p.addChild(b2)
    shape(p,x-7,y-7)
    pop()
    
def pole(x,y):
    x = x*20
    y = y*20
    push()
    fill(255)
    stroke(0)
    strokeWeight(1.5)
    ellipseMode(CENTER)
    circle(x,y,15)
    pop()
    
def nArrow(x,y):
    x = x*20
    y = y*20
    stroke(0)
    fill(0)
    strokeWeight(1)
    triangle(x,y,x-5,y+10,x+5,y+10)
    line(x,y+10,x,y+30)

def sArrow(x,y):
    x = x*20
    y = y*20
    push()
    translate(x,y)
    rotate(PI)
    nArrow(0,0)
    pop()
    
def eArrow(x,y):
    x = x*20
    y = y*20
    push()
    translate(x,y)
    rotate(HALF_PI)
    nArrow(0,0)
    pop()
    
def wArrow(x,y):
    x = x*20
    y = y*20
    push()
    translate(x,y)
    rotate(-HALF_PI)
    nArrow(0,0)
    pop()

def mHouse(num,x,y):
    x = x * 20
    y = y * 20
    push()
    textAlign(CENTER,CENTER)
    stroke(0)
    fill(255)
    strokeWeight(1)
    translate(x,y)
    rect(0,0,80,80)
    fill(0)
    strokeWeight(0)
    textSize(16)
    text(num,40,40)
    textSize(10)
    fill(0)
    stroke(0)
    text('NBL',40,7)
    text('SBL',40,73)
    translate(7,40)
    rotate(-HALF_PI)
    text('WBL',0,0)
    text('EBL',0,66)
    pop()
    
