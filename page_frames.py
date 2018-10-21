import tkinter
from n_jointed_arm_ik import Vector
from input_section import MAX_INPUT, Input_Box


class InvalidNException(Exception):
    pass
class InvalidLengthException(Exception):
    pass
class InvalidWeightException(Exception):
    pass

FRAME_CONTENTS_BASE = Vector(20.0, 10.0)
UPDATE_BUTTON_POSITION = Vector(175, 10.0)

DEFAULT_LENGTH = 1.0

MAX_WEIGHT_INPUT = MAX_INPUT - 2
DEFAULT_WEIGHT = 0.7

class N_Frame(tkinter.Frame):
    def __init__(self, root, update_N_event):
        super().__init__(root, width=1000, height=1000)
        self.numeric_N = 0
        self.input_box = Input_Box(self, "N: ", FRAME_CONTENTS_BASE)

        self.update_N_event = update_N_event
        
        self.update_button = tkinter.Button(self,
                                            text="Update N",
                                            command=lambda self=self:
                                            self.set_N(update_N_event))
        self.update_button.place(x=UPDATE_BUTTON_POSITION.x,
                                 y=UPDATE_BUTTON_POSITION.y)
        
        self.variable_label_frame = tkinter.LabelFrame(self)
        self.variable_label_frame.place(x=FRAME_CONTENTS_BASE.x,
                                        y=FRAME_CONTENTS_BASE.y + 40)
        self.variable_label_text = tkinter.Label(self.variable_label_frame)
        self.variable_label_text.pack()
        self.update_variable_display()

        self.label_frame = tkinter.LabelFrame(self, padx=10, pady=10)
        self.label_frame.place(x=20, y=80)

        self.description="'N' is the number of joints our inverse kinematics simulation will deal with. For this simulation, please simulate 2-" + str(MAX_INPUT) + " joints"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
        
    def set_N(self, update_N_event):
        try:
            tmp_N = int(self.input_box.get())
            if tmp_N < 2 or tmp_N > MAX_INPUT:
                print("Invalid N")
                raise InvalidNException
            self.numeric_N = tmp_N
            self.update_variable_display()
            update_N_event(self.numeric_N)
        except ValueError:
            print("Invalid input for N")

    def update_variable_display(self):
        self.variable_label_text.config(text="N: " + str(self.numeric_N))

class Length_Frame(tkinter.Frame):
    def __init__(self, root, update_arm_lengths):
        super().__init__(root, width=1000, height=1000)
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_position = FRAME_CONTENTS_BASE.add(Vector(0.0,
                                                           i * 20))
            next_box = Input_Box(self, "Length " + str(i) + ":",
                                next_position)
            next_box.widget.insert(0, str(DEFAULT_LENGTH))
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)

        self.update_button = tkinter.Button(self,
                                            text="Update Lengths",
                                            command=lambda self=self:
                                            self.update_arm(update_arm_lengths))
        self.update_button.place(x=UPDATE_BUTTON_POSITION.x,
                                 y=UPDATE_BUTTON_POSITION.y)
        
        self.variable_label_frame = tkinter.LabelFrame(self)
        self.variable_label_frame.place(x=FRAME_CONTENTS_BASE.x,
                                        y=FRAME_CONTENTS_BASE.y + 220)
        self.variable_label_text = tkinter.Label(self.variable_label_frame,
                                                 wraplength=240)
        self.variable_label_text.pack()
        self.update_variable_display([])

        
        self.label_frame = tkinter.LabelFrame(self,
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=300)

        self.description="Lengths determine how far each joint is from the last, and determines the overall reach of the arm. Length 0 is the arm closest to the base"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
        
    def update_arm(self, update_function):
        lengths_array = []
        for i in range(MAX_INPUT):
            if self.input_boxes[i].widget.cget("state") == "disabled":
                break
            
            try:
                length = float(self.input_boxes[i].get())
                if length < 0.0:
                    print("Invalid length at index " + str(i))
                    raise InvalidLengthException
                lengths_array.append(length)
            except ValueError:
                print("Invalid length input at index " + str(index))
                
        self.update_variable_display(lengths_array)
        update_function(lengths_array)
        
    def set_N(self, count):
        for i in range(count):
            self.input_boxes[i].widget.config(state="normal")
        for i in range(count, MAX_INPUT):
            self.input_boxes[i].widget.config(state="disabled")
        
    def update_variable_display(self, lengths):
        self.variable_label_text.config(text="Lengths: " + str(lengths))
            
