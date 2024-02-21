import PySimpleGUI as sg

layout = [[sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), key='graph', enable_events=True, drag_submits=True)]]

window = sg.Window('Drag and Select', layout)

graph = window['graph']

dragging = False
start_point = end_point = prior_rect = None

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'graph':
        x, y = values['graph']
        if not dragging:
            start_point = (x, y)
            dragging = True
        else:
            end_point = (x, y)
            if prior_rect:
                graph.delete_figure(prior_rect)
            prior_rect = graph.draw_rectangle(start_point, end_point, line_color='red')
    elif event.endswith('+UP'):
        dragging = False

window.close()
