import PySimpleGUI as sg


#i am using a unit system of 24x24 on this one - weird i know
# CONSTANTS

HEIGHT = 24
WIDTH = 24


# WRAPPER FUNCTIONS
def show_grid():
    '''
    Turns grid on
    '''

        # draws grid
    for x in range(0,WIDTH,1):
        graph.DrawLine((x,0),(x,HEIGHT),color='grey')
    for y in range(0,HEIGHT,1):
        graph.DrawLine((0,y),(WIDTH,y),color='grey')

    # draws in numbers
    for a in range(0,WIDTH,2):
        graph.DrawText(a, (a, 0.4), font='Arial 9 normal', angle=90)
    for b in range(0,HEIGHT,2):
        graph.DrawText(b, (0.4, b), font='Arial 9 normal',)

def arrow(dir,x,y):
    '''
     Draws an arrow with head at (x,y)

        Parameters:
            dir (str): one of 'n','s','e' or 'w'
            x(int): number between 0,24
            y(int): number between 0,24

        Returns:
            None
    '''
    if dir.lower() not in ['n','s','e','w']:
        return
    if dir == 'n':
        graph.DrawPolygon([(x,y),(x-0.25,y+0.5),(x+0.25,y+0.5)],fill_color='black',line_color='black')
        graph.DrawLine((x,y+0.5),(x,y+1.5),width=1.5)
    elif dir == 's':
        graph.DrawPolygon([(x,y), (x-0.25, y-0.5), (x+0.25, y-0.5)], fill_color='black', line_color='black')
        graph.DrawLine((x, y-0.5), (x, y-1.5), width=1.5)
    elif dir == 'e':
        graph.DrawPolygon([(x, y), (x - 0.5, y - 0.25), (x - 0.5, y + 0.25)], fill_color='black', line_color='black')
        graph.DrawLine((x-0.5, y), (x-1.5, y), width=1.5)
    else:
        graph.DrawPolygon([(x, y), (x+0.5, y+0.25), (x+0.5, y-0.25)], fill_color='black', line_color='black')
        graph.DrawLine((x+0.5, y), (x+1.5, y), width=1.5)

def pole(x,y):
    graph.draw_circle((x,y), 0.4)

def transformer(x,y):
    graph.draw_rectangle((x-0.5, y-0.5), (x+0.5, y+0.5), line_color='black')
    graph.draw_polygon([(x, y-0.5), (x-0.5, y+0.5), (x+0.5, y+0.5)], fill_color='black')

def vault(util,x,y):
    if util.lower() == 'b':
        vlbl = 'FTG'
    else:
        vlbl = 'HW'
    graph.draw_rectangle((x-0.7, y-0.4), (x+0.7, y+0.4), line_color='black')
    graph.draw_text(vlbl, (x, y), 'Arial 9 normal')

def ped():
    pass

def road(x1, y1, x2, y2):
    graph.draw_line((x1, y1), (x2, y2), width=3)

def cable(x1, y1, x2, y2):
    cable = graph.DrawLine((x1, y1),(x2, y2),width='2')
    graph.TKCanvas.itemconfig(cable,dash=(10,5))
    
def line():
    pass

        
layout = [      
               [sg.Graph(canvas_size=(480, 480), graph_bottom_left=(0,HEIGHT), graph_top_right=(WIDTH, 0), background_color='white', key='graph', enable_events=True, drag_submits=True)],
               [sg.Text('Select Image:'),sg.Input(key='file',enable_events=True),sg.FileBrowse(enable_events=True)],
               [sg.Button('Add to image',enable_events=True,key='add')]  
               ]      

window = sg.Window('Graph test', layout, finalize=True,font='Verdana',resizable=True,return_keyboard_events=True)       

graph = window['graph']
#graph for testing
#show_grid()
arrow('n', 5,7)
arrow('s', 5, 3)
arrow('w', 18,  18)
arrow('e', 14, 14)
pole(16,16)
road(0,7,24,7)
transformer(12,12)
vault('r',9, 9)
cable(0,3,24,3)

#line2 = graph.DrawLine((0,4),(24,4), color='black', width='3')    

#graph.move_figure(line2,0,6)
#graph.draw_image('C:\\Users\\Cr\ped1.png',(0,0))
#road_text = graph.DrawText(('A WEIRD ST'),(240,20),font='Arial 20 normal')
#road_label = graph.DrawText(('SCL'), (440,30))
#cable = graph.DrawLine((0,120),(480,120),width='2')
#graph.TKCanvas.itemconfig(cable,dash=(10,5))
#narrow = graph.DrawPolygon([(100,0),(95,10),(105,10)],fill_color='black')

while True:      
        event, values = window.read()
        #print(event,values)   
        if event == sg.WIN_CLOSED:      
            break
        #if event == 'add':
                #print(values['file'])
                #graph.DrawText((values['file']), (200,200))
                #graph.draw_image(filename=values['file'],location=(100,100))
