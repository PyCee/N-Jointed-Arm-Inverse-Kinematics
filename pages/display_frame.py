import tkinter
from tkinter import Checkbutton
from vector import Vector

class Display_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)

        self.angle_labels = []
        self.angle_boxes = []
        
        self.grid_lines_CB = Checkbutton(self, text="Show Grid")
        self.grid_numbers_CB = Checkbutton(self,
                                           text="Show Grid Numbers")
        self.arm_bounds_CB = Checkbutton(self,
                                         text="Show Arm Bounds")
        self.angle_text_CB = Checkbutton(self,
                                         text="Show Angle Text")
        self.angle_arc_CB = Checkbutton(self, text="Show Angle Arc")
        self.fit_arm_button = tkinter.Button(self, text="Fit Arm")

        elements = [self.grid_lines_CB, self.grid_numbers_CB,
                    self.arm_bounds_CB, self.angle_text_CB,
                    self.angle_arc_CB, self.fit_arm_button]
        for i in range(len(elements)):
            elements[i].place(x=200, y=10 + i * 20)
        
    def bind_canvas(self, canvas):
        self.grid_lines_CB.config(variable=canvas.show_grid,
                              command=canvas.update)
        self.grid_numbers_CB.config(variable=canvas.show_grid_numbers,
                                    command=canvas.update)
        self.arm_bounds_CB.config(variable=canvas.show_arm_bounds,
                                  command=canvas.update)
        self.angle_text_CB.config(variable=canvas.show_angle_text,
                                  command=canvas.update)
        self.angle_arc_CB.config(variable=canvas.show_angle_arc,
                                 command=canvas.update)
        self.fit_arm_button.config(command=canvas.scale_to_fit_arm)

    def set_elements(self, angles):

        while len(self.angle_boxes) < len(angles):
            self.add_element()
        while len(self.angle_boxes) > len(angles):
            self.remove_element()
        
        for i in range(len(angles)):
            self.angle_boxes[i].config(state="normal")
            self.angle_boxes[i].delete(0, tkinter.END)
            angle = round(angles[i] * 180 / 3.14159, 3)
            self.angle_boxes[i].insert(0, str(angle))
            self.angle_boxes[i].config(state="disabled")
            
    def add_element(self):
        index = len(self.angle_boxes)
        y_val = 10 + index * 20
        
        label = tkinter.Label(self,
                              text="Angle "+str(index+1)+":")
        label.place(x=20, y=y_val)
        
        a_box = tkinter.Entry(self, width=10, justify="center")
        a_box.place(x=100, y=y_val)
        a_box.delete(0, tkinter.END)
        a_box.insert(0, "0.0")
        a_box.config(state="disabled")
        
        self.angle_labels.append(label)
        self.angle_boxes.append(a_box)
    def remove_element(self):
        self.angle_labels[-1].destroy()
        self.angle_labels = self.angle_labels[:-1]
        
        self.angle_boxes[-1].destroy()
        self.angle_boxes = self.angle_boxes[:-1]
