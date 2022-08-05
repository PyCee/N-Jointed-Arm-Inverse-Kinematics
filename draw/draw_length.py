import math
from vector import Vector
import display_settings

def draw_length(self, position, length, absolute_radians, relative_radians,
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
        
        if display_settings.ShowAngleText.get():
            # Draw text to show angles
            text_distance = 0.5
            text_radians = absolute_radians + 1.7676#relative_radians / 2.0
            text_base = Vector(math.cos(text_radians),
                            math.sin(text_radians)).scale(text_distance)
            text_base = text_base + start_point

            draw_angle = relative_angle
            end_text = ""
            if display_settings.AngleUnits.get() == display_settings.UNITS_RADIANS:
                draw_angle *= (3.14159 / 180.0)
            else:
                end_text = u'\N{DEGREE SIGN}'
            self.create_text(text_base.x, text_base.y,
                             font=("Times", 10, "bold"), fill="black",
                             anchor="s", text=str(round(draw_angle, 2)) + end_text)
        
        # Draw rectangle to represent arm
        points = [
            start_point.x + cos_width, start_point.y + sin_width,
            end_point.x + cos_width, end_point.y + sin_width,
            end_point.x - cos_width, end_point.y - sin_width,
            start_point.x - cos_width, start_point.y - sin_width]
        self.create_polygon(points, fill="black")