def road(x1,y1,x2,y2):
    stroke(0)
    strokeWeight(3)
    line(x1,y1,x2,y2)

def digbox(ulx,uly,lrx,lry):
    strokeWeight(1)
    fill(170,20)
    rectMode(CORNERS)
    stroke(0)
    rect(ulx,uly,lrx,lry)
    
def draw_grid():
    stroke(200)
    textAlign(CENTER,CENTER)
    for i in range(0,width,20):
        line(i,0,i,height)
    for j in range(0,height,20):
        line(0,j,width,j)
    fill(0)
    strokeWeight(1)
    for k in range(0,width,40):
        text(k,k,10)
    for l in range(0,height,40):
        text(l,10,l)

#text
def htext(string,x,y,font):
    pushMatrix()
    fill(0)
    textSize(font)
    text(string,x,y)
    popMatrix()

def vtext(string,x,y,font):
    fill(0)
    textSize(font)
    pushMatrix()
    translate(x,y)
    rotate(-HALF_PI)
    text(string,0,0)
    popMatrix()
    
                
#buildings

def m_house(num,x,y):
    pass
    
def ped(x,y):
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
    
def pole(x,y):
    fill(255)
    stroke(0)
    strokeWeight(1.5)
    ellipseMode(CENTER)
    circle(x,y,15)

    
    
