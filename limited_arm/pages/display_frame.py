import tkinter
from tkinter import Checkbutton, Radiobutton
from vector import Vector
import display_settings

class Display_Frame(tkinter.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=1000)

        self.angles = []

        self.units_radio_rad = Radiobutton(self, 
                                           variable=display_settings.AngleUnits,
                                           text="radians",
                                           value=display_settings.UNITS_RADIANS)
        self.units_radio_rad.place(y=10, x=20)
        self.units_radio_deg = Radiobutton(self, 
                                           variable=display_settings.AngleUnits,
                                           text="degrees",
                                           value=display_settings.UNITS_DEGREES)
        self.units_radio_deg.place(y=30, x=20)

        self.angle_labels = []
        self.angle_boxes = []
        
        self.grid_lines_CB = Checkbutton(self,
                                         variable=display_settings.ShowGrid,
                                         text="Show Grid")
        self.grid_numbers_CB = Checkbutton(self,
                                           variable=display_settings.ShowGridNumbers,
                                           text="Show Grid Numbers")
        self.arm_bounds_CB = Checkbutton(self,
                                         variable=display_settings.ShowArmBounds,
                                         text="Show Arm Bounds")
        self.angle_text_CB = Checkbutton(self,
                                         variable=display_settings.ShowAngleText,
                                         text="Show Angle Text")
        self.angle_arc_CB = Checkbutton(self, 
                                        variable=display_settings.ShowAngleArc,
                                        text="Show Angle Arc")
        self.fit_arm_button = tkinter.Button(self, text="Fit Arm")

        elements = [self.grid_lines_CB, self.grid_numbers_CB,
                    self.arm_bounds_CB, self.angle_text_CB,
                    self.angle_arc_CB, self.fit_arm_button]
        for i in range(len(elements)):
            elements[i].place(x=200, y=10 + i * 20)
        
    def bind_canvas(self, canvas):
        self.units_radio_rad.config(command=lambda self=self: [self.refresh_angle_elements(), canvas.update()])
        self.units_radio_deg.config(command=lambda self=self: [self.refresh_angle_elements(), canvas.update()])
        
        self.grid_lines_CB.config(command=canvas.update)
        self.grid_numbers_CB.config(command=canvas.update)
        self.arm_bounds_CB.config(command=canvas.update)
        self.angle_text_CB.config(command=canvas.update)
        self.angle_arc_CB.config(command=canvas.update)
        self.fit_arm_button.config(command=canvas.scale_to_fit_arm)
        
    def refresh_angle_elements(self):
        angle_mult = 1
        if display_settings.AngleUnits.get() == display_settings.UNITS_DEGREES:
            angle_mult = (180 / 3.14159)
        for i in range(len(self.angles)):
            self.angle_boxes[i].config(state="normal")
            self.angle_boxes[i].delete(0, tkinter.END)
            angle = round(self.angles[i] * angle_mult, 3)
            self.angle_boxes[i].insert(0, str(angle))
            self.angle_boxes[i].config(state="disabled")
        
    def set_elements(self, angles):
        self.angles = angles
        while len(self.angle_boxes) < len(angles):
            self.add_angle_element()
        while len(self.angle_boxes) > len(angles):
            self.remove_angle_element()
        self.refresh_angle_elements()
        
            
    def add_angle_element(self):
        index = len(self.angle_boxes)
        y_val = 70 + index * 20
        
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
    def remove_angle_element(self):
        self.angle_labels[-1].destroy()
        self.angle_labels = self.angle_labels[:-1]
        
        self.angle_boxes[-1].destroy()
        self.angle_boxes = self.angle_boxes[:-1]
