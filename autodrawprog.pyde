#todo

#test constants

form = 'BELLAUXILLIARY.png'
font_size = 16
date = '2021-06-28'
ba_date_x = 15
ba_date_y = 90
sizex = 816
sizey = 1056

#load background form - bell auxilliary catv auxilliary
def setup():
    fullScreen()
    global f,baform
    baform = loadImage(form)
    f = createFont("Arial", font_size, True)
    #image(baform,0,0,500,500)

#write dig area
#
def draw():
    pushMatrix()
    scale(0.7)
    translate(400,0)
    image(baform,0,0)
    textFont(f)
    fill(0)
    text(date, ba_date_x, ba_date_y)
    text('NCL SOME ST', 80,260)
    popMatrix()
