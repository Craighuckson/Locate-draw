add_library('dashedlines')
global dash # put here for dashed
#TODO - draw functions

def input(message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)

def setup():
    global dash,f, fs, tree
    size(600,600)
    background(255)
    dash = DashedLines(this) #dashed lines constructor
    strokeWeight(1)
    f = createFont('Arial', 20) # STREET FONT
    fs = createFont('Arial', 12) # LABEL FONT
    hint(ENABLE_NATIVE_FONTS)
    tree = loadImage('Drilling.bmp') # load tree icon in setup
    #loads font that is already present in data
    #f = loadFont(

def draw_curb(landbase):
    strokeWeight(3)
    if landbase == 'N' or landbase == 'n' or landbase == 'S' or landbase == 's':
        line(125,300,475,300)
    elif landbase == 'W' or landbase == 'w' or landbase == 'E' or landbase == 'e':
        line(300,125,300,475)
    
def draw_cable(landbase,cablearray):
    pass
    
def draw_streetname(landbase, street_name):
    pass
    
def draw_labels(landbase):
    pass
    
def draw_tree(landbase):
    pass
def draw_measurements(landbase,cablearray,measarray):
    pass


                  
    
def draw():
    global dash, f, fs, tree
    curb = input('Which direction? (N, E, S, W)')
    num_cables = int(input('How many cables?'))
    #initialize arrays
    cablearray = []
    measarray = []
    
    #get cable locations
    if num_cables == 1:
        cable_location = int(input('Enter cable location - 1-5, 1 closest to curb'))
        cablearray.append(cable_location)
    elif num_cables == 2:
        cable_location1 = int(input('Enter cable location 1 - 1-5, 1 closest to curb'))
        cable_location2 = int(input('Enter cable location 2 - 1-5, 1 closest to curb'))
        cablearray.append(cable_location1)
        cablearray.append(cable_location2)
    else:
        cable_location1 = int(input('Enter cable location 1 - 1-5, 1 closet to curb'))
        cable_location2 = int(input('Enter cable location 2 - 1-5, 1 closest to curb'))
        cable_location3 = int(input('Enter cable location 3 - 1-5, 1 closest to curb'))
        cablearray.append(cable_location1) 
        cablearray.append(cable_location2)
        cablearray.append(cable_location3)
        
    #get measurement text    
    for n in cablearray:
        meas = input('Enter cable measurement')
        if len(meas) == 1:
            meas = '0.' + meas + ' m'
        elif len(meas) == 2:
            meas = meas[0] + '.' + meas[1] + ' m'
        else:
            meas = meas[0] + meas[1] + '.' + meas[2] + ' m'
        measarray.append(meas)
            
        
         
    street_name = input('Enter street name?')
    address = input('Enter address number if applicable')
    print(cablearray)
    print(measarray)
    textFont(f) # sets the font
    strokeWeight(3)
    stroke(0)
    draw_curb(curb)
    #draws S or N curb line
    #line(125,300,475,300)
    #dash.line(0,200,600,200)
    
    #draws tree
    image(tree,280,365) 
    
    #text syntax - text(string,x,y)
    stroke(0)
    fill(0)
    textAlign(CENTER)
    text(street_name, 300, 270)
    textFont(fs) # CHANGES TO SMALLER FONT
    text('SCL', 170, 290)
    strokeWeight(1)
    fill(209,203,190,20) # DIG BOX COLOUR
    rect(150,300,300,150)
    noLoop()
