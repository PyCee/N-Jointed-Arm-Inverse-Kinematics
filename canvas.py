import math
import tkinter
from draw.draw_arm import draw_arm
from draw.draw_bounds import draw_arm_bounds
from draw.draw_grid_lines import draw_grid_lines
from vector import Vector, Angle_Vector
from input_section import Input_Box, Input_Slider
from arc import Arc, Translate_Arc, Rotate_Arc
from limited_arm.sweep import sweep_area, get_swept_arc_subdivisions
from limited_arm.cull_arc_bounded_area import cull_arc_bounded_area
from limited_arm.limited_n_jointed_arm_ik import limited_n_jointed_arm_range
import display_settings

MAX_SCALE = 100

class IK_Canvas(tkinter.Canvas):

    def __init__(self, root, size, position, get_arm_controller):
        self.size = size
        self.center = self.size / 2.0
        self.scale_value = 0.5 * MAX_SCALE
        self.get_arm_controller = get_arm_controller

        super().__init__(root, width=self.size, height=self.size,
                         bg="white")
        self.place(x=position.x, y=position.y)

        self.point_x_entry = Input_Box(root, "Point X",
                                       Vector(x=0, y=0))
        self.point_y_entry = Input_Box(root, "Point Y",
                                       Vector(x=0, y=0))
        self.update_button =tkinter.Button(root,
                                           text="Update Point",
                                           command=lambda self=self:
                                           self.get_input_box_point())

        self.update_point_display()
        
        self.scale_slider = Input_Slider(root, "Scale Canvas",
                                         Vector(x=0, y=0),
                                         lambda event, self=self:
                                         self.update_scale(event))
        self.scale_slider.widget.set(0.5)

        self.bind("<Button-1>", lambda event, self=self:
                  self.set_point_from_canvas_event(event))
        self.bind("<B1-Motion>", lambda event, self=self:
                  self.set_point_from_canvas_event(event))

        x_entry_position = Vector(position.x,
                                  position.y + self.size + 10)
        self.point_x_entry.set_position(x_entry_position)

        y_entry_position = x_entry_position + Vector(140, 0)
        self.point_y_entry.set_position(y_entry_position)

        button_position = y_entry_position + Vector(140, 0)
        self.update_button.place(x=button_position.x,
                                 y=button_position.y)

        scale_slider_position = Vector(position.x,
                                       position.y + self.size + 40)
        self.scale_slider.set_position(scale_slider_position)

    def set_point_from_canvas_event(self, event):
        '''
        Update point from a mouse event on the canvas
        '''
        x = float(event.x) / self.scale_value
        y = -1.0 * float(event.y) / self.scale_value

        x = x - 0.5 * self.get_effective_size()
        y = y + 0.5 * self.get_effective_size()
        
        self.get_arm_controller().set_point(Vector(x, y))
        self.update()
        
    def update_point_display(self):
        '''
        Set strings in entry widgets to display current point
        '''

        if(self.get_arm_controller().point == None):
            return
        point = self.get_arm_controller().point
        self.point_x_entry.widget.delete(0, tkinter.END)
        self.point_x_entry.widget.insert(0, str(round(point.x, 3)))
        self.point_y_entry.widget.delete(0, tkinter.END)
        self.point_y_entry.widget.insert(0, str(round(point.y, 3)))
        
    def get_input_box_point(self):
        '''
        Get data from entry widgets and update point
        '''
        new_point = Vector(0.0, 0.0)
        try:
            new_point.x = float(self.point_x_entry.widget.get())
        except ValueError:
            print("Invalid Point X Input")
        try:
            new_point.y = float(self.point_y_entry.widget.get())
        except ValueError:
            print("Invalid Point Y Input")
        
        self.get_arm_controller().set_point(new_point)
        self.update_point_display()
        self.update()

    def update_scale(self, event):
        self.scale_value = self.scale_slider.get() * 0.99 * MAX_SCALE + (MAX_SCALE * 0.01)
        self.update()

    def scale_to_fit_arm(self):
        fit = self.get_arm_controller().get_bounds()[1] * 2 * 1.2
        if fit != 0.0:
            self.scale_value = self.size / fit
            self.scale_slider.widget.set(self.scale_value / 
                                         MAX_SCALE)
            self.update()
        
    def get_effective_size(self):
        return self.size / self.scale_value
    
    def get_grid_offset(self):
        effective_size = self.get_effective_size()
        half_effective_size = effective_size / 2.0
        upper_size = 2.0
        while upper_size < 200:
            if half_effective_size <= upper_size:
                break
            else:
                upper_size *= 2.0
            
        grid_line_offset = upper_size / 4.0
        return grid_line_offset

    

    def update(self):
        self.delete("all")

        offset = self.size / 2.0
        if display_settings.ShowGrid.get():
            draw_grid_lines(self, offset)

        arm_controller = self.get_arm_controller()
        if len(arm_controller.lengths) != 0:
            
            if display_settings.ShowArmBounds.get():
                draw_arm_bounds(self, arm_controller.get_bounds(), offset)
                #self.draw_arm_bounds(arm_controller.get_arc_bounded_area())
                
            # Draw arms
            draw_arm(self, arm_controller, offset)
        
        if(display_settings.ShowEndPointCoords.get()):
            coords_offset = 0.075
            self.create_text(offset + arm_controller.point.x + coords_offset, offset + arm_controller.point.y - coords_offset,
								font=("Times", 10, "bold"), 
								fill="#333",
								anchor="nw", 
								text=str(arm_controller.point))

        #TMP
        #self.draw_arc_testing()
        #END TMP
        
        self.update_point_display()
        # Scale and translate canvas so arm base appears at center
        self.scale("all", offset, offset,
                   self.scale_value, -1.0 * self.scale_value)


