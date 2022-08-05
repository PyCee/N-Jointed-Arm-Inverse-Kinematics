
from vector import Vector


def draw_arc(canvas, arc, color):
    offset = canvas.size / 2.0
    center = arc.get_origin() + Vector(offset, offset)
    angle = arc.get_limits()[0] * 180.0 / 3.14159
    angle_range = arc.get_limit_range() * 180.0 / 3.14159
    canvas.create_arc(center.x - arc.get_radius(),
                    center.y - arc.get_radius(),
                    center.x + arc.get_radius(),
                    center.y + arc.get_radius(),
                    start=angle,
                    extent=angle_range,
                    fill=color,
                    style="arc")
    r = 4.0 / canvas.scale_value
    first_point = arc.get_first_point() + Vector(offset, offset)
    canvas.create_oval(first_point.x - r, -r + first_point.y,
                     r + first_point.x, r + first_point.y, 
                     fill="#11f", width=0.0)
    second_point = arc.get_last_point() + Vector(offset, offset)
    canvas.create_oval(second_point.x - r, -r + second_point.y,
                     r + second_point.x, r + second_point.y, 
                     fill="#11f", width=0.0)