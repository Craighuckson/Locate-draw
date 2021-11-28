add_library('UiBooster')
add_library('dashedlines')

from functions import *

presses = 0
pointlist = []
log = []

sq = int(20)


def setup():
    #size(600,600)
    size(480,480)
    background(255)
    shapeMode(CENTER)
    imageMode(CENTER)
    
    #init
    global dash,ui
    ui = UiBooster()
    dash = DashedLines(this)
    dash.pattern(10,5)
    
    #curb = {'x1': 1, 'y1': int(30*.66), 'x2': 29,'y2': (30*.66)}
    
    #npl to pl
    '''
    curb = [0,18,24,18]
    curblabel = 'NCL'
    cllocation = [1,17]
    streettext = [12,21]
    digarea = [0,0,24,12]
    street = "LAWSON ST"
    lastamp = [12,10]
    h1  = [2,4]
    h2 = [18,4]
    hnum1 = 1432
    hnum2 = 1362
    '''

    
    #wpl to pl
    
    curb = [18,0,18,24]
    curblabel = 'WCL'
    cllocation = [17,23]
    streettext = [21,12]
    digarea = [0,0,12,24]
    street = "HARDY WAY"
    lastamp = [6,12]
    h1 = [4,4]
    h2 = [4,18]
    hnum1 = 'L87'
    hnum2 = 'L82'
    
    
    #draw_grid()
    '''
     routine for drawing pl to pl for bell
    road(curb[0],curb[1],curb[2],curb[3])
    road(18,1,18,10)
    vtext(street, streettext[0], streettext[1],20)
    digbox(digarea[0], digarea[1], digarea[2], digarea[3])
    vtext(curblabel,cllocation[0],cllocation[1],12)
    vtext(,,,)
    mHouse(hnum1,h1[0],h1[1])
    mHouse(hnum2,h2[0],h2[1])
    htext('LOCATED AREA CLEAR OF BELL',lastamp[0],lastamp[1],12)
    #vtext(,,,)
    '''
    #
    #s pl to pl 1 cable
    
    htext('2ND LINE',12,2,20)
    htext('SRE',21,3,10)
    htext('1B',10,7,14)
    for x in (3,15):
        vtext('3.0m',x,6,12)
    digbox(0,4,24,24)
    mHouse('1109',10,18)
    road(0,4,width/20,4)
    cable(0,8,24,8)
    cable(5,12,5,8)
    ped(5,12)
    sArrow(3,4)
    sArrow(15,4)
    nArrow(3,8)
    nArrow(15,8)
    htext('LOCATED AREA',12,11,13)
    
    
    #wpl to pl
    
    file = ui.showTextInputDialog('Save file name?')
    try:
        ufile = file.upper()
    except:
        pass
    if not file:
        pass
    else:
        save(file)
    
    
    
    
    #roads - n/s/e/w
     #landbase = ui.showTextInputDialog("Landbase? (n,e,s,w)").upper()
     #street = ui.showTextInputDialog("Street name?").upper()
     #house1 = ui.showTextInputDialog("House number 1 (N/W)").upper()
     #house2 = ui.showTextInputDialog("House number 2 (S/E)").upper()
     
    

def cable(x1,y1,x2,y2):
    x1,y1,x2,y2 = x1*20, y1*20,x2*20,y2*20
    stroke(0)
    strokeWeight(2)
    strokeCap(ROUND)
    dash.line(x1,y1,x2,y2)

def draw():
    pass
'''
def keyPressed():
    global presses
    global pointlist
    global log
    if (key == 'c'):
        if presses == 0:
            pointlist.append(mouseX)
            pointlist.append(mouseY)
            presses = 1
            print('Please choose 2nd point with c key')
        elif presses == 1:
            pointlist.append(mouseX)
            pointlist.append(mouseY)
            cable(pointlist[0],pointlist[1],pointlist[2],pointlist[3])
            for x in range(4):
                log.append(pointlist[x])
            presses = 0
            pointlist = []
    if (key == 'l'):
        println(log)
'''
