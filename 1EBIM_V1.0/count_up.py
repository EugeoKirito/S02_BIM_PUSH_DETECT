# import random
# import PySimpleGUI as sg
# import numpy as np
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot

# This is matplot
# fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
# t = ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']
# data = [0,0,0,0,0,0,0]
#
# matplotlib.use("TkAgg")
# fig.add_subplot(111).plot(t, data)

# this is fresh count
# class Singleton(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance
#
#     def __init__(self):
#         self.pwm = 0
# Dados = Singleton()  # instance Single
# def update(num):
#     print('update')
#     Dados.pwm = num
# layout = [
#     # [sg.Canvas(key="-CANVAS-")],
#     [sg.Button('Total Push Count'), sg.Button(Dados.pwm, key='pwm'), ]
# ]
# push_count = 0
# janela = sg.Window('Statistic', layout=layout, size=(500, 450),
#                    location=(0, 0),
#                    finalize=True,
#                    element_justification="center",
#                    font="Helvetica 18", )
# def draw_figure(canvas, figure):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
#     return figure_canvas_agg


# draw_figure(janela["-CANVAS-"].TKCanvas, fig)
# push_count = 1
# def update_count():
#     global push_count
#     while True:
#         event, values = janela.read(timeout=250)
#         if event == sg.WIN_CLOSED or event == 'Exit':
#             break
#         janela['pwm'](Dados.pwm)
#         janela.Refresh()
#         update(push_count)
#         push_count += 1
#     janela.close()

# update_count()
import math
# import random
# from matplotlib import use as use_agg
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import PySimpleGUI as sg
# import datetime
#
# today = datetime.datetime.now().weekday() + 1
#
# '''this num'''
# push_count = 0
#
#
# class Singleton(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance
#
#     def __init__(self):
#         self.pwm = 0
#
#
# Dados = Singleton()  # instance Single
#
#
# def update(num):
#     print('update')
#     Dados.pwm = num
#
#
# def pack_figure(graph, figure):
#     canvas = FigureCanvasTkAgg(figure, graph.Widget)
#     plot_widget = canvas.get_tk_widget()
#     plot_widget.pack(side='top', fill='both', expand=1)
#     return plot_widget
#
#
# def plot_figure(index, theta):
#     fig = plt.figure(index)  # Active an existing figure
#     ax = plt.gca()  # Get the current axes
#     x = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun']
#     y = [random.randint(1, 10) for i in range(7)]
#     ax.cla()  # Clear the current axes
#     # ax.set_title("Sensor Data")
#     # ax.set_xlabel("Date")
#     ax.set_ylabel("Count")
#     # ax.set_xscale('log')
#     ax.grid()
#     plt.plot(x, y)  # Plot y versus x as lines and/or markers
#     fig.canvas.draw()  # Rendor figure into canvas
#
#
# # Use Tkinter Agg
# use_agg('TkAgg')
# Firsttab = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1')]]
#
# tab_group_layout = [
#     [sg.Tab('Statistic', Firsttab, font='Courier 15', key='FirstTAB')],
# ]
#
# column_layout = [[sg.TabGroup(tab_group_layout, enable_events=True, key='TABGROUP')]]
#
# # PySimplGUI window
# layout = [[sg.Column(column_layout, visible=True, key='GRAPHPANEL')],
#           # [sg.Button(button_text='Result', key='Start')],
#           [sg.Button('Total Push Count'), sg.Button(Dados.pwm, key='pwm')]
#           ]
#
# jiye = sg.Window('Matplotlib', layout,finalize=True)
# # Set Button to repeat
# # jiye['Start'].Widget.configure(repeatdelay=50, repeatinterval=50)
#
# # Initial
# graph1 = jiye['Graph1']
# plt.ioff()  # Turn the interactive mode off
# fig1 = plt.figure(1)  # Create a new figure
# ax1 = plt.subplot(111)  # Add a subplot to the current figure.
# pack_figure(graph1, fig1)  # Pack figure under graph
# theta1 = 0  # theta for fig1
# theta2 = 0  # theta for fig2
# index = 1  # Current Tab
# plot_figure(1, theta1)
# plot_figure(2, theta2)
#
#
# def update_count():
#     global theta1
#     push_count = 1
#     while True:
#         event, values = jiye.read(timeout=250)
#         theta1 = 11  # updat pic value
#         plot_figure(index, theta1)
#         jiye['pwm'](Dados.pwm)
#         # jiye.Refresh()
#         update(push_count)  # update  value
#         push_count+=1

# update_count()

