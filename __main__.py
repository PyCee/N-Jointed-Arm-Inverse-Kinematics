import math
from n_jointed_arm_ik import Vector
from arm_controller import Arm_Controller
from page_frames import N_Frame, Length_Frame, Weight_Frame, Angle_Frame
from canvas import IK_Canvas

from input_section import Input_Box, Input_Slider
import tkinter
from tkinter import ttk

TITLE = "N-Joint Inverse Kinematics"
WIDTH = 750
HEIGHT = 500

top = tkinter.Tk()
top.title(TITLE)
top.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+400+10")

pages = ttk.Notebook(top)
    
arm_c = Arm_Controller()
def get_arm_controller():
    return arm_c

def Update_N_Event(N):
    get_arm_controller().update_N(N)
    lengths_page.set_N(N)
    weights_page.set_N(N)

def update_arm_lengths(length_array):
    print("updating lengths " + str(length_array))
    get_arm_controller().update_lengths(length_array)
    
def update_arm_weights(weight_array):
    print("updating weights " + str(weight_array))
    get_arm_controller().update_weights(weight_array)
    
N_page = N_Frame(top, Update_N_Event)
lengths_page = Length_Frame(top, update_arm_lengths)
weights_page = Weight_Frame(top, update_arm_weights)
angles_page = Angle_Frame(top)


pages.place(x=0, y=10)

pages.add(N_page, text="N")
pages.add(lengths_page, text="Lengths")
pages.add(weights_page, text="Weights")
pages.add(angles_page, text="Angles")

canvas = IK_Canvas(top, 400, get_arm_controller)

canvas.set_position(Vector(325, 10))

def update_angles(angle_array):
    angles_page.set_elements(angle_array)
    canvas.update()
arm_c.set_angle_update(update_angles)


