import tkinter
from n_jointed_arm_ik import Vector
from input_section import MAX_INPUT, Input_Box

MAX_WEIGHT_INPUT = MAX_INPUT - 2
DEFAULT_WEIGHT = 0.7

class InvalidWeightException(Exception):
    pass

class Weight_Frame(tkinter.Frame):
    def __init__(self, root, update_arm_weights):
        super().__init__(root, width=1000, height=1000)
        self.input_boxes = []
        for i in range(MAX_WEIGHT_INPUT):
            next_position = Vector(20, 10 + i * 20)
            next_box = Input_Box(self, "Weight " + str(i) + ":",
                                 next_position)
            next_box.widget.insert(0, str(DEFAULT_WEIGHT))
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)
            
        self.update_button = tkinter.Button(self, text="Update Weights",
                                            command=lambda self=self:
                                            self.update_arm(update_arm_weights))
        self.update_button.place(x=175, y=10)
        
        self.variable_label_frame = tkinter.LabelFrame(self)
        self.variable_label_frame.place(x=20, y=190)
        self.variable_label_text = tkinter.Label(self.variable_label_frame,
                                                 wraplength=240)
        self.variable_label_text.pack()
        self.update_variable_display([])
        
        self.label_frame = tkinter.LabelFrame(self, text="Weights",
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=220)

        self.description="A weight will determine how angles are biased. A weight of 1.0 will weigh the joint away from the point. A weight of 0.0 will weigh the joint nearer to the point. Weights must be in (0.0, 1.0)."
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=250)
        self.label_text.pack()

        self.label_frame_2 = tkinter.LabelFrame(self,
                                              padx=10, pady=10)
        self.label_frame_2.place(x=20, y=360)

        self.description_2 = "A 2 jointed arm can have no weighting (as there are only 2 solutions), so we do not have weights for the last 2 joints, leaving us with N - 2 weights for any N."
        self.label_text_2 = tkinter.Label(self.label_frame_2,
                                        text=self.description_2,
                                        wraplength=250)
        self.label_text_2.pack()
    
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
