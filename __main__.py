import tkinter
from tkinter import ttk
top = tkinter.Tk()

import math
from vector import Vector
from arm_controller import Arm_Controller
from pages.parameters_frame import Parameters_Frame
from pages.display_frame import Display_Frame
from pages.pathing_frame import Pathing_Frame
from canvas import IK_Canvas


TITLE = "N-Joint Inverse Kinematics"
WIDTH = 1030
HEIGHT = 500

top.title(TITLE)
top.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+400+10")

pages = ttk.Notebook(top)
pages.config(width=610)
pages.place(x=0, y=0)
    
arm_c = Arm_Controller()
def get_arm_controller():
    return arm_c

def update_arm_parameters():
    N = parameters_page.get_N()
    length_array = parameters_page.get_lengths()
    lower_limits_array = parameters_page.get_lower_limits()
    upper_limits_array = parameters_page.get_upper_limits()
    weight_array = parameters_page.get_weights()
    #print("N: " + str(N))
    #print("Lengths: " + str(length_array))
    #print("Lower Limits: " + str(lower_limits_array))
    #print("Upper Limits: " + str(upper_limits_array))
    #print("Weights: " + str(weight_array))
    #get_arm_controller().set_N(N)
    #get_arm_controller().set_lengths(length_array)
    #get_arm_controller().set_weights(weight_array)
    get_arm_controller().set_parameters(N, length_array,
                                        lower_limits_array,
                                        upper_limits_array, weight_array)
    
def update_arm_point(point):
    get_arm_controller().set_point(point)

parameters_page = Parameters_Frame(top)
display_page = Display_Frame(top)
pathing_page = Pathing_Frame(top, update_arm_point)

pages.add(parameters_page, text="Arm Parameters")
pages.add(display_page, text="Display Options")
pages.add(pathing_page, text="Pathing")

canvas = IK_Canvas(top, 400, Vector(620, 10), get_arm_controller)

parameters_page.bind_update_parameters_event(update_arm_parameters)
display_page.bind_canvas(canvas)

def update_angles(angle_array):
    canvas.point = get_arm_controller().point
    canvas.update_point_display()
    display_page.set_elements(angle_array)
    canvas.update()
    
arm_c.set_update_event(update_angles)

top.mainloop()