#
# import math
# import random
# from matplotlib import use as use_agg
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import PySimpleGUI as sg
# import time
# import numpy as np
#
# def fig_maker(window):  # this should be called as a thread, then time.sleep() here would not freeze the GUI
#     plt.scatter(np.random.rand(1, 10), np.random.rand(1, 10))
#     window.write_event_value('-THREAD-', 'done.')
#     time.sleep(1)
#     return plt.gcf()
#
# def draw_figure(canvas, figure, loc=(0, 0)):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg
#
#
# def delete_fig_agg(fig_agg):
#     fig_agg.get_tk_widget().forget()
#     plt.close('all')
#
#
#
#
#
# class Singleton(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance
#     def __init__(self):
#         self.pwm = 0
#
# Dados = Singleton()
# def update(num):
#     print('update')
#     Dados.pwm = num
# # Use Tkinter Agg
# use_agg('TkAgg')
# Firsttab = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1')]]
#
# tab_group_layout = [
#     [sg.Tab('Statistic', Firsttab, font='Courier 15', key='FirstTAB')],
# ]
# column_layout = [[sg.TabGroup(tab_group_layout, enable_events=True, key='TABGROUP')]]
#
# layout = [[sg.Button('update'), sg.Button('Stop', key="-STOP-"), sg.Button('Exit', key="-EXIT-")],
#               [sg.Radio('Keep looping', "RADIO1", default=True, size=(12, 3), key="-LOOP-"),
#                sg.Radio('Stop looping', "RADIO1", size=(12, 3), key='-NOLOOP-')],
#               [sg.Text('Plot test', font='Any 18')],
#               [sg.Canvas(size=(500, 500), key='canvas')],
#           # [sg.Column(column_layout, visible=True, key='GRAPHPANEL')],
#           # [sg.Button(button_text='Result', key='Start')],
#           [sg.Button('Total Push Count'), sg.Button(Dados.pwm, key='pwm')]
#           ]
#
#
# push_count = 0
# # janela = sg.Window( 'Test', layout=layout, size=(500, 600) )
# window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
#                        layout, finalize=True)
# fig_agg = None
# def kk(push_count):
#    fig_agg = None
#    while True:
#     push_count += 1
#     event, values = window.read()
#     if event is None:  # if user closes window
#         break
#
#     if event == "update":
#         if fig_agg is not None:
#             delete_fig_agg(fig_agg)
#         fig = fig_maker(window)
#         fig_agg = draw_figure(window['canvas'].TKCanvas, fig)
#         window['pwm'](Dados.pwm)
#
#     if event == "-THREAD-":
#         print('Acquisition: ', values[event])
#         time.sleep(1)
#         if values['-LOOP-'] == True:
#             if fig_agg is not None:
#                 delete_fig_agg(fig_agg)
#             fig = fig_maker(window)
#             fig_agg = draw_figure(window['canvas'].TKCanvas, fig)
#             window.Refresh()
#
#     if event == "-STOP-":
#         window['-NOLOOP-'].update(True)
#
#     if event == "-EXIT-":
#         break
    # while True:
    #     event, values = janela.read( timeout=250 )
    #     janela['pwm']( Dados .pwm )
    #     update(push_count)
    #     push_count += 1
    # janela.close()
# kk(12)

# import math
# import random
# from matplotlib import use as use_agg
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import PySimpleGUI as sg
# import datetime
# import time
# import numpy as np
# today = datetime.datetime.now().weekday() + 1
#
# '''this num'''
# push_count = 0
#
# class Singleton(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance
#
#     def __init__(self):
#         self.pwm = 0
#
#
# Dados = Singleton()  # instance Single
#
#
# def update(num):
#     print('update')
#     Dados.pwm = num



# # Use Tkinter Agg
# use_agg('TkAgg')
# Firsttab = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1')]]
# tab_group_layout = [
#     [sg.Tab('Statistic', Firsttab, font='Courier 15', key='FirstTAB')],
# ]
# column_layout = [[sg.TabGroup(tab_group_layout, enable_events=True, key='TABGROUP')]]
# # PySimplGUI window
# layout = [[sg.Column(column_layout, visible=True, key='GRAPHPANEL')],
#           [sg.Button(button_text='Result', key='Start')],
#           [sg.Button('Total Push Count'), sg.Button(Dados.pwm, key='pwm')]
#           ]
# # sg.Canvas(key="-CANVAS-")
#
# def fig_maker(window):  # this should be called as a thread, then time.sleep() here would not freeze the GUI
#     plt.scatter(np.random.rand(1, 10), np.random.rand(1, 10))
#     window.write_event_value('-THREAD-', 'done.')
#     time.sleep(1)
#     return plt.gcf()
# def draw_figure(canvas, figure, loc=(0, 0)):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg
# def delete_fig_agg(fig_agg):
#     fig_agg.get_tk_widget().forget()
#     plt.close('all')
#
#
#
# jiye = sg.Window('Matplotlib', layout,finalize=True)
# # Initial
# graph1 = jiye['Graph1']
# plt.ioff()  # Turn the interactive mode off
#
#
# def update_count(push_count):
#     global theta1
#     while True:
#         event, values = jiye.read(timeout=250)
#         fig = fig_maker(jiye)
#         fig_agg = draw_figure(jiye['Graph1'].TKCanvas, fig)
#         time.sleep(1)
#         jiye['pwm'](Dados.pwm)
#         jiye.Refresh()
#         update(push_count)  # update  value
#         time.sleep(1)
#         delete_fig_agg(fig_agg)
#


# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import PySimpleGUI as sg
# import matplotlib, time, threading
# from matplotlib import use as use_agg
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# def fig_maker(window):  # this should be called as a thread, then time.sleep() here would not freeze the GUI
#     plt.scatter(np.random.rand(1, 10), np.random.rand(1, 10))
#     window.write_event_value('-THREAD-', 'done.')
#     time.sleep(1)
#     return plt.gcf()
#
#
# def draw_figure(canvas, figure, loc=(0, 0)):
#     figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
#     figure_canvas_agg.draw()
#     figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
#     return figure_canvas_agg
#
#
# def delete_fig_agg(fig_agg):
#     fig_agg.get_tk_widget().forget()
#     plt.close('all')
# class Singleton(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance
#
#     def __init__(self):
#         self.pwm = 0
#
#
# Dados = Singleton()  # instance Single
#
#
# def update(num):
#     print('update')
#     Dados.pwm = num
#
#
#
#
# layout = [[sg.Button('update'), sg.Button('Stop', key="-STOP-"), sg.Button('Exit', key="-EXIT-")],
#           [sg.Radio('Keep looping', "RADIO1", default=True, size=(12, 3), key="-LOOP-"),
#            sg.Radio('Stop looping', "RADIO1", size=(12, 3), key='-NOLOOP-')],
#           [sg.Text('Plot test', font='Any 18')],
#           [sg.Canvas(size=(500, 500), key='canvas')]]
#
#
#
#
# def update_count(push_count):
#     # Use Tkinter Agg
#     use_agg('TkAgg')
#     Firsttab = [[sg.Graph((640, 480), (0, 0), (640, 480), key='Graph1')]]
#     tab_group_layout = [
#         [sg.Tab('Statistic', Firsttab, font='Courier 15', key='FirstTAB')],
#     ]
#     column_layout = [[sg.TabGroup(tab_group_layout, enable_events=True, key='TABGROUP')]]
#     # PySimplGUI window
#     layout = [[sg.Column(column_layout, visible=True, key='GRAPHPANEL')],
#               [sg.Button(button_text='Result', key='Start')],
#               [sg.Button('Total Push Count'), sg.Button(Dados.pwm, key='pwm')]
#               ]
#     window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI',
#                        layout, finalize=True)
#     jiye = window
#     while True:
#         event, values = window.read(1)
#         fig = fig_maker(jiye)
#         fig_agg = draw_figure(jiye['Graph1'].TKCanvas, fig)
#         jiye['pwm'](Dados.pwm)
#         jiye.Refresh()
#         update(push_count)  # update  value
#         time.sleep(1)
#         delete_fig_agg(fig_agg)
#         push_count += 1


# update_count(10)



import random
import PySimpleGUI as sg
import datetime
import cv2
import matplotlib.pyplot as plt



today = datetime.datetime.now().weekday() + 1
class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.pwm = 0


Dados = Singleton()  # instance Single
def update(num):
    print('update')
    Dados.pwm = num


def save_pic(count,today,li):
    x = ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']
    # 绘图
    li[today-1] = count
    plt.plot(x, li)
    # 展示

    plt.savefig("./sta.png")
    plt.close()
    return "./sta.png"


Firsttab = [[sg.Image(key='Graph1')]]
tab_group_layout = [
    [sg.Tab('Statistic', Firsttab, font='Courier 15', key='FirstTAB')],
]
column_layout = [[sg.TabGroup(tab_group_layout, enable_events=True, key='TABGROUP')]]

# PySimplGUI window
layout = [[sg.Column(column_layout, visible=True, key='GRAPHPANEL')],

          [sg.Button('Total Push Count'), sg.Button(Dados.pwm, key='pwm')]
          ]

jiye = sg.Window( 'Result', layout=layout, size=(600,700) )
statis_elem = jiye['Graph1']

def up_img(img_addr):
    statis_pic = cv2.imread(img_addr)
    statis_pic = cv2.resize(statis_pic, (500, 600), interpolation=cv2.INTER_CUBIC)
    img_sta = cv2.imencode('.png', statis_pic)[1].tobytes()
    return img_sta

def update_count(push_count,today,li):
    while True:
        event, values = jiye.read(timeout=250)
        jiye['pwm'](Dados.pwm)
        jiye.Refresh()
        img_addr = save_pic(count=push_count,today=today,li=li)
        statis_elem.update(data=up_img(img_addr))
        update(push_count)  # update  value


# update_count(10)