import math
from n_jointed_arm_ik import Vector, two_jointed_arm_ik, n_jointed_arm_ik, recreate_point, n_joint_point_validity
import tkinter
top = tkinter.Tk()

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

NUMBER_CHARACTERS = "1234567890-+."

n_input = Input_Box("N: ", Vector(10, 10))


POINT = None
L = []
canvas = None
canvas_size = 400
canvas_scale = 30
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

def set_canvas():
    global canvas
    canvas = tkinter.Canvas(top, width=canvas_size, height=canvas_size, bg="white")
    canvas.place(x=325, y=10)
    reach = n_joint_point_validity(L, POINT)
    
    A = n_jointed_arm_ik(L, 0.5, POINT)
    print(A)
    position = Vector(0.0, 0.0)
    
    for i in range(len(L)):
        absolute_angle = sum(A[:i+1])
        draw_rectangle(position, L[i], absolute_angle)
        position = position.add(Vector(L[i] * math.cos(absolute_angle),
                                       L[i] * math.sin(absolute_angle)))
        print(position)
    r = 0.1
    canvas.create_oval(-r, -r, r, r, 
                       fill="#11f", width=0.0)
    canvas.create_oval(POINT.x-r, POINT.y-r, POINT.x+r, POINT.y+r,
                       fill="#f11", width=0.0)
    
    offset = -canvas_size / (canvas_scale * 2)
    canvas.scale("all", offset, -offset,
                 canvas_scale, -canvas_scale)

point_input_boxes = []

def set_point():
    x = point_input_boxes[0].get()
    y = point_input_boxes[1].get()

    if len(x) == 0:
        print("Invalid empty field \'Point X\'")
        return
    if len(y) == 0:
        print("Invalid empty field \'Point Y\'")
        return
    for char in x:
        if char not in NUMBER_CHARACTERS:
            print("Invalid characters in field \'Point X\'")
            return
    for char in y:
        if char not in NUMBER_CHARACTERS:
            print("Invalid characters in field \'Point Y\'")
            return
    global POINT
    
    POINT = Vector(float(x), float(y))
    set_canvas()

    # Remove focus from any of the text boxes
    top.focus()

length_input_boxes = []
set_point_button = tkinter.Button(top, text="Set Point", command=set_point)
def set_lengths():
    global L
    L = [0] * len(length_input_boxes)
    for i in range(len(length_input_boxes)):
        value = length_input_boxes[i].box.get()
        if len(value) == 0:
            print("Invalid empty field \'length_" + str(i) + "\'")
            return
        for char in value:
            if char not in "1234567890.-+":
                print("Invalid characters in field \'length_" + str(i) + "\'")
                return
        L[i] = float(value)
    point_input_position = Vector(10, length_input_boxes[len(length_input_boxes)-1].position.y)
    global point_input_boxes
    if len(point_input_boxes) == 0:
        point_input_boxes = [0] * 2
        point_input_boxes[0] = Input_Box("Point X: ", point_input_position.add(Vector(0, 80)))
        point_input_boxes[1] = Input_Box("Point Y: ", point_input_position.add(Vector(0, 100)))
    else:
        point_input_boxes[0].set_position(point_input_position.add(Vector(0, 80)))
        point_input_boxes[1].set_position(point_input_position.add(Vector(0, 100)))
    
    point_input_boxes[0].box.bind("<Return>", lambda event : point_input_boxes[1].box.focus())
    point_input_boxes[1].box.bind("<Return>", lambda event : set_point())
    set_point_button.place(x=point_input_position.x, y=point_input_position.y+140)
    point_input_boxes[0].box.focus()

set_lengths_button = tkinter.Button(top, text="Set Lengths", command=set_lengths)
def set_n():
    N = n_input.get()
    if len(N) == 0:
        print("Invalid empty field \'N\'")
        return

    # Check that all characters in N are numeric or otherwise related
    for char in N:
        if char not in "1234567890.-+":
            print("Invalid characters in field \'N\'")
            return
    global length_input_boxes
    for input_box in length_input_boxes:
        input_box.label.place_forget()
        input_box.box.place_forget()
    length_input_boxes = []

    # Create input boxes
    for i in range(int(N)):
        length_input_boxes.append(Input_Box("length_" + str(i) + ":",
                                            Vector((i%2) * 160 + 10,
                                                   (i//2) * 20 + 50)))
    # Bind callbacks
    for i in range(int(N)):
        return_function = None
        if i < int(N)-1:
            length_input_boxes[i].box.bind("<Return>", lambda event, i=i : length_input_boxes[i+1].box.focus())
        else:
            length_input_boxes[i].box.bind("<Return>", lambda event : set_lengths())
                                           
    length_input_boxes[0].box.focus()
    set_lengths_button.place(x=10, y=(int(N)//2) * 20 + 75)
    L = []

n_input.box.bind("<Return>", lambda event : set_n())

set_n_button = tkinter.Button(top, text="Set N", command=set_n)
set_n_button.place(x=120, y=7)

n_input.box.focus()


top.geometry("750x500+400+10")
top.mainloop()
