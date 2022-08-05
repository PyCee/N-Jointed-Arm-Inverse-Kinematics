from vector import Vector


def draw_point(canvas, point, fill_color):
    offset = canvas.size / 2.0
    r = 4.0 / canvas.scale_value
    point += Vector(offset, offset)
    canvas.create_oval(point.x - r, -r + point.y,
                     r + point.x, r + point.y, 
                     fill=fill_color, width=0.0)