'''
length_input_boxes = []
angle_display_boxes = []
for i in range(MAX_N):
    #in past, created input boxes here
    angle_display_boxes.append(Input_Box(tmp_page, "angle_" + str(i) + ":",
                                         Vector(170, i * 20 + 50)))
    angle_display_boxes[i].widget.config(state="disabled")



canvas = None
canvas_size = 400
center_offset = canvas_size / 2.0
MAX_SCALE = 100
canvas_scale = 0.5 * MAX_SCALE

canvas = tkinter.Canvas(tmp_page, width=canvas_size, height=canvas_size, bg="white")
canvas.place(x=325, y=10)

def get_effective_width():
    return canvas_size / canvas_scale

def get_grid_offset():
    effective_width = get_effective_width()
    half_effective_width = effective_width / 2.0
    upper_width = 2.0
    while upper_width < 200:
        if half_effective_width <= upper_width:
            break
        else:
            upper_width *= 2.0
            
    grid_line_offset = upper_width / 4.0
    return grid_line_offset


def draw_arm(position, length,
             absolute_radians, relative_radians):
    ARM_WIDTH = 3.0 / canvas_scale
    ARC_WIDTH = 7.0 * ARM_WIDTH

    cos_width = ARM_WIDTH * math.cos(absolute_radians+math.pi/2)
    sin_width = ARM_WIDTH * math.sin(absolute_radians+math.pi/2)
    
    cos_length = length * math.cos(absolute_radians)
    sin_length = length * math.sin(absolute_radians)
    offset = Vector(cos_length, sin_length)
    
    start_point = position.add(Vector(center_offset, center_offset))
    end_point = start_point.add(offset)

    # Draw arc to show angle
    absolute_angle = absolute_radians * 180.0 / 3.14159
    relative_angle = relative_radians * 180.0 / 3.14159
    canvas.create_arc(start_point.x - ARC_WIDTH, start_point.y - ARC_WIDTH,
                      start_point.x + ARC_WIDTH, start_point.y + ARC_WIDTH,
                      start=absolute_angle, extent=-1.0 * relative_angle,
                      fill="#bbbbbb")

    # Draw text to show angle

    angle_text_distance = 0.5
    text_radians = absolute_radians - relative_radians / 2.0
    text_base = Vector(math.cos(text_radians),
                       math.sin(text_radians)).scale(angle_text_distance)
    text_base = text_base.add(start_point)
    canvas.create_text(text_base.x, text_base.y,
                       font=("Times", 10, "bold"), fill="black",
                       anchor="s", text=str(round(relative_angle, 2)))
    
    # Draw rectangle to represent arm
    points = [
        start_point.x + cos_width, start_point.y + sin_width,
        end_point.x + cos_width, end_point.y + sin_width,
        end_point.x - cos_width, end_point.y - sin_width,
        start_point.x - cos_width, start_point.y - sin_width,
    ]
    canvas.create_polygon(points, fill="black")

def update_canvas():
    #
    #Calculates angles for current lengths/point, calls draw_rectangle
    #for each length, and draws circles for appropriate origin and endpoint info
    #
    global canvas
    global arm_c
    
    canvas.delete("all")
    
    offset = canvas_size / 2.0
    
    # Draw arm bounds
    BOUNDS_COLOR = "#555"
    BOUNDS_SIZE = 2.0
    canvas.create_oval(-arm_c.lower_bound + offset,
                       -arm_c.lower_bound + offset,
                       arm_c.lower_bound + offset,
                       arm_c.lower_bound + offset, 
                       fill="", outline=BOUNDS_COLOR, width=BOUNDS_SIZE)
    canvas.create_oval(-arm_c.upper_bound + offset,
                       -arm_c.upper_bound + offset,
                       arm_c.upper_bound + offset,
                       arm_c.upper_bound + offset, 
                       fill="", outline=BOUNDS_COLOR, width=BOUNDS_SIZE)

    # Draw grid lines
    grid_line_offset = get_grid_offset()
    half_line_width = 0.75 / canvas_scale
    GRID_COLOR = "#aaa"
    for i in range(-6, 7):
        line_value = grid_line_offset * i
        upper_line_value = line_value + half_line_width
        lower_line_value = line_value - half_line_width
        vert_points = [upper_line_value, -get_effective_width(),
                       upper_line_value, get_effective_width(),
                       lower_line_value, get_effective_width(),
                       lower_line_value, -get_effective_width()]
        horiz_points = [-get_effective_width(), upper_line_value,
                        get_effective_width(), upper_line_value,
                        get_effective_width(), lower_line_value,
                        -get_effective_width(), lower_line_value]
        for j in range(8):
            vert_points[j] += center_offset
            horiz_points[j] += center_offset
        
        canvas.create_polygon(vert_points, fill=GRID_COLOR)
        canvas.create_polygon(horiz_points, fill=GRID_COLOR)

        line_position = center_offset + lower_line_value
        displayed_line_value = str(line_value).rstrip('0').rstrip('.')
        if i != 0:
            # If this is the center line, don't draw the line value
            #   (it looksbad if draw alongside the value for the
            #   horizontal center line)
            
            # Display vertical line values
            canvas.create_text(line_position, center_offset,
                               font=("Times", 10, "bold"),
                               fill="black", anchor="se",
                               text=displayed_line_value)
            
        # Display horizontal line values
        canvas.create_text(center_offset, line_position,
                           font=("Times", 10, "bold"), fill="black",
                           anchor="sw", text=displayed_line_value)
    position = Vector(0.0, 0.0)
    for i in range(len(arm_c.lengths)):
        angle_display_boxes[i].widget.config(state="normal")
        angle_display_boxes[i].widget.delete(0, tkinter.END)
        angle = round(arm_c.angles[i] * 180 / 3.14159, 3)
        angle_display_boxes[i].widget.insert(0, str(angle))
        angle_display_boxes[i].widget.config(state="disabled")
        absolute_angle = sum(arm_c.angles[:i+1])
        draw_arm(position, arm_c.lengths[i], absolute_angle, arm_c.angles[i])
        position = position.add(Vector(arm_c.lengths[i] *
                                       math.cos(absolute_angle),
                                       arm_c.lengths[i] *
                                       math.sin(absolute_angle)))
        
    # Draw circles that represent origin and endpoint
    r = 4.0 / canvas_scale
    canvas.create_oval(-r + offset, -r + offset, r + offset, r + offset, 
                       fill="#11f", width=0.0)
    canvas.create_oval(arm_c.point.x-r + offset, arm_c.point.y-r + offset,
                       arm_c.point.x+r + offset, arm_c.point.y+r + offset,
                       fill="#f11", width=0.0)
    
    # Scale and translate canvas so arm appears at center
    canvas.scale("all", center_offset, center_offset,
                 canvas_scale, -1.0 * canvas_scale)
    
    
point_data_boxes = [Input_Box(tmp_page, "Point X: ", Vector(10, 270)),
                  Input_Box(tmp_page, "Point Y: ", Vector(10, 290))]
point_data_boxes[0].widget.insert(0, "0")
point_data_boxes[1].widget.insert(0, "0")

def set_point(x, y):
    global arm_c
    arm_c.update_point(Vector(x, y))
    
    update_canvas()
    
    point_data_boxes[0].widget.delete(0, tkinter.END)
    point_data_boxes[0].widget.insert(0, str(round(x, 3)))
    point_data_boxes[1].widget.delete(0, tkinter.END)
    point_data_boxes[1].widget.insert(0, str(round(y, 3)))
    
    # Set focus to the canvas so we can pick up mouse-move events
    canvas.focus()
    
def set_point_from_mouse_event(event):
    x = event.x
    y = event.y
    # Scale coordinate
    x = float(x) / canvas_scale
    y = -1.0 * float(y) / canvas_scale
    # Translate coordinates
    x = x - 0.5 * (canvas_size / canvas_scale)
    y = y + 0.5 * (canvas_size / canvas_scale)
    
    set_point(x, y)
'''

