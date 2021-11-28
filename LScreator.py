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
        #graph.DrawPolygon([(x,y),(x-0.5,y-1),()])
        pass
    elif dir == 's':
        pass
    elif dir == 'e':
        pass
    else:
        pass

def pole():
    pass

def transformer():
    pass

def vault():
    pass

def ped():
    pass

def road():
    pass

def cable():
    pass

def line():
    pass

        
layout = [      
               [sg.Graph(canvas_size=(480, 480), graph_bottom_left=(0,HEIGHT), graph_top_right=(WIDTH, 0), background_color='white', key='graph', enable_events=True)],
               [sg.Text('Select Image:'),sg.Input(key='file',enable_events=True),sg.FileBrowse(enable_events=True)],
               [sg.Button('Add to image',enable_events=True,key='add')]  
               ]      

window = sg.Window('Graph test', layout, finalize=True,font='Verdana',resizable=True)       

graph = window['graph']
#graph for testing


 

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
        print(event,values)   
        if event == sg.WIN_CLOSED:      
            break
        if event == 'add':
                #print(values['file'])
                graph.DrawText((values['file']), (200,200))
                graph.draw_image(filename=values['file'],location=(100,100))
                window['graph'].update()