import math
from n_jointed_arm_ik import Vector, two_jointed_arm_ik, n_jointed_arm_ik, recreate_point, n_joint_point_validity
import tkinter
top = tkinter.Tk()

# TODO:make base Input_Group class the below classes inherit from
class Input_Thing:
    def __init__(self, title, position, widget):
        self.title = title
        self.position = position
        self.label = tkinter.Label(top, text=title)
        self.label.place(x=position.x, y=position.y)
        self.widget = widget#tkinter.Entry(top, width=10, justify="center")
        self.set_position(position)
    def set_position(self, position):
        self.label.place(x=position.x, y=position.y)
        self.widget.place(x=position.x + 7*len(self.title), y=position.y)
    def get(self):
        return self.widget.get()
        
class Input_Box:
    def __init__(self, title, position):
        self.position = position
        self.title = title
        self.label = tkinter.Label(top, text=title)
        self.label.place(x=position.x, y=position.y)
        self.box = tkinter.Entry(top, width=10, justify="center")
        self.set_position(position)
    def set_position(self, position):
        self.label.place(x=position.x, y=position.y)
        self.box.place(x=position.x + 7*len(self.title), y=position.y)
    def get(self):
        return self.box.get()
class Input_Scale:
    def __init__(self, title, position):
        pass
        

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
    length_input_boxes[i].box.config(state="disabled")
    angle_display_boxes.append(Input_Box("angle_" + str(i) + ":",
                                         Vector(170, i * 20 + 50)))
    angle_display_boxes[i].box.config(state="disabled")

canvas = None
canvas_size = 400
canvas_scale = 30

canvas = tkinter.Canvas(top, width=canvas_size, height=canvas_size, bg="white")
canvas.place(x=325, y=10)

def draw_rectangle(position, length, radians):
    WIDTH = 0.1
    points = []
    points.append(position.x + WIDTH * math.cos(radians+math.pi/2))
    points.append(position.y + WIDTH * math.sin(radians+math.pi/2))
    points.append(points[0] + length * math.cos(radians))
    points.append(points[1] + length * math.sin(radians))
    points.append(points[2] - WIDTH * math.cos(radians+math.pi/2) * 2)
    points.append(points[3] - WIDTH * math.sin(radians+math.pi/2) * 2)
    points.append(position.x - WIDTH * math.cos(radians+math.pi/2))
    points.append(position.y - WIDTH * math.sin(radians+math.pi/2))
    
    canvas.create_polygon(points, fill="black")

def update_canvas():
    '''
    Calculates angles for current lengths/point, calls draw_rectangle
    for each length, and draws circles for appropriate origin and endpoint info
    '''
    global canvas
    global L
    global POINT
    
    reach = n_joint_point_validity(L, POINT)
    if not reach:
        return
    A = n_jointed_arm_ik(L, W, POINT)
    position = Vector(0.0, 0.0)
    for i in range(len(L)):
        angle_display_boxes[i].box.config(state="normal")
        angle_display_boxes[i].box.delete(0, tkinter.END)
        angle_display_boxes[i].box.insert(0, str(round(A[i] * 180 / 3.14159, 3)))
        angle_display_boxes[i].box.config(state="disabled")
        absolute_angle = sum(A[:i+1])
        draw_rectangle(position, L[i], absolute_angle)
        position = position.add(Vector(L[i] * math.cos(absolute_angle),
                                       L[i] * math.sin(absolute_angle)))
        
    # Draw circles that represent origin and endpoint
    r = 0.1
    canvas.create_oval(-r, -r, r, r, 
                       fill="#11f", width=0.0)
    canvas.create_oval(POINT.x-r, POINT.y-r, POINT.x+r, POINT.y+r,
                       fill="#f11", width=0.0)
    
    # Scale and translate canvas so arm appears at center
    offset = -canvas_size / (canvas_scale * 2)
    canvas.scale("all", offset - 0.2, -offset - 0.2,
                 canvas_scale, -canvas_scale)

point_data_boxes = [Input_Box("Point X: ", Vector(10, 270)),
                  Input_Box("Point Y: ", Vector(10, 290))]
point_data_boxes[0].box.insert(0, "0")
point_data_boxes[1].box.insert(0, "0")

def set_point(x, y):
    global POINT
    POINT = Vector(x, y)
    update_canvas()
    
    point_data_boxes[0].box.delete(0, tkinter.END)
    point_data_boxes[0].box.insert(0, str(round(x, 3)))
    point_data_boxes[1].box.delete(0, tkinter.END)
    point_data_boxes[1].box.insert(0, str(round(y, 3)))
    
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
    
    # Update data boxes to display current end-point
    
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
        length_input_boxes[i].box.config(state="normal")
        if i < N-1:
            length_input_boxes[i].box.bind("<Return>", lambda event, i=i:length_input_boxes[i+1].box.focus())
        else:
            length_input_boxes[i].box.bind("<Return>", lambda event:point_data_boxes[0].box.focus())
    for i in range(N, len(length_input_boxes)):
        length_input_boxes[i].box.delete(0, tkinter.END)
        length_input_boxes[i].box.config(state="disabled")
        
    length_input_boxes[0].box.focus()

# Input box for number of joints
n_input = Input_Box("N: ", Vector(10, 10))
n_input.box.bind("<Return>", lambda event : set_n(n_input.get()))
set_n_button = tkinter.Button(top, text="Set N", command=lambda : set_n(n_input.get()))
set_n_button.place(x=120, y=7)
n_input.box.focus()

def set_input_variables_w_boxes():
    '''
    Gathers data from entry fields and calls set_input_variables(...)
    '''
    lengths = []
    if N == 0:
        print("Please enter an N and lengths")
        return
    for i in range(N):
        lengths.append(length_input_boxes[i].box.get())
    point_x = point_data_boxes[0].box.get()
    point_y = point_data_boxes[1].box.get()
    set_input_variables(lengths, point_x, point_y)
    
set_vars_button = tkinter.Button(top, text="Set Arm Variables", command=set_input_variables_w_boxes)
set_vars_button.place(x=10, y=350)

def update_weight_scale(event):
    '''
    Update global W when the slider has been adjusted
    '''
    global W
    W = weight_scale.widget.get()
    update_canvas()

weight_scale = Input_Thing("Weight", Vector(10, 400),
                           tkinter.Scale(top, from_=0, to=1, resolution=0.001,
                                         orient=tkinter.HORIZONTAL,
                                         command=update_weight_scale))
weight_scale.widget.set(0.5)

# Update point position on mouse click
canvas.bind("<Button-1>", set_point_from_mouse_event)
# Update point position on mouse motion when clicked
canvas.bind("<B1-Motion>", set_point_from_mouse_event)
point_data_boxes[0].box.bind("<Return>", lambda event: point_data_boxes[1].box.focus())
point_data_boxes[1].box.bind("<Return>", lambda event: set_input_variables_w_boxes())

top.geometry("750x500+400+10")
top.mainloop()
