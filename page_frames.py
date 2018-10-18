import tkinter
from n_jointed_arm_ik import Vector
from input_section import MAX_INPUT, Input_Box

class N_Frame(tkinter.Frame):
    def __init__(self, root, update_N_event):
        super().__init__(root, width=1000, height=1000)
        self.numeric_N = 0
        self.input_box = Input_Box(self, "N: ", Vector(0.0, 0.0))

        self.input_box.widget.bind("<FocusOut>", lambda event, self=self:
                                   self.set_N())
        self.update_N_event = update_N_event
        
    def set_N(self):
        try:
            self.numeric_N = int(self.input_box.get())
            print("got a new N")
            self.update_N_event(self.numeric_N)
        except ValueError:
            print("invalid input for N")

class Length_Frame(tkinter.Frame):
    def __init__(self, root, update_arm_lengths):
        super().__init__(root, width=1000, height=1000)
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_box = Input_Box(self, "length_" + str(i) + ":",
                                 Vector(10, i * 20 + 50))
            next_box.widget.insert(0, "1.0")
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)

        self.update_button = tkinter.Button(self, text="Update Lengths",
                                            command=lambda self=self:
                                            self.update_arm(update_arm_lengths))
        self.update_button.place(x=100, y=400)
        
    def update_arm(self, update_function):
        lengths_array = []
        for i in range(MAX_INPUT):
            if self.input_boxes[i].widget.cget("state") == "disabled":
                break
            
            try:
                lengths_array.append(float(self.input_boxes[i].get()))
            except ValueError:
                print("Invalid length input at index " + str(index))
        
        update_function(lengths_array)
    def set_N(self, count):
        for i in range(count):
            self.input_boxes[i].widget.config(state="normal")
        for i in range(count, MAX_INPUT):
            self.input_boxes[i].widget.config(state="normal")
            self.input_boxes[i].widget.delete(0, tkinter.END)
            self.input_boxes[i].widget.insert(0, "1.0")
            self.input_boxes[i].widget.config(state="disabled")

            

class Weight_Frame(tkinter.Frame):
    def __init__(self, root, update_arm_weights):
        super().__init__(root, width=1000, height=1000)
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_box = Input_Box(self, "weight_" + str(i) + ":",
                                 Vector(10, i * 20 + 50))
            next_box.widget.insert(0, "1.0")
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)
            
        self.update_button = tkinter.Button(self, text="Update Weights",
                                            command=lambda self=self:
                                            self.update_arm(update_arm_weights))
        self.update_button.place(x=100, y=400)
    
    def update_arm(self, update_function):
        weights_array = []
        for i in range(MAX_INPUT):
            if self.input_boxes[i].widget.cget("state") == "disabled":
                break
            
            try:
                weights_array.append(float(self.input_boxes[i].get()))
            except ValueError:
                print("Invalid weight input at index " + str(index))
        
        update_function(weights_array)
            
    def set_N(self, count):
        for i in range(count):
            self.input_boxes[i].widget.config(state="normal")
        for i in range(count, MAX_INPUT):
            self.input_boxes[i].widget.config(state="normal")
            self.input_boxes[i].widget.delete(0, tkinter.END)
            self.input_boxes[i].widget.insert(0, "1.0")
            self.input_boxes[i].widget.config(state="disabled")

            
class Angle_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)
        self.angles_array = [0.0] * MAX_INPUT
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_box = Input_Box(self, "angle_" + str(i) + ":",
                                 Vector(10, i * 20 + 50))
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)
            
    def set_elements(self, angles):
        for i in range(len(angles)):
            self.input_boxes[i].widget.config(state="normal")
            self.input_boxes[i].widget.delete(0, tkinter.END)
            angle = round(angles[i] * 180 / 3.14159, 3)
            self.input_boxes[i].widget.insert(0, str(angle))
            self.input_boxes[i].widget.config(state="disabled")