class Weight_Frame(tkinter.Frame):
    def __init__(self, root, update_arm_weights):
        super().__init__(root, width=1000, height=1000)
        self.input_boxes = []
        for i in range(MAX_WEIGHT_INPUT):
            next_position = FRAME_CONTENTS_BASE.add(Vector(0.0,
                                                           i * 20))
            next_box = Input_Box(self, "Weight " + str(i) + ":",
                                next_position)
            next_box.widget.insert(0, str(DEFAULT_WEIGHT))
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)
            
        self.update_button = tkinter.Button(self, text="Update Weights",
                                            command=lambda self=self:
                                            self.update_arm(update_arm_weights))
        self.update_button.place(x=UPDATE_BUTTON_POSITION.x,
                                 y=UPDATE_BUTTON_POSITION.y)
        
        self.variable_label_frame = tkinter.LabelFrame(self)
        self.variable_label_frame.place(x=FRAME_CONTENTS_BASE.x,
                                        y=FRAME_CONTENTS_BASE.y + 220)
        self.variable_label_text = tkinter.Label(self.variable_label_frame,
                                                 wraplength=240)
        self.variable_label_text.pack()
        self.update_variable_display([])
        
        self.label_frame = tkinter.LabelFrame(self, text="Weights",
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=300)

        self.description="Weight will determine if angles are biased towards the base of point of the arm. A weight of 1.0 will weigh fully towards the base. Because of the way angles are calculated, there are N - 2 allowed weights"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
    
    def update_arm(self, update_function):
        weights_array = []
        for i in range(MAX_WEIGHT_INPUT):
            if self.input_boxes[i].widget.cget("state") == "disabled":
                break
            
            try:
                weight = float(self.input_boxes[i].get())
                if weight > 1.0 or weight < 0.0:
                    print("Invalid weight at index " + str(i))
                    raise InvalidWeightException
                weights_array.append(weight)
            except ValueError:
                print("Invalid weight input at index " + str(index))
        weights_array += [0.0, 0.0]
        self.update_variable_display(weights_array)
        update_function(weights_array)
            
    def set_N(self, count):
        count = count - 2
        for i in range(count):
            self.input_boxes[i].widget.config(state="normal")
        for i in range(count, MAX_WEIGHT_INPUT):
            self.input_boxes[i].widget.config(state="disabled")
            
    def update_variable_display(self, weights):
        self.variable_label_text.config(text="Weights: " + str(weights))

            
class Angle_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)
        self.angles_array = [0.0] * MAX_INPUT
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_position = FRAME_CONTENTS_BASE.add(Vector(0.0,
                                                           i * 20))
            next_box = Input_Box(self, "Angle " + str(i) + ":",
                                next_position)
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)
            
        self.label_frame = tkinter.LabelFrame(self, text="Angles",
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=300)

        self.description="Shows the current angles of the arm (in degrees)"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
            
    def set_elements(self, angles):
        for i in range(len(angles)):
            self.input_boxes[i].widget.config(state="normal")
            self.input_boxes[i].widget.delete(0, tkinter.END)
            angle = round(angles[i] * 180 / 3.14159, 3)
            self.input_boxes[i].widget.insert(0, str(angle))
            self.input_boxes[i].widget.config(state="disabled")

class Display_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)
        self.show_grid = tkinter.Checkbutton(self,
                                             text="Show Grid")
        self.show_arm_bounds = tkinter.Checkbutton(self,
                                                   text="Show Arm Bounds")
        self.show_angle_text = tkinter.Checkbutton(self,
                                                   text="Show Angle Text")
        self.show_angle_arc = tkinter.Checkbutton(self,
                                                  text="Show Angle Arc")
        self.show_grid.place(x=FRAME_CONTENTS_BASE.x,
                             y=FRAME_CONTENTS_BASE.y)
        self.show_arm_bounds.place(x=FRAME_CONTENTS_BASE.x,
                                   y=FRAME_CONTENTS_BASE.y + 20)
        self.show_angle_text.place(x=FRAME_CONTENTS_BASE.x,
                                   y=FRAME_CONTENTS_BASE.y + 40)
        self.show_angle_arc.place(x=FRAME_CONTENTS_BASE.x,
                                   y=FRAME_CONTENTS_BASE.y + 60)
        
        self.label_frame = tkinter.LabelFrame(self,
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=160)

        self.description="Various toggles that change how the canvas is displayed"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
    def bind_canvas(self, canvas):
        self.show_grid.config(variable=canvas.show_grid,
                              command=canvas.update)
        self.show_arm_bounds.config(variable=canvas.show_arm_bounds,
                                    command=canvas.update)
        self.show_angle_text.config(variable=canvas.show_angle_text,
                                    command=canvas.update)
        self.show_angle_arc.config(variable=canvas.show_angle_arc,
                                   command=canvas.update)
