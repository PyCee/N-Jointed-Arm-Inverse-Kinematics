import tkinter
from n_jointed_arm_ik import Vector
from input_section import MAX_INPUT, Input_Box

class Display_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)
        self.show_grid = tkinter.Checkbutton(self,
                                             text="Show Grid")
        self.show_grid_numbers = tkinter.Checkbutton(self,
                                                     text="Show Grid Numbers")
        self.show_arm_bounds = tkinter.Checkbutton(self,
                                                   text="Show Arm Bounds")
        self.show_angle_text = tkinter.Checkbutton(self,
                                                   text="Show Angle Text")
        self.show_angle_arc = tkinter.Checkbutton(self,
                                                  text="Show Angle Arc")
        self.fit_arm_button = tkinter.Button(self, text="Fit Arm")

        elements = [self.show_grid, self.show_grid_numbers,
                      self.show_arm_bounds, self.show_angle_text,
                      self.show_angle_arc, self.fit_arm_button]
        for i in range(len(elements)):
            elements[i].place(x=20, y=10 + i * 20)
        
        self.label_frame = tkinter.LabelFrame(self,
                                              padx=10, pady=10)
        self.label_frame.place(x=20, y=160)

        self.description="Various toggles that change the canvas display"
        self.label_text = tkinter.Label(self.label_frame,
                                        text=self.description,
                                        wraplength=200)
        self.label_text.pack()

    def bind_canvas(self, canvas):
        self.show_grid.config(variable=canvas.show_grid,
                              command=canvas.update)
        self.show_grid_numbers.config(variable=canvas.show_grid_numbers,
                                      command=canvas.update)
        self.show_arm_bounds.config(variable=canvas.show_arm_bounds,
                                    command=canvas.update)
        self.show_angle_text.config(variable=canvas.show_angle_text,
                                    command=canvas.update)
        self.show_angle_arc.config(variable=canvas.show_angle_arc,
                                   command=canvas.update)
        self.fit_arm_button.config(command=canvas.scale_to_fit_arm)
