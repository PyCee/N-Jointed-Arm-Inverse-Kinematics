import math
from n_jointed_arm_ik import Vector
from arm_controller import Arm_Controller
from pages.length_frame import Length_Frame
from pages.display_frame import Display_Frame
from pages.pathing_frame import Pathing_Frame
from canvas import IK_Canvas

import tkinter
from tkinter import ttk

TITLE = "N-Joint Inverse Kinematics"
WIDTH = 1030
HEIGHT = 500

top = tkinter.Tk()
top.title(TITLE)
top.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+400+10")

pages = ttk.Notebook(top)
pages.config(width=610)
pages.place(x=0, y=0)
    
arm_c = Arm_Controller()
def get_arm_controller():
    return arm_c

def update_arm_lengths():
    N = lengths_page.get_N()
    length_array = lengths_page.get_lengths()
    weight_array = lengths_page.get_weights()
    #print("N: " + str(N))
    #print("Lengths: " + str(length_array))
    #print("Weights: " + str(weight_array))
    get_arm_controller().set_N(N)
    get_arm_controller().set_lengths(length_array)
    get_arm_controller().set_weights(weight_array)

    get_arm_controller().refresh_results()
    
def update_arm_point(point):
    get_arm_controller().set_point(point)

lengths_page = Length_Frame(top)
display_page = Display_Frame(top)
pathing_page = Pathing_Frame(top, update_arm_point)

pages.add(lengths_page, text="Arm Values")
pages.add(display_page, text="Display Options")
pages.add(pathing_page, text="Pathing")

canvas = IK_Canvas(top, 400, Vector(620, 10), get_arm_controller)

lengths_page.bind_update_lengths_event(update_arm_lengths)
display_page.bind_canvas(canvas)

def update_angles(angle_array):
    canvas.point = get_arm_controller().point
    canvas.update_point_display()
    display_page.set_elements(angle_array)
    canvas.update()
    
arm_c.set_update_event(update_angles)

top.mainloop()
