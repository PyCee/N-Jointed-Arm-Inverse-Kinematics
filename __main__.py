import tkinter
from tkinter import ttk
top = tkinter.Tk()

from vector import Vector
from arm_controller import Arm_Controller
from pages.parameters_frame import Parameters_Frame
from pages.display_frame import Display_Frame
from pages.pathing_frame import Pathing_Frame
from canvas import IK_Canvas


TITLE = "N-Joint Inverse Kinematics"
WIDTH = 1180
HEIGHT = 500

top.title(TITLE)
top.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+400+10")
from tkinter import ttk
style = ttk.Style(top)
#style.theme_use('default')

pages = ttk.Notebook(top)
pages.config(width=760)
pages.place(x=0, y=0)
    
arm_c = Arm_Controller()
def get_arm_controller():
    return arm_c

def update_arm_parameters():
    N = parameters_page.get_N()
    length_array = parameters_page.get_lengths()
    weight_array = parameters_page.get_weights()
    get_arm_controller().set_parameters(N, length_array, weight_array)
    canvas.update()
    
def update_arm_point(point):
    get_arm_controller().set_point(point)
    canvas.update()

def initialize_arm():
    initial_N = 2
    for i in range(initial_N):
        parameters_page.append_joint()
    get_arm_controller().set_point(Vector(1.0, 0.0))

parameters_page = Parameters_Frame(top)
Active_Display_Frame = Display_Frame(top)
pathing_page = Pathing_Frame(top, update_arm_point)

pages.add(parameters_page, text="Arm Parameters")
pages.add(Active_Display_Frame, text="Display Options")
pages.add(pathing_page, text="Pathing")


canvas = IK_Canvas(top, 400, Vector(770, 10), get_arm_controller)

parameters_page.bind_update_parameters_event(update_arm_parameters)
Active_Display_Frame.bind_canvas(canvas)

def update_angles(angle_array):
    canvas.point = get_arm_controller().point
    canvas.update_point_display()
    Active_Display_Frame.set_elements(angle_array)
    canvas.update()
    
arm_c.set_update_event(update_angles)

initialize_arm()

#pages.select(2)

top.mainloop()