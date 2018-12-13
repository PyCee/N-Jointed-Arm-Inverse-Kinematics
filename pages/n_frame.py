import tkinter
from input_section import MAX_INPUT, Input_Box
from n_jointed_arm_ik import Vector

class InvalidNException(Exception):
    pass
class N_Frame(tkinter.Frame):
    def __init__(self, root, update_N_event):
        super().__init__(root, width=1000, height=1000)
        self.numeric_N = 0
        self.input_box = Input_Box(self, "N: ", Vector(20, 10))

        self.update_N_event = update_N_event
        
        self.update_button = tkinter.Button(self,
                                            text="Update N",
                                            command=self.set_N)
        self.update_button.place(x=175, y=10)
        
        self.n_label_frame = tkinter.LabelFrame(self)
        self.n_label_frame.place(x=20, y=50)
        self.n_label_text = tkinter.Label(self.n_label_frame)
        self.n_label_text.pack()
        self.update_variable_display()

        self.label_frame = tkinter.LabelFrame(self, padx=10, pady=10)
        self.label_frame.place(x=20, y=80)

        self.description="'N' is the number of joints our inverse \
        kinematics simulation will deal with. For this simulation, \
        please simulate 2-" + str(MAX_INPUT) + " joints"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()
        
    def set_N(self):
        try:
            tmp_N = int(self.input_box.get())
            if tmp_N < 2 or tmp_N > MAX_INPUT:
                print("Invalid N")
                raise InvalidNException
            self.numeric_N = tmp_N
            self.update_variable_display()
            self.update_N_event(self.numeric_N)
        except ValueError:
            print("Invalid input for N")

    def update_variable_display(self):
        self.n_label_text.config(text="N: " + str(self.numeric_N))
