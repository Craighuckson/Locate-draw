import PySimpleGUIWeb as sg

layout = [[sg.Text('My Window')],
            [sg.Input(key='-IN-')],
            [sg.Button('Go'), sg.Button('Exit')],
            [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), background_color='white', key='graph', enable_events=True, drag_submits=True)],
]

window = sg.Window('Window Title', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event == 'Go':
        sg.popup('You entered', values['-IN-'])
    """
    if event == 'graph':
        (x,y) = values['graph']
        sg.Graph.draw_circle(window['graph'], (x, y), 10, fill_color='red')
    """
    #drag the mouse to draw a blue line
    if event == 'graph+DRAG':
        (x,y) = values['graph']
        sg.Graph.draw_line(window['graph'], (x, y), (x+1, y+1), color='blue')
    #drag the mouse to draw a red line
    if event == 'graph+RIGHT_DRAG':
        (x,y) = values['graph']
        sg.Graph.draw_line(window['graph'], (x, y), (x+1, y+1), color='red')

window.close()

