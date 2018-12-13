import tkinter
from n_jointed_arm_ik import Vector
from input_section import MAX_INPUT, Input_Box

class Angle_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)
        self.angles_array = [0.0] * MAX_INPUT
        self.input_boxes = []
        for i in range(MAX_INPUT):
            next_position = Vector(20, 10 + i * 20)
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
