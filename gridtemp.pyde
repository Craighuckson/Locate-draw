

def setup():
    size(600,600)
    background(255)
    global grid
    grid = createGraphics(600,600)
    fill(0)

def drawGrid():
    
    grid.beginDraw()
    grid.stroke(80)
    for x in range(0, width, 20):
        for y in range(0, height,20):
            grid.point(x,y)
    grid.endDraw()
    image(grid,0,0)
    
def drawDot(x,y):
    pushMatrix()
    stroke(255,0,0)
    circle(x,y,5)
    popMatrix()
            
def mouseMoved():
    print(mouseX,mouseY)
    
def mouseClicked():
    t = '(%s, %s)' % (mouseX,mouseY)
    fill(0)
    text(t,mouseX,mouseY)
    drawDot(mouseX,mouseY)

def draw():
    drawGrid()
    
def keyPressed():
    if (key == 'c'):
        grid.clear()
        background(255)
        drawGrid()
    
    

    
    