def set_input_variables(lengths, point_x, point_y):
    global arm_c
    '''
    L = []
    for i in range(len(lengths)):
        value = lengths[i]
        if len(value) == 0:
            print("Invalid empty field \'length_" + str(i) + "\'")
            return
        for char in value:
            if char not in "1234567890.-+":
                print("Invalid characters in field \'length_" + str(i) + "\'")
                return
        length = float(value)
        if length == 0.0:
            print("Invalid length value \'0.0\' in field \'length_" + str(i) + "\'")
            return
        L.append(float(value))
        
    arm_c.update_lengths(L)
    
    # Set point variable 'POINT'
    if len(point_x) == 0:
        print("Invalid empty field \'Point X\'")
        return
    if len(point_y) == 0:
        print("Invalid empty field \'Point Y\'")
        return
    for char in point_x:
        if char not in NUMBER_CHARACTERS:
            print("Invalid characters in field \'Point X\'")
            return
    for char in point_y:
        if char not in NUMBER_CHARACTERS:
            print("Invalid characters in field \'Point Y\'")
            return
    set_point(float(point_x), float(point_y))
'''
def set_n(N_str):
    '''
    Sets global variable N to number in string parameter N_str, and
    sets up length_input_boxes for appropriate use
    '''
    if len(N_str) == 0:
        print("Invalid empty field \'N\'")
        return

    # Check that all characters in N are numeric or otherwise related
    for char in N_str:
        if char not in "1234567890+":
            print("Invalid characters in field \'N\'")
            return
    global length_input_boxes
    global arm_c
    arm_c.update_N(int(N_str))
    # Set length input boxes states to NORMAL
    for i in range(arm_c.N):
        length_input_boxes[i].widget.config(state="normal")
        if i < arm_c.N-1:
            length_input_boxes[i].widget.bind("<Return>",
                                              lambda event, i=i:length_input_boxes[i+1].widget.focus())
        else:
            length_input_boxes[i].widget.bind("<Return>",
                                              lambda event:point_data_boxes[0].widget.focus())
    for i in range(arm_c.N, len(length_input_boxes)):
        length_input_boxes[i].widget.delete(0, tkinter.END)
        length_input_boxes[i].widget.config(state="disabled")
        
    length_input_boxes[0].widget.focus()

# Input box for number of joints
'''
n_input = Input_Box(tmp_page, "N: ", Vector(10, 10))
n_input.widget.bind("<Return>", lambda event : set_n(n_input.get()))
set_n_button = tkinter.Button(tmp_page, text="Set N", command=lambda : set_n(n_input.get()))
set_n_button.place(x=120, y=7)
n_input.widget.focus()
'''
def set_input_variables_w_boxes():
    '''
    Gathers data from entry fields and calls set_input_variables(...)
    
    lengths = []
    if arm_c.N == 0:
        print("Please enter an N and lengths")
        return
    for i in range(arm_c.N):
        lengths.append(length_input_boxes[i].widget.get())
    point_x = point_data_boxes[0].widget.get()
    point_y = point_data_boxes[1].widget.get()
    set_input_variables(lengths, point_x, point_y)
    '''
'''    
set_vars_button = tkinter.Button(tmp_page, text="Set Arm Variables", command=set_input_variables_w_boxes)
set_vars_button.place(x=10, y=350)

def update_weight_slider(event):
    arm_c.update_weights([weight_slider.widget.get()] * arm_c.N)
    update_canvas()
    
weight_slider = Input_Slider(tmp_page, "Weight", Vector(10, 400), update_weight_slider)
weight_slider.widget.set(0.5)

def update_scale_slider(event):
    global canvas_scale
    canvas_scale = scale_slider.get() * 0.99 * MAX_SCALE + (MAX_SCALE * 0.01)
    update_canvas()
    
scale_slider = Input_Slider(tmp_page, "Scale", Vector(10, 450), update_scale_slider)
scale_slider.widget.set(0.5)

# Update point position on mouse click
canvas.bind("<Button-1>", set_point_from_mouse_event)
# Update point position on mouse motion when clicked
canvas.bind("<B1-Motion>", set_point_from_mouse_event)
point_data_boxes[0].widget.bind("<Return>", lambda event: point_data_boxes[1].widget.focus())
point_data_boxes[1].widget.bind("<Return>", lambda event: set_input_variables_w_boxes())
'''

top.mainloop()
