import math
from n_jointed_arm_ik import Vector
from arm_controller import Arm_Controller
from page_frames import N_Frame, Length_Frame, Weight_Frame, Angle_Frame, Display_Frame, Pathing_Frame
from canvas import IK_Canvas

from input_section import Input_Box, Input_Slider
import tkinter
from tkinter import ttk

TITLE = "N-Joint Inverse Kinematics"
WIDTH = 800
HEIGHT = 500

top = tkinter.Tk()
top.title(TITLE)
top.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+400+10")

pages = ttk.Notebook(top)
pages.place(x=0, y=0)
    
arm_c = Arm_Controller()
def get_arm_controller():
    return arm_c

def Update_N_Event(N):
    get_arm_controller().update_N(N)
    lengths_page.set_N(N)
    weights_page.set_N(N)

def update_arm_lengths(length_array):
    get_arm_controller().update_lengths(length_array)
    
def update_arm_weights(weight_array):
    get_arm_controller().update_weights(weight_array)

N_page = N_Frame(top, Update_N_Event)
lengths_page = Length_Frame(top, update_arm_lengths)
weights_page = Weight_Frame(top, update_arm_weights)
angles_page = Angle_Frame(top)
display_page = Display_Frame(top)
pathing_page = Pathing_Frame(top, get_arm_controller())

pages.add(N_page, text="N")
pages.add(lengths_page, text="Lengths ")
pages.add(weights_page, text="Weights")
pages.add(angles_page, text="Angles")
pages.add(display_page, text="Display")
pages.add(pathing_page, text="Pathing")

canvas = IK_Canvas(top, 400, Vector(420, 10), get_arm_controller)

display_page.bind_canvas(canvas)


def update_angles(angle_array):
    canvas.point = get_arm_controller().point
    canvas.update_point_display()
    angles_page.set_elements(angle_array)
    canvas.update()
arm_c.set_draw_update(update_angles)

top.mainloop()
