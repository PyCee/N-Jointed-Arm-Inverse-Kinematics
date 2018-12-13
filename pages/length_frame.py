import tkinter
from n_jointed_arm_ik import Vector
from input_section import MAX_INPUT, Input_Box

DEFAULT_LENGTH = 1.0

class InvalidLengthException(Exception):
    pass
class Length_Frame(tkinter.Frame):
    def __init__(self, root, update_arm_lengths):
        super().__init__(root, width=1000, height=1000)
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_position = Vector(20, 10 + i * 20)
            next_box = Input_Box(self, "Length " + str(i) + ":",
                                 next_position)
            next_box.widget.insert(0, str(DEFAULT_LENGTH))
            next_box.widget.config(state="disabled")
            self.input_boxes.append(next_box)

        self.update_button = tkinter.Button(self,
                                            text="Update Lengths",
                                            command=lambda self=self:
                                            self.update_arm(update_arm_lengths))
        self.update_button.place(x=175, y=10)
        
        self.variable_label_frame = tkinter.LabelFrame(self)
        self.variable_label_frame.place(x=20, y=230)
        self.variable_label_text = tkinter.Label(self.variable_label_frame,
                                                 wraplength=240)
        self.variable_label_text.pack()
        self.update_variable_display([])

        
        self.label_frame = tkinter.LabelFrame(self,
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=300)

        self.description="Lengths determine how far each joint is from the \
        last, and determines the overall reach of the arm. Length 0 is the \
        arm closest to the base"
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
