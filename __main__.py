import math
from n_jointed_arm_ik import Vector, n_jointed_arm_ik, n_joint_range
import tkinter

TITLE = "N-Joint Inverse Kinematics"

top = tkinter.Tk()
top.title(TITLE)

class Input_Thing:
    def __init__(self, title, position, widget):
        self.title = title
        self.position = position
        self.label = tkinter.Label(top, text=title)
        self.label.place(x=position.x, y=position.y)
        self.widget = widget
        self.set_position(position)
    def set_position(self, position):
        self.label.place(x=position.x, y=position.y)
        self.widget.place(x=position.x + 7*len(self.title),
                          y=position.y)
    def get(self):
        return self.widget.get()
class Input_Box (Input_Thing):
    def __init__(self, title, position):
        super().__init__(title, position,
                         tkinter.Entry(top, width=10,
                                       justify="center"))
class Input_Slider (Input_Thing):
    def __init__(self, title, position, command_):
        super().__init__(title, position,
                         tkinter.Scale(top, from_=0, to=1,
                                       resolution=0.001,
                                       orient=tkinter.HORIZONTAL,
                                       command=command_))

NUMBER_CHARACTERS = "1234567890-+."

MAX_N = 10
N = 0
POINT = None
L = []
W = 0.5

length_input_boxes = []
angle_display_boxes = []
for i in range(MAX_N):
    length_input_boxes.append(Input_Box("length_" + str(i) + ":",
                                        Vector(10, i * 20 + 50)))
    length_input_boxes[i].widget.config(state="disabled")
    angle_display_boxes.append(Input_Box("angle_" + str(i) + ":",
                                         Vector(170, i * 20 + 50)))
    angle_display_boxes[i].widget.config(state="disabled")

canvas = None
canvas_size = 400
center_offset = canvas_size / 2.0
MAX_SCALE = 100
canvas_scale = 0.5 * MAX_SCALE

canvas = tkinter.Canvas(top, width=canvas_size, height=canvas_size, bg="white")
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

def draw_rectangle(position, length, radians):
    WIDTH = 0.15
    points = []
    points.append(position.x + WIDTH * math.cos(radians+math.pi/2))
    points.append(position.y + WIDTH * math.sin(radians+math.pi/2))
    points.append(points[0] + length * math.cos(radians))
    points.append(points[1] + length * math.sin(radians))
    points.append(points[2] - WIDTH * math.cos(radians+math.pi/2) * 2)
    points.append(points[3] - WIDTH * math.sin(radians+math.pi/2) * 2)
    points.append(position.x - WIDTH * math.cos(radians+math.pi/2))
    points.append(position.y - WIDTH * math.sin(radians+math.pi/2))

    for i in range(len(points)):
        points[i] += center_offset
        
    canvas.create_polygon(points, fill="black")

def update_canvas():
    '''
    Calculates angles for current lengths/point, calls draw_rectangle
    for each length, and draws circles for appropriate origin and endpoint info
    '''
    global canvas
    global L
    global POINT

    if not POINT:
        return
    if not L:
        return
    canvas.delete("all")
    
    offset = canvas_size / 2.0
    LOW, UPP = n_joint_range(L)
    
    # Draw arm bounds
    BOUNDS_COLOR = "#555"
    BOUNDS_SIZE = 2.0
    canvas.create_oval(-LOW + offset, -LOW + offset,
                       LOW + offset, LOW + offset, 
                       fill="", outline=BOUNDS_COLOR, width=BOUNDS_SIZE)
    canvas.create_oval(-UPP + offset, -UPP + offset,
                       UPP + offset, UPP + offset, 
                       fill="", outline=BOUNDS_COLOR, width=BOUNDS_SIZE)
    
    # Scale POINT if it is outside the bounds
    if not POINT.magnitude() == 0.0:
        if POINT.magnitude() < LOW:
            POINT = POINT.scale(LOW / (POINT.magnitude() * 0.999999999))
        if POINT.magnitude() > UPP:
            POINT = POINT.scale(UPP * 0.999999999 / POINT.magnitude())

    grid_line_offset = get_grid_offset()
    half_line_width = 0.75 / canvas_scale

    # Draw vertical grid lines
    for i in range(-6, 7):
        points = [
            grid_line_offset * i + half_line_width, -get_effective_width(),
            grid_line_offset * i + half_line_width, get_effective_width(),
            grid_line_offset * i - half_line_width, get_effective_width(),
            grid_line_offset * i - half_line_width, -get_effective_width()
        ]
        for i in range(len(points)):
            points[i] += center_offset
        canvas.create_polygon(points, fill="black")
        
    # Draw horizontal grid lines
    for i in range(-6, 7):
        points = [
            -get_effective_width(), grid_line_offset * i + half_line_width,
            get_effective_width(), grid_line_offset * i + half_line_width,
            get_effective_width(), grid_line_offset * i - half_line_width,
            -get_effective_width(), grid_line_offset * i - half_line_width
        ]
        for i in range(len(points)):
            points[i] += center_offset
        canvas.create_polygon(points, fill="black")
        
            
    A = n_jointed_arm_ik(L, W, POINT)
    if not A == None:
        position = Vector(0.0, 0.0)
        for i in range(len(L)):
            angle_display_boxes[i].widget.config(state="normal")
            angle_display_boxes[i].widget.delete(0, tkinter.END)
            angle = round(A[i] * 180 / 3.14159, 3)
            angle_display_boxes[i].widget.insert(0, str(angle))
            angle_display_boxes[i].widget.config(state="disabled")
            absolute_angle = sum(A[:i+1])
            draw_rectangle(position, L[i], absolute_angle)
            position = position.add(Vector(L[i] * math.cos(absolute_angle),
                                           L[i] * math.sin(absolute_angle)))
        
        # Draw circles that represent origin and endpoint
        r = 0.1
        canvas.create_oval(-r + offset, -r + offset, r + offset, r + offset, 
                           fill="#11f", width=0.0)
        canvas.create_oval(POINT.x-r + offset, POINT.y-r + offset,
                           POINT.x+r + offset, POINT.y+r + offset,
                           fill="#f11", width=0.0)
    
    # Scale and translate canvas so arm appears at center
    canvas.scale("all", center_offset, center_offset,
                 canvas_scale, -1.0 * canvas_scale)
    
