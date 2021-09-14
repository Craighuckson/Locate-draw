
def setup():
    background(255)
    size(600,600)
    stroke(255,0,0)
    fill(255,0,0)
    rect(570,0,30,30)

def draw():
    stroke(0)
    line(0,40,200,40)

def mouseClicked():
    if (570 < mouseX < 600) and (mouseY <= 30):
        fill(0,255,0)
        circle(200,200,10)