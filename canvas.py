import math
import tkinter
from vector import Vector, Angle_Vector
from input_section import Input_Box, Input_Slider
from arc import Arc, Translate_Arc, Rotate_Arc
from sweep import sweep_area, get_swept_arc_subdivisions
from cull_arc_bounded_area import cull_arc_bounded_area
import display_settings

MAX_SCALE = 100

class IK_Canvas(tkinter.Canvas):

    

    '''TMP'''

    def draw_arc(self, arc):
        offset = self.size / 2.0
        center = arc.get_origin() + Vector(offset, offset)
        angle = arc.get_limits()[0] * 180.0 / 3.14159
        angle_range = arc.get_limit_range() * 180.0 / 3.14159
        self.create_arc(center.x - arc.get_radius(),
                        center.y - arc.get_radius(),
                        center.x + arc.get_radius(),
                        center.y + arc.get_radius(),
                        start=angle,
                        extent=angle_range,
                        fill="#333333",
                        style="arc")
        r = 4.0 / self.scale_value
        first_point = arc.get_first_point() + Vector(offset, offset)
        self.create_oval(first_point.x - r, -r + first_point.y,
                         r + first_point.x, r + first_point.y, 
                         fill="#11f", width=0.0)
        second_point = arc.get_last_point() + Vector(offset, offset)
        self.create_oval(second_point.x - r, -r + second_point.y,
                         r + second_point.x, r + second_point.y, 
                         fill="#11f", width=0.0)
        
    
    def draw_arc_testing(self):
        d_0 = 0.0
        d_180 = math.pi
        d_90 = d_180 / 2.0
        d_45 = d_180 / 4.0
        d_30 = d_180 / 6.0
        d_15 = d_180 / 12.0
        d_135 = d_45 * 3.0
    
        from limited_n_jointed_arm_ik import limited_n_jointed_arm_range
        '''
        arcs = limited_n_jointed_arm_range([1.0, 1.0, 1.0],
                                           [-d_90, -d_90, -d_90],
                                           [d_90, d_90, d_90])
        '''
        arcs = limited_n_jointed_arm_range([1, 1, 1],
                                           [d_0, d_0, d_0],
                                           [d_90, d_90, d_90])
        
        arcs = limited_n_jointed_arm_range([1, 1],
                                           [d_0, d_0],
                                           [d_90, d_90])
        
        #print(arcs)
        for arc in arcs:
                        self.draw_arc(arc)
        
        
    '''END TMP'''


    def __init__(self, root, size, position, get_arm_controller):
        self.size = size
        self.center = self.size / 2.0
        self.scale_value = 0.5 * MAX_SCALE

        super().__init__(root, width=self.size, height=self.size,
                         bg="white")
        self.place(x=position.x, y=position.y)

        self.point = Vector(0, 0)

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
        self.get_arm_controller = get_arm_controller

    def set_point_from_canvas_event(self, event):
        '''
        Update point from a mouse event on the canvas
        '''
        x = float(event.x) / self.scale_value
        y = -1.0 * float(event.y) / self.scale_value

        x = x - 0.5 * self.get_effective_size()
        y = y + 0.5 * self.get_effective_size()

        self.point = Vector(x, y)
        
        self.update_point_display()
        
        self.get_arm_controller().set_point(self.point)
        
    def update_point_display(self):
        '''
        Set strings in entry widgets to display current point
        '''
        self.point_x_entry.widget.delete(0, tkinter.END)
        self.point_x_entry.widget.insert(0, str(round(self.point.x, 3)))
        self.point_y_entry.widget.delete(0, tkinter.END)
        self.point_y_entry.widget.insert(0, str(round(self.point.y, 3)))
        
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

        self.point = new_point
        
        self.get_arm_controller().set_point(self.point)
        self.update_point_display()

    def update_scale(self, event):
        self.scale_value = self.scale_slider.get() * 0.99 * MAX_SCALE + (MAX_SCALE * 0.01)
        self.update()

    def scale_to_fit_arm(self):
        fit = self.get_arm_controller().upper_bound * 2 * 1.2
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


    def draw_arm(self, position, length, absolute_radians, relative_radians,
                 center_offset):
        
        ARM_WIDTH = 3.0 / self.scale_value
        ARC_WIDTH = 7.0 * ARM_WIDTH
        
        cos_width = ARM_WIDTH * math.cos(absolute_radians+math.pi/2)
        sin_width = ARM_WIDTH * math.sin(absolute_radians+math.pi/2)
    
        cos_length = length * math.cos(absolute_radians)
        sin_length = length * math.sin(absolute_radians)
        offset = Vector(cos_length, sin_length)
        
        start_point = position + Vector(center_offset, center_offset)
        end_point = start_point + offset
        
        absolute_angle = absolute_radians * 180.0 / 3.14159
        relative_angle = relative_radians * 180.0 / 3.14159

        if display_settings.ShowAngleArc.get():
            # Draw arc to show angle
            self.create_arc(start_point.x - ARC_WIDTH,
                            start_point.y - ARC_WIDTH,
                            start_point.x + ARC_WIDTH,
                            start_point.y + ARC_WIDTH,
                            start=absolute_angle,
                            extent=-1.0 * relative_angle,
                            fill="#bbbbbb")

            
        text_distance = 0.5
        text_radians = absolute_radians - relative_radians / 2.0
        text_base = Vector(math.cos(text_radians),
                           math.sin(text_radians)).scale(text_distance)
        text_base = text_base + start_point
        
        if display_settings.ShowAngleText.get():
            # Draw text to show angles
            draw_angle = relative_angle
            if display_settings.AngleUnits.get() == display_settings.UNITS_RADIANS:
                draw_angle *= (3.14159 / 180.0)
            self.create_text(text_base.x, text_base.y,
                             font=("Times", 10, "bold"), fill="black",
                             anchor="s", text=str(round(draw_angle, 2)))
        
        # Draw rectangle to represent arm
        points = [
            start_point.x + cos_width, start_point.y + sin_width,
            end_point.x + cos_width, end_point.y + sin_width,
            end_point.x - cos_width, end_point.y - sin_width,
            start_point.x - cos_width, start_point.y - sin_width]
        self.create_polygon(points, fill="black")
    def draw_arm_bounds(self, lower_bound, upper_bound, offset):
        '''
        Draw arm bounds
        '''
        BOUNDS_COLOR = "#555"
        BOUNDS_SIZE = 2.0
        self.create_oval(-lower_bound + offset,
                         -lower_bound + offset,
                         lower_bound + offset,
                         lower_bound + offset, 
                         fill="", outline=BOUNDS_COLOR, width=BOUNDS_SIZE)
        self.create_oval(-upper_bound + offset,
                         -upper_bound + offset,
                         upper_bound + offset,
                         upper_bound + offset, 
                         fill="", outline=BOUNDS_COLOR, width=BOUNDS_SIZE)

    def draw_grid_lines(self, offset):
        '''
        Draw grid lines
        '''
        grid_line_offset = self.get_grid_offset()
        half_line_width = 0.75 / self.scale_value
        GRID_COLOR = "#aaa"
        for i in range(-6, 7):
            line_value = grid_line_offset * i
            upper_line_value = line_value + half_line_width
            lower_line_value = line_value - half_line_width
            vert_points = [upper_line_value, -self.get_effective_size(),
                           upper_line_value, self.get_effective_size(),
                           lower_line_value, self.get_effective_size(),
                           lower_line_value, -self.get_effective_size()]
            horiz_points = [-self.get_effective_size(), upper_line_value,
                            self.get_effective_size(), upper_line_value,
                            self.get_effective_size(), lower_line_value,
                            -self.get_effective_size(), lower_line_value]
            for j in range(8):
                vert_points[j] += offset
                horiz_points[j] += offset
                
                
            self.create_polygon(vert_points, fill=GRID_COLOR)
            self.create_polygon(horiz_points, fill=GRID_COLOR)

            line_position = offset + lower_line_value
            displayed_line_value = str(line_value).rstrip('0').rstrip('.')
            if display_settings.ShowGridNumbers.get():
                if i != 0:
                    # If this is the center line, don't draw the line value
                    #   (it looksbad if draw alongside the value for the
                    #   horizontal center line)
                    
                    # Display vertical line values
                    self.create_text(line_position, offset,
                                     font=("Times", 10, "bold"),
                                     fill="black", anchor="se",
                                     text=displayed_line_value)
                    
                # Display horizontal line values
                self.create_text(offset, line_position,
                                 font=("Times", 10, "bold"), 
                                 fill="black",
                                 anchor="sw", 
                                 text=displayed_line_value)

    def update(self):
        self.delete("all")

        offset = self.size / 2.0
        if display_settings.ShowGrid.get():
            self.draw_grid_lines(offset)

        arm_controller = self.get_arm_controller()
        if len(arm_controller.lengths) != 0:
            
            if display_settings.ShowArmBounds.get():
                self.draw_arm_bounds(arm_controller.lower_bound,
                                     arm_controller.upper_bound,
                                     offset)
                
            # Draw arms
            position = Vector(0.0, 0.0)
            for i in range(len(arm_controller.lengths)):
                radian = arm_controller.angles[i]
                angle = round(radian * 180 / 3.14159, 3)
                absolute_angle = sum(arm_controller.angles[:i+1])
                self.draw_arm(position, arm_controller.lengths[i],
                              absolute_angle, radian,
                              offset)
                position = position + Vector(arm_controller.lengths[i] *
                                             math.cos(absolute_angle),
                                             arm_controller.lengths[i] *
                                             math.sin(absolute_angle))
            
                # Draw circles that represent origin and endpoint
                r = 4.0 / self.scale_value
                self.create_oval(-r + offset, -r + offset,
                                 r + offset, r + offset, 
                                 fill="#11f", width=0.0)
                self.create_oval(arm_controller.point.x-r + offset,
                                 arm_controller.point.y-r + offset,
                                 arm_controller.point.x+r + offset,
                                 arm_controller.point.y+r + offset,
                                 fill="#f11", width=0.0)
        
        #TMP
        self.draw_arc_testing()
        #END TMP
        
        # Scale and translate canvas so arm base appears at center
        self.scale("all", offset, offset,
                   self.scale_value, -1.0 * self.scale_value)