point_data_boxes = [Input_Box("Point X: ", Vector(10, 270)),
                  Input_Box("Point Y: ", Vector(10, 290))]
point_data_boxes[0].widget.insert(0, "0")
point_data_boxes[1].widget.insert(0, "0")

def set_point(x, y):
    global POINT
    POINT = Vector(x, y)
    
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


def set_input_variables(lengths, point_x, point_y):
    global L
    global POINT
    # Set lengths variable 'L'
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
    global N
    N = int(N_str)
    if N == 0:
        print("Enter a non-zero value for N")
        return
    # Set length input boxes states to NORMAL
    for i in range(N):
        length_input_boxes[i].widget.config(state="normal")
        if i < N-1:
            length_input_boxes[i].widget.bind("<Return>", lambda event, i=i:length_input_boxes[i+1].widget.focus())
        else:
            length_input_boxes[i].widget.bind("<Return>", lambda event:point_data_boxes[0].widget.focus())
    for i in range(N, len(length_input_boxes)):
        length_input_boxes[i].widget.delete(0, tkinter.END)
        length_input_boxes[i].widget.config(state="disabled")
        
    length_input_boxes[0].widget.focus()

# Input box for number of joints
n_input = Input_Box("N: ", Vector(10, 10))
n_input.widget.bind("<Return>", lambda event : set_n(n_input.get()))
set_n_button = tkinter.Button(top, text="Set N", command=lambda : set_n(n_input.get()))
set_n_button.place(x=120, y=7)
n_input.widget.focus()

def set_input_variables_w_boxes():
    '''
    Gathers data from entry fields and calls set_input_variables(...)
    '''
    lengths = []
    if N == 0:
        print("Please enter an N and lengths")
        return
    for i in range(N):
        lengths.append(length_input_boxes[i].widget.get())
    point_x = point_data_boxes[0].widget.get()
    point_y = point_data_boxes[1].widget.get()
    set_input_variables(lengths, point_x, point_y)
    
set_vars_button = tkinter.Button(top, text="Set Arm Variables", command=set_input_variables_w_boxes)
set_vars_button.place(x=10, y=350)

def update_weight_slider(event):
    '''
    Update global W when the slider has been adjusted
    '''
    global W
    W = weight_slider.widget.get()
    update_canvas()
    
weight_slider = Input_Slider("Weight", Vector(10, 400), update_weight_slider)
weight_slider.widget.set(0.5)

def update_scale_slider(event):
    '''
    Update canvas scale
    '''
    global canvas_scale
    canvas_scale = scale_slider.get() * 0.99 * MAX_SCALE + (MAX_SCALE * 0.01)
    update_canvas()
    
scale_slider = Input_Slider("Scale", Vector(10, 450), update_scale_slider)
scale_slider.widget.set(0.5)

# Update point position on mouse click
canvas.bind("<Button-1>", set_point_from_mouse_event)
# Update point position on mouse motion when clicked
canvas.bind("<B1-Motion>", set_point_from_mouse_event)
point_data_boxes[0].widget.bind("<Return>", lambda event: point_data_boxes[1].widget.focus())
point_data_boxes[1].widget.bind("<Return>", lambda event: set_input_variables_w_boxes())

top.geometry("750x500+400+10")
top.mainloop()